from PIL import Image
import numpy as np


def convert_and_stack_ycbcr(img: Image) -> np.ndarray:
    ycbcr_img = img.convert('YCbCr')

    y, cb, cr = ycbcr_img.split()

    y_np = np.array(y)
    cb_np = np.array(cb)
    cr_np = np.array(cr)

    stacked_img_np = np.hstack([y_np, cb_np, cr_np])

    return stacked_img_np


def restore_from_stacked_ycbcr(stacked_img_np: np.ndarray) -> Image:
    _, w3 = stacked_img_np.shape
    w = w3 // 3

    y_np = stacked_img_np[:, 0:w]
    cb_np = stacked_img_np[:, w:2*w]
    cr_np = stacked_img_np[:, 2*w:3*w]

    ycbcr_img_np = np.stack([y_np, cb_np, cr_np], axis=-1).astype(np.uint8)
    ycbcr_img = Image.fromarray(ycbcr_img_np, mode='YCbCr')
    img = ycbcr_img.convert('RGB')

    return img
