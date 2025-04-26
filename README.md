# JPEG Friendly Encryption with Grayscale Stacking

A grayscale-based image encryption system compatible with JPEG compression.  
Uses block-wise transformations on stacked YCbCr grayscale images for secure and reversible encryption.

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## 🚀 Working

### 🔒 Encrypt / Decrypt a Single Image

Use the `-e` or `-d` flags:

#### ▶️ Encrypt

```bash
python main.py -e path/to/image.jpg
```

- Encrypted image will be saved **next to the input image**.
- A key file (`.txt`) will also be saved alongside the image.

#### 🔓 Decrypt

```bash
python main.py -d path/to/encrypted_image.jpg path/to/key_file.txt
```

- Decrypted image will be saved **next to the encrypted image**.

---

### 📁 Batch Mode (No Flags)

To encrypt and decrypt **all** `.jpg` images in `input_images/`:

```bash
python main.py
```

- Encrypted images are saved in `encrypted_images/`
- Decrypted images are saved in `decrypted_images/`

---

## ⚙️ Common Options (Encryption Only)

These flags can be used with encryption (`-e` or batch mode):

### 🔢 Operation Bitmask (`-ops`)

Specify which transformations to apply:

```bash
-ops <bitmask>
```

If not provided, the default is `15` (apply all operations).

| Bit | Operation             |
| --- | --------------------- |
| 1   | Adaptive XOR          |
| 2   | Permutation           |
| 4   | Rotation and Flipping |
| 8   | Negative-Positive     |

Examples:

- `-ops 3` → XOR + Permutation
- `-ops 15` → All operations

### 🖼️ JPEG Compression Quality (`-jq`)

Set JPEG compression quality after encryption:

```bash
-jq <quality>
```

- Default is `95`.
- Controls the output quality of encrypted JPEGs.

Examples:

- `-jq 85` → Save encrypted images at quality 85
- `-jq 100` → Save encrypted images at maximum quality

---

## 📁 Directory Structure

| Folder              | Used In    | Description                        |
| ------------------- | ---------- | ---------------------------------- |
| `input_images/`     | Batch mode | Source images for batch encryption |
| `encrypted_images/` | Batch mode | Output of encrypted images         |
| `decrypted_images/` | Batch mode | Output of decrypted images         |

> 🔐 In `-e` / `-d` mode, files are saved next to the input image instead.

---

## ⚠️ Notes

- The key file is **essential** — without it, decryption is not possible.
- Do **not resize or modify** encrypted images before decryption — block structure matters.
- `-ops` and `-jq` only affect encryption, not decryption.
- You can combine `-ops` and `-jq` freely during encryption.

---

## 🛠️ Example Commands

Encrypt a single image with custom settings:

```bash
python main.py -e path/to/image.jpg -ops 7 -jq 90
```

Batch encrypt all images with maximum JPEG quality:

```bash
python main.py -ops 15 -jq 100
```

Decrypt a single encrypted image:

```bash
python main.py -d path/to/encrypted_image.jpg path/to/key_file.txt
```
