from PIL import Image
import numpy as np
from typing import Tuple
from graphic.helper import open_grayscale_image, convert_and_stack_ycbcr, restore_rgb_from_ycbcr, pad_image_to_block_size, divide_image_into_blocks


def preprocess_raw_img(input_image_path: str) -> Tuple[np.ndarray, Tuple[int, int]]:
    stacked_img_np, img_size = convert_and_stack_ycbcr(input_image_path)
    padded_img_np = pad_image_to_block_size(stacked_img_np)
    blocks = divide_image_into_blocks(padded_img_np)

    return blocks, img_size


def preprocess_grayscale_img(input_image_path: str) -> Tuple[np.ndarray, Tuple[int, int]]:
    img_np, img_size = open_grayscale_image(input_image_path)
    padded_img_np = pad_image_to_block_size(img_np)
    blocks = divide_image_into_blocks(padded_img_np)

    return blocks, img_size


def postprocess_grayscale_img(img_np: np.ndarray, output_image_path: str) -> Image:
    restore_rgb_from_ycbcr(img_np).save(
        output_image_path, format="JPEG", quality=95)
