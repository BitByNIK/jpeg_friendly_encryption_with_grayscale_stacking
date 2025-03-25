from PIL import Image
import numpy as np
from config import BLOCK_SIZE


def convert_and_stack_ycbcr(input_image_path):
    img = Image.open(input_image_path).convert('RGB')
    img_ycbcr = img.convert('YCbCr')

    y, cb, cr = img_ycbcr.split()

    y_np = np.array(y)
    cb_np = np.array(cb)
    cr_np = np.array(cr)

    stacked_np = np.hstack([y_np, cb_np, cr_np])

    return stacked_np, img.size


def pad_image_to_block_size(img_np):
    h, w = img_np.shape
    pad_h = (BLOCK_SIZE - h % BLOCK_SIZE) % BLOCK_SIZE
    pad_w = (BLOCK_SIZE - w % BLOCK_SIZE) % BLOCK_SIZE

    padded_img = np.pad(img_np, ((0, pad_h), (0, pad_w)), mode='edge')

    return padded_img


def divide_image_into_blocks(img_np):
    h, w = img_np.shape
    blocks = (img_np.reshape(h // BLOCK_SIZE, BLOCK_SIZE, w // BLOCK_SIZE, BLOCK_SIZE)
              .swapaxes(1, 2)
              .reshape(-1, BLOCK_SIZE, BLOCK_SIZE))

    return blocks
