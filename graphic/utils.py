from PIL import Image
import numpy as np


def generate_jpeg_image(img_np: np.ndarray, output_image_path):
    Image.fromarray(img_np.astype(np.uint8), mode='L').save(
        output_image_path, format="JPEG", quality=95)
