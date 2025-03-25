from crypto.operations import encrypt
from graphic.operations import preprocess
from graphic.utils import generate_jpeg_image

blocks, img_size = preprocess()
encrypted_image_np = encrypt(blocks, img_size)
generate_jpeg_image(encrypted_image_np)
