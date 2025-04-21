import os
import argparse
from pathlib import Path
from crypto.operations import encrypt, decrypt
from graphic.utils import open_jpeg, save_jpeg
from graphic.io import convert_and_stack_ycbcr, restore_from_stacked_ycbcr
from graphic.operations import pad_to_block_size, divide_into_blocks, merge_blocks
from config import INPUT_DIR, ENCRYPTED_DIR, DECRYPTED_DIR


INPUT_DIR.mkdir(exist_ok=True)
ENCRYPTED_DIR.mkdir(exist_ok=True)
DECRYPTED_DIR.mkdir(exist_ok=True)


def process_image(path: Path, ops_flag: int) -> None:
    name = path.stem

    # -------- ENCRYPT --------
    img = open_jpeg(str(path))
    stacked = convert_and_stack_ycbcr(img)
    padded = pad_to_block_size(stacked)
    blocks = divide_into_blocks(padded)

    encrypted_blocks, key = encrypt(blocks, ops_flag)
    encrypted_img = merge_blocks(encrypted_blocks, stacked.shape)
    encrypted_name = f"{name}_encrypted_{ops_flag}.jpg"
    save_jpeg(str(ENCRYPTED_DIR / encrypted_name), encrypted_img)

    # -------- DECRYPT --------
    encrypted_reloaded = open_jpeg(
        str(ENCRYPTED_DIR / encrypted_name), as_array=True)
    padded = pad_to_block_size(encrypted_reloaded)
    blocks = divide_into_blocks(padded)
    decrypted_blocks = decrypt(blocks, key)
    decrypted_img = restore_from_stacked_ycbcr(
        merge_blocks(decrypted_blocks, encrypted_img.shape)
    )

    decrypted_name = f"{name}_decrypted_{ops_flag}.jpg"
    save_jpeg(str(DECRYPTED_DIR / decrypted_name), decrypted_img)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ops", type=int, default=15,
                        help="Ops bitmask (e.g. 15, 7, etc.)")
    args = parser.parse_args()

    ops_flag = args.ops

    for path in INPUT_DIR.glob("*.jpg"):
        process_image(path, ops_flag)


if __name__ == "__main__":
    main()
