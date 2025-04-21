from PIL import Image
import numpy as np
from typing import Union


def open_jpeg(path: str, as_array: bool = False) -> Union[Image.Image, np.ndarray]:
    img = Image.open(path)
    return np.array(img) if as_array else img.convert("RGB")


def save_jpeg(path: str, img: Union[Image.Image, np.ndarray]) -> None:
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img.astype(np.uint8)).convert("L")

    img.save(path, format="JPEG", quality=95)
