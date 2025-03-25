from PIL import Image
import numpy as np


def convert_and_stack_ycbcr(input_image_path):
    img = Image.open(input_image_path).convert('RGB')
    img_ycbcr = img.convert('YCbCr')

    y, cb, cr = img_ycbcr.split()

    y_np = np.array(y)
    cb_np = np.array(cb)
    cr_np = np.array(cr)

    stacked_np = np.hstack([y_np, cb_np, cr_np])

    return stacked_np


def pad_image_to_block_size(img_np, block_size=100):
    h, w = img_np.shape
    pad_h = (block_size - h % block_size) % block_size
    pad_w = (block_size - w % block_size) % block_size

    padded_img = np.pad(img_np, ((0, pad_h), (0, pad_w)), mode='edge')

    return padded_img


def divide_image_into_blocks(img_np, block_size=8):
    h, w = img_np.shape
    blocks = (img_np.reshape(h // block_size, block_size, w // block_size, block_size)
              .swapaxes(1, 2)
              .reshape(-1, block_size, block_size))

    return blocks


final_img = Image.fromarray(pad_image_to_block_size(
    convert_and_stack_ycbcr('test.jpg')).astype(np.uint8), mode='L')
final_img.save('test-n.jpg')
