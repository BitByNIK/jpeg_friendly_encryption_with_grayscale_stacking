from PIL import Image
import numpy as np
from config import OUTPUT_IMAGE_PATH


def generate_jpeg_image(img_np):
    Image.fromarray(img_np.astype(np.uint8), mode='L').save(
        OUTPUT_IMAGE_PATH, format="JPEG", quality=95)
