import base64
import pickle
import numpy as np
from crypto.transforms import (
    apply_intensity_modulation,
    undo_intensity_modulation,
    permute,
    undo_permute,
    apply_rotation_and_flipping,
    undo_rotation_and_flipping,
    apply_negative_positive,
    undo_negative_positive,
)
from crypto.keys import TransformKeys


def encrypt(blocks: np.ndarray, ops_flag: bool = 0b1111) -> np.ndarray:
    xor_keys = indices = rf_values = np_flags = None
    temp = blocks

    if ops_flag & 0b0001:
        temp, xor_keys = apply_intensity_modulation(temp)
    if ops_flag & 0b0010:
        temp, indices = permute(temp)
    if ops_flag & 0b0100:
        temp, rf_values = apply_rotation_and_flipping(temp)
    if ops_flag & 0b1000:
        temp, np_flags = apply_negative_positive(temp)

    keys = TransformKeys(
        xor_keys=xor_keys,
        indices=indices,
        rf_values=rf_values,
        np_flags=np_flags
    )

    return temp, keys


def decrypt(transformed_blocks: np.ndarray, keys: TransformKeys) -> np.ndarray:
    temp = transformed_blocks

    if keys.np_flags is not None:
        temp = undo_negative_positive(temp, keys.np_flags)
    if keys.rf_values is not None:
        temp = undo_rotation_and_flipping(temp, keys.rf_values)
    if keys.indices is not None:
        temp = undo_permute(temp, keys.indices)
    if keys.xor_keys is not None:
        temp = undo_intensity_modulation(temp, keys.xor_keys)

    return temp


def export_key_to_string(key_obj) -> str:
    return base64.b64encode(pickle.dumps(key_obj)).decode("utf-8")


def import_key_from_string(key_str: str):
    return pickle.loads(base64.b64decode(key_str.encode("utf-8")))
