from dataclasses import dataclass


@dataclass
class TransformKeys:
    indices: list
    rf_values: list
    np_flags: list
    xor_keys: list
