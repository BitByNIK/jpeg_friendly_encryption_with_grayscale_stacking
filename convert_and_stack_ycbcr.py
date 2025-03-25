from PIL import Image
import numpy as np


def convert_and_stack_ycbcr(input_image_path, output_image_path):
    img = Image.open(input_image_path).convert('RGB')
    img_ycbcr = img.convert('YCbCr')

    y, cb, cr = img_ycbcr.split()

    y_np = np.array(y)
    cb_np = np.array(cb)
    cr_np = np.array(cr)

    stacked_np = np.hstack([y_np, cb_np, cr_np])

    stacked_img = Image.fromarray(stacked_np.astype(np.uint8), mode='L')
    stacked_img.save(output_image_path)


convert_and_stack_ycbcr('test.jpg', 'test-1.jpg')
