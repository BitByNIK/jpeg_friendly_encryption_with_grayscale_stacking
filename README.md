# JPEG Friendly Encryption with Grayscale Stacking

A grayscale-based image encryption system compatible with JPEG compression. Uses block-wise transformations on stacked YCbCr grayscale images for secure and reversible encryption.

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🚀 Working

1. Place `.jpg` images inside the `input_images/` folder.

2. Run the script with desired operation bits:

```bash
python main.py --ops <bitmask>
```

- Encrypted images will be saved in `encrypted_images/`
- Decrypted images will be saved in `decrypted_images/`

## 🔢 Operation Bitmask

| Bit | Operation             |
| --- | --------------------- |
| 1   | XOR                   |
| 2   | Permutation           |
| 4   | Rotation and Flipping |
| 8   | Negative-Positive     |

Use any combination (e.g., `--ops 15` for all).
