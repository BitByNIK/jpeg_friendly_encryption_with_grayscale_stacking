from crypto.operations import encrypt, encrypt_with_xor, decrypt_with_xor
from graphic.operations import preprocess_raw_img, preprocess_grayscale_img, postprocess_grayscale_img
from graphic.utils import generate_jpeg_image
from evaluation.operations import compare_encryptions, plot_histograms, get_rate_distortion_curve
from config import INPUT_IMAGE_PATH

blocks, img_size = preprocess_raw_img(INPUT_IMAGE_PATH)

# encrypted_image_np = encrypt(blocks, img_size)
# generate_jpeg_image(encrypted_image_np, "test_e.jpg")

encrypted_image_with_xor_np, keys = encrypt_with_xor(blocks, img_size)
generate_jpeg_image(encrypted_image_with_xor_np, "test_e_xor.jpg")

transformed_blocks, encrypted_img_size = preprocess_grayscale_img(
    'test_e_xor.jpg')
decrypted_image_with_xor_np = decrypt_with_xor(
    transformed_blocks, encrypted_img_size, keys)
postprocess_grayscale_img(decrypted_image_with_xor_np, "test_d_xor.jpg")

# get_rate_distortion_curve(encrypted_image_np, encrypted_image_with_xor_np)
