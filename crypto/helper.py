import numpy as np
import random
from config import BLOCK_SIZE, SEED


def permute_blocks(blocks):
    num_blocks = len(blocks)
    indices = list(range(num_blocks))

    random.seed(SEED)
    random.shuffle(indices)

    transformed_blocks = blocks[indices]

    return transformed_blocks, indices


def apply_rotation_and_flipping(blocks):
    np.random.seed(SEED)
    transformed_blocks = []
    rf_values = []

    for block in blocks:
        rot_k = np.random.randint(0, 4)
        rotated_block = np.rot90(block, k=rot_k)

        flip_functions = {
            0: lambda x: x,
            1: np.fliplr,
            2: np.flipud,
        }
        flip_mode = np.random.randint(0, 3)
        flipped_block = flip_functions[flip_mode](rotated_block)

        transformed_blocks.append(flipped_block)
        rf_values.append((rot_k, flip_mode))

    return np.array(transformed_blocks), rf_values


def apply_negative_positive(blocks):
    np.random.seed(SEED)
    transformed_blocks = []
    np_flags = []

    for block in blocks:
        apply_neg = np.random.rand() < 0.5
        if apply_neg:
            block = 255 - block
        transformed_blocks.append(block)
        np_flags.append(apply_neg)

    return np.array(transformed_blocks), np_flags


def merge_blocks(blocks, original_shape):
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
