import numpy as np
from typing import Tuple
from config import INPUT_IMAGE_PATH
from graphic.helper import convert_and_stack_ycbcr, pad_image_to_block_size, divide_image_into_blocks


def preprocess() -> Tuple[np.ndarray, Tuple[int, int]]:
    stacked_img_np, img_size = convert_and_stack_ycbcr(INPUT_IMAGE_PATH)
    padded_img_np = pad_image_to_block_size(stacked_img_np)
    blocks = divide_image_into_blocks(padded_img_np)

    return blocks, img_size
