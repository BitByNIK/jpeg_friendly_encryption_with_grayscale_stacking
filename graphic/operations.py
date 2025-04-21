import numpy as np
from typing import Tuple
from config import BLOCK_SIZE


def pad_to_block_size(img_np: np.ndarray) -> np.ndarray:
    h, w = img_np.shape
    pad_h = (BLOCK_SIZE - h % BLOCK_SIZE) % BLOCK_SIZE
    pad_w = (BLOCK_SIZE - w % BLOCK_SIZE) % BLOCK_SIZE

    padded_img_np = np.pad(img_np, ((0, pad_h), (0, pad_w)), mode='edge')

    return padded_img_np


def divide_into_blocks(img_np: np.ndarray) -> np.ndarray:
    h, w = img_np.shape
    blocks = (img_np.reshape(h // BLOCK_SIZE, BLOCK_SIZE, w // BLOCK_SIZE, BLOCK_SIZE)
              .swapaxes(1, 2)
              .reshape(-1, BLOCK_SIZE, BLOCK_SIZE))

    return blocks


def merge_blocks(blocks: np.ndarray, original_shape: Tuple[int, int]) -> np.ndarray:
    h, w = original_shape
    padded_h = ((h + BLOCK_SIZE - 1) // BLOCK_SIZE) * BLOCK_SIZE
    padded_w = ((w + BLOCK_SIZE - 1) // BLOCK_SIZE) * BLOCK_SIZE
    num_blocks_w = padded_w // BLOCK_SIZE

    merged = (
        blocks.reshape(padded_h // BLOCK_SIZE,
                       num_blocks_w, BLOCK_SIZE, BLOCK_SIZE)
        .swapaxes(1, 2)
        .reshape(padded_h, padded_w)
    )

    return merged[:h, :w]
