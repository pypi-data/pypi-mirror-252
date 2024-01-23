import math
import sys

import numpy as np
from tqdm.auto import tqdm

from wtpsplit.utils import Constants, hash_encode


class ORTWrapper:
    def __init__(self, config, ort_session):
        self.config = config
        self.ort_session = ort_session

    def __getattr__(self, name):
        assert hasattr(self, "ort_session")
        return getattr(self.ort_session, name)

    def __call__(self, hashed_ids, attention_mask):
        logits = self.ort_session.run(
            ["logits"],
            {
                "attention_mask": attention_mask.astype(np.float16), # ORT expects fp16 mask
                "hashed_ids": hashed_ids,
            },
        )[0]

        return {"logits": logits}


class PyTorchWrapper:
    def __init__(self, model):
        self.model = model
        self.config = model.config

    def __getattr__(self, name):
        assert hasattr(self, "model")
        return getattr(self.model, name)

    def __call__(self, hashed_ids, attention_mask, language_ids=None):
        try:
            import torch
        except ImportError:
            raise ImportError("`torch` must be installed to use PyTorch models!")

        with torch.no_grad():
            logits = (
                self.model(
                    hashed_ids=torch.from_numpy(hashed_ids).to(self.model.device),
                    attention_mask=torch.from_numpy(attention_mask).to(self.model.device),
                    language_ids=torch.from_numpy(language_ids).to(self.model.device)
                    if language_ids is not None
                    else None,
                )["logits"]
                .cpu()
                .numpy()
            )

        return {"logits": logits}

def extract(
    batch_of_texts,
    model,
    stride,
    block_size,
    batch_size,
    lang_code=None,
    pad_last_batch=False,
    verbose=False,
):
    """
    Computes logits for the given batch of texts by:
        1. slicing the texts into chunks of size `block_size`.
        2. passing every chunk through the model forward.
        3. stitching predictings back together by averaging chunk logits.

    ad 1.: text is sliced into partially overlapping chunks by moving forward by a `stride` parameter (think conv1d).
    """

    text_lengths = [len(text) for text in batch_of_texts]
    # reduce block size if possible
    block_size = min(block_size, max(text_lengths))

    # make sure block_size is a multiple of downsampling rate
    downsampling_rate = getattr(model.config, "downsampling_rate", 1)
    block_size = math.ceil(block_size / downsampling_rate) * downsampling_rate

    # total number of forward passes
    num_chunks = sum(math.ceil(max(length - block_size, 0) / stride) + 1 for length in text_lengths)
    
    # preallocate a buffer for all input hashes & attention masks
    input_hashes = np.zeros((num_chunks, block_size, model.config.num_hash_functions), dtype=np.int64)
    attention_mask = np.zeros((num_chunks, block_size), dtype=np.float32)

    # locs keep track of the location of every chunk with a 3-tuple (text_idx, char_start, char_end) that indexes
    # back into the batch_of_texts
    locs = np.zeros((num_chunks, 3), dtype=np.int32)

    # this is equivalent to (but faster than) np.array([ord(c) for c in "".join(batch_of_texts)]) 
    codec = "utf-32-le" if sys.byteorder == "little" else "utf-32-be"
    ordinals = np.frombuffer(bytearray("".join(batch_of_texts), encoding=codec), dtype=np.int32)
    
    # hash encode all ids 
    flat_hashed_ids = hash_encode(ordinals, 
                                  num_hashes=model.config.num_hash_functions, 
                                  num_buckets=model.config.num_hash_buckets)
    offset = 0
    current_chunk = 0

    for i in range(len(batch_of_texts)):
        for j in range(0, text_lengths[i], stride):
            # for every chunk, assign input hashes, attention mask and loc
            start, end = j, j + block_size
            done = False

            if end >= text_lengths[i]:
                end = text_lengths[i]
                start = max(end - block_size, 0)
                done = True

            input_hashes[current_chunk, : end - start] = flat_hashed_ids[offset + start : offset + end]
            attention_mask[current_chunk, : end - start] = 1
            locs[current_chunk, :] = [i, start, end]

            current_chunk += 1

            if done:
                break

        offset += text_lengths[i]

    assert current_chunk == num_chunks
    n_batches = math.ceil(len(input_hashes) / batch_size)

    # containers for the final logits
    all_logits = [
        np.zeros(
            (
                length,
                model.config.num_labels,
            ),
            dtype=np.float16,
        )
        for length in text_lengths
    ]
    # container for the number of chunks that any character was part of (to average chunk predictions)
    all_counts = [np.zeros(length, dtype=np.int16) for length in text_lengths]

    uses_lang_adapters = getattr(model.config, "language_adapter", "off") == "on"
    if uses_lang_adapters:
        if lang_code is None:
            raise ValueError("Please specify a `lang_code` when using a model with language adapters.")

        if isinstance(model, ORTWrapper):
            raise ValueError("Language adapters are not supported in ONNX models.")

        language_ids = np.array(
            [Constants.LANG_CODE_TO_INDEX[lang_code]] * batch_size,
            dtype=int,
        )
    else:
        language_ids = None

    # forward passes through all chunks
    for batch_idx in tqdm(range(n_batches), disable=not verbose):
        start, end = batch_idx * batch_size, min(len(input_hashes), (batch_idx + 1) * batch_size)

        batch_input_hashes = input_hashes[start:end]
        batch_attention_mask = attention_mask[start:end]

        if len(batch_input_hashes) < batch_size and pad_last_batch:
            n_missing = batch_size - len(batch_input_hashes)

            batch_input_hashes = np.pad(batch_input_hashes, ((0, n_missing), (0, 0), (0, 0)))
            batch_attention_mask = np.pad(batch_attention_mask, ((0, n_missing), (0, 0)))

        kwargs = {"language_ids": language_ids[: len(batch_input_hashes)]} if uses_lang_adapters else {}

        logits = model(
            hashed_ids=batch_input_hashes,
            attention_mask=batch_attention_mask,
            **kwargs,
        )["logits"]

        for i in range(start, end):
            original_idx, start_char_idx, end_char_idx = locs[i]
            all_logits[original_idx][start_char_idx:end_char_idx] += logits[i - start, : end_char_idx - start_char_idx]
            all_counts[original_idx][start_char_idx:end_char_idx] += 1

    # so far, logits are summed, so we average them here
    all_logits = [(logits / counts[:, None]).astype(np.float16) for logits, counts in zip(all_logits, all_counts)]

    return all_logits
