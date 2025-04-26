import argparse
from pathlib import Path
from typing import Any, Tuple
from crypto.operations import encrypt, decrypt, export_key_to_string, import_key_from_string
from graphic.utils import open_jpeg, save_jpeg
from graphic.io import convert_and_stack_ycbcr, restore_from_stacked_ycbcr
from graphic.operations import pad_to_block_size, divide_into_blocks, merge_blocks
from config import INPUT_DIR, ENCRYPTED_DIR, DECRYPTED_DIR


INPUT_DIR.mkdir(exist_ok=True)
ENCRYPTED_DIR.mkdir(exist_ok=True)
DECRYPTED_DIR.mkdir(exist_ok=True)


def get_output_path(input_path: Path, batch_dir: Path, operation_type: str, ops_flag: int, jpeg_quality: int, batch: bool = False) -> str:
    stem = input_path.stem

    if batch:
        if operation_type == "decrypted" and "_encrypted_" in stem:
            stem = stem.rsplit("_encrypted_", 1)[0]

        filename = f"{stem}_{operation_type}_{ops_flag}_q{jpeg_quality}.jpg"
        return str(batch_dir / filename)
    else:
        filename = input_path.name.replace("encrypted", "decrypted")
        return str(input_path.parent / filename)


def encrypt_image(path: Path, ops_flag: int, jpeg_quality: int, batch: bool = False) -> Tuple[Any, Path]:
    # -------- ENCRYPT --------
    img = open_jpeg(str(path))

    stacked = convert_and_stack_ycbcr(img)
    padded = pad_to_block_size(stacked)
    blocks = divide_into_blocks(padded)

    encrypted_blocks, key = encrypt(blocks, ops_flag)
    encrypted_img = merge_blocks(encrypted_blocks, stacked.shape)

    encrypted_img_path = get_output_path(
        path, ENCRYPTED_DIR, "encrypted", ops_flag, jpeg_quality, batch)
    save_jpeg(encrypted_img_path, encrypted_img, jpeg_quality)

    return key, Path(encrypted_img_path)


def decrypt_image(path: Path, ops_flag: int, key, jpeg_quality: int, batch: bool = False) -> None:
    # -------- DECRYPT --------
    encrypted_reloaded = open_jpeg(str(path), as_array=True)

    padded = pad_to_block_size(encrypted_reloaded)
    blocks = divide_into_blocks(padded)
    decrypted_blocks = decrypt(blocks, key)

    decrypted_img = restore_from_stacked_ycbcr(
        merge_blocks(decrypted_blocks, encrypted_reloaded.shape)
    )

    save_jpeg(get_output_path(path, DECRYPTED_DIR, "decrypted",
              ops_flag, jpeg_quality, batch), decrypted_img)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", nargs=1, metavar="IMAGE",
                        help="Encrypt a single image")
    parser.add_argument("-d", nargs=2, metavar=("IMAGE",
                        "KEY"), help="Decrypt a single image")
    parser.add_argument("-ops", type=int, default=15,
                        help="Operation bitmask for encryption")
    parser.add_argument("-jq", type=int, default=95,
                        help="JPEG compression quality")
    args = parser.parse_args()

    if args.e:
        path = Path(args.e[0])
        if not path.is_file():
            print(f"File {path} does not exist.")
            return

        key, _ = encrypt_image(path, args.ops, args.jq)

        key_path = path.with_name(f"{path.stem}_key.txt")
        key_path.write_text(export_key_to_string(key))

        print("Encryption complete. DO NOT LOSE THIS KEY FILE:")
        print(key_path)
        print("\nRequired to decrypt this image.")

    elif args.d:
        path = Path(args.d[0])
        key_path = Path(args.d[1])

        if not path.is_file():
            print(f"File {path} does not exist.")
            return
        if not key_path.is_file():
            print(f"Key file {key_path} does not exist.")
            return

        try:
            key_str = key_path.read_text().strip()
            key = import_key_from_string(key_str)
            decrypt_image(path, args.ops, key, args.jq)
        except Exception:
            print("Invalid decryption key.")

    else:
        for path in INPUT_DIR.glob("*.jpg"):
            key, temp_path = encrypt_image(path, args.ops, args.jq, batch=True)
            decrypt_image(temp_path, args.ops, key, args.jq, batch=True)


if __name__ == "__main__":
    main()
