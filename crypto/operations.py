import numpy as np
from typing import Tuple
from crypto.helper import (
    TransformKeys,
    apply_intensity_modulation,
    undo_intensity_modulation,
    permute,
    undo_permute,
    apply_rotation_and_flipping,
    undo_rotation_and_flipping,
    apply_negative_positive,
    undo_negative_positive,
    merge_blocks,
)


def encrypt(blocks: np.ndarray, original_shape: Tuple[int, int]) -> np.ndarray:
    blocks, indices = permute(blocks)
    blocks, rf_values = apply_rotation_and_flipping(blocks)
    blocks, np_flags = apply_negative_positive(blocks)

    return merge_blocks(blocks, original_shape)


def encrypt_with_xor(blocks: np.ndarray, original_shape: Tuple[int, int]) -> Tuple[np.ndarray, TransformKeys]:
    blocks, xor_keys = apply_intensity_modulation(blocks)
    blocks, indices = permute(blocks)
    blocks, rf_values = apply_rotation_and_flipping(blocks)
    transformed_blocks, np_flags = apply_negative_positive(blocks)

    keys = TransformKeys(indices, rf_values, np_flags, xor_keys)
    return merge_blocks(transformed_blocks, original_shape), keys


def decrypt_with_xor(transformed_blocks: np.ndarray, original_shape: Tuple[int, int], keys: TransformKeys) -> np.ndarray:
    transformed_blocks = undo_negative_positive(
        transformed_blocks, keys.np_flags)
    transformed_blocks = undo_rotation_and_flipping(
        transformed_blocks, keys.rf_values)
    transformed_blocks = undo_permute(transformed_blocks, keys.indices)
    blocks = undo_intensity_modulation(transformed_blocks, keys.xor_keys)

    return merge_blocks(blocks, original_shape)
