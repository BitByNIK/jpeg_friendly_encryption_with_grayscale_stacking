from crypto.operations import encrypt
from graphic.operations import preprocess
from graphic.utils import generate_jpeg_image
from config import INPUT_IMAGE_PATH, ENCRYPTED_IMAGE_PATH

blocks, img_size = preprocess(INPUT_IMAGE_PATH)
encrypted_image_np = encrypt(blocks, img_size)
generate_jpeg_image(encrypted_image_np, ENCRYPTED_IMAGE_PATH)
