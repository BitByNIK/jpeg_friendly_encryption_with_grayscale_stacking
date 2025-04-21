from graphic.operations import (
    pad_to_block_size,
    divide_into_blocks,
    merge_blocks
)
from graphic.utils import open_jpeg, save_jpeg
from graphic.io import convert_and_stack_ycbcr, restore_from_stacked_ycbcr
from crypto.operations import encrypt, decrypt

# -------- ENCRYPT --------
# Open RGB image
img = open_jpeg("test_input.jpg")

# Convert to stacked YCbCr format
stacked = convert_and_stack_ycbcr(img)

# Pad and divide into blocks
padded = pad_to_block_size(stacked)
blocks = divide_into_blocks(padded)

# Encrypt with all ops
encrypted_blocks, key = encrypt(blocks)

# Merge and save encrypted image
encrypted_img = merge_blocks(encrypted_blocks, stacked.shape)
save_jpeg("test_e.jpg", encrypted_img)

# -------- DECRYPT --------
# Reuse the encrypted image (fresh load)
encrypted = open_jpeg("test_e.jpg", as_array=True)

# Pad and divide into blocks
padded = pad_to_block_size(encrypted)
blocks = divide_into_blocks(padded)

# Decrypt using saved keys
decrypted_blocks = decrypt(blocks, key)

# Merge blocks and restore RGB
decrypted_img = restore_from_stacked_ycbcr(
    merge_blocks(decrypted_blocks, encrypted.shape))

# Save the final result
save_jpeg("test_d.jpg", decrypted_img)
