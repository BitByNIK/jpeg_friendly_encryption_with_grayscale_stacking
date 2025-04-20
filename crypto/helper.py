import numpy as np
import random
from dataclasses import dataclass
from config import BLOCK_SIZE, SEED, VARIANCE_THRESHOLD


@dataclass
class TransformKeys:
    indices: list
    rf_values: list
    np_flags: list
    xor_keys: list


def permute(blocks):
    num_blocks = len(blocks)
    indices = list(range(num_blocks))

    random.seed(SEED)
    random.shuffle(indices)

    transformed_blocks = blocks[indices]

    return transformed_blocks, indices


def undo_permute(transformed_blocks, indices):
    blocks = np.empty_like(transformed_blocks)

    for i, idx in enumerate(indices):
        blocks[idx] = transformed_blocks[i]

    return blocks


flip_functions = {
    0: lambda x: x,
    1: np.fliplr,
    2: np.flipud,
}


def apply_rotation_and_flipping(blocks):
    np.random.seed(SEED)
    transformed_blocks = []
    rf_values = []

    for block in blocks:
        rot_k = np.random.randint(0, 4)
        rotated_block = np.rot90(block, k=rot_k)

        flip_mode = np.random.randint(0, 3)
        flipped_block = flip_functions[flip_mode](rotated_block)

        transformed_blocks.append(flipped_block)
        rf_values.append((rot_k, flip_mode))

    return np.array(transformed_blocks), rf_values


def undo_rotation_and_flipping(transformed_blocks, rf_values):
    blocks = []
    for transformed_block, (rot_k, flip_mode) in zip(transformed_blocks, rf_values):
        unflipped_block = flip_functions[flip_mode](transformed_block)
        unrotated_block = np.rot90(unflipped_block, k=(4 - rot_k) % 4)
        blocks.append(unrotated_block)

    return np.array(blocks)


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


def undo_negative_positive(transformed_blocks, np_flags):
    blocks = []
    for transformed_block, apply_neg in zip(transformed_blocks, np_flags):
        if apply_neg:
            block = 255 - transformed_block
        else:
            block = transformed_block
        blocks.append(block)

    return np.array(blocks)


def apply_intensity_modulation(blocks):
    transformed_blocks = []
    xor_keys = []

    for block in blocks:
        block_variance = np.var(block)
        if block_variance < VARIANCE_THRESHOLD:
            xor_value = np.random.randint(0, 4, dtype=np.uint8)
        else:
            xor_value = np.random.randint(0, 16, dtype=np.uint8)

        xor_key = np.full((BLOCK_SIZE, BLOCK_SIZE), xor_value, dtype=np.uint8)
        transformed_blocks.append(np.bitwise_xor(block, xor_key))
        xor_keys.append(xor_key)

    return np.array(transformed_blocks), xor_keys


def undo_intensity_modulation(transformed_blocks, xor_keys):
    blocks = []
    for transformed_block, xor_key in zip(transformed_blocks, xor_keys):
        block = np.bitwise_xor(transformed_block, xor_key)
        blocks.append(block)

    return np.array(blocks)


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
