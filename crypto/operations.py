import numpy as np
from typing import Tuple
from crypto.helper import permute, apply_rotation_and_flipping, apply_negative_positive, appy_intensity_modulation, merge_blocks


def encrypt(blocks: np.ndarray, original_shape: Tuple[int, int]) -> np.ndarray:
    blocks, indices = permute(blocks)
    blocks, rf_values = apply_rotation_and_flipping(blocks)
    blocks, np_flags = apply_negative_positive(blocks)

    return merge_blocks(blocks, original_shape)


def encrypt_with_xor(blocks: np.ndarray, original_shape: Tuple[int, int]) -> np.ndarray:
    blocks, indices = permute(blocks)
    blocks, rf_values = apply_rotation_and_flipping(blocks)
    blocks, np_flags = apply_negative_positive(blocks)
    blocks, xor_keys = appy_intensity_modulation(blocks)

    return merge_blocks(blocks, original_shape)
