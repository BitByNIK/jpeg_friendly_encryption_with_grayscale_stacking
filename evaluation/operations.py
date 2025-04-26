import os
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import shannon_entropy
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim
from graphic.utils import open_jpeg
from config import BLOCK_SIZE


def evaluate_entropy(folder: Path, mode1: int = 14, mode2: int = 15) -> None:
    """Compare Shannon entropy between two encryption modes."""
    def compute_entropy(img_path: Path) -> float:
        img = Image.open(img_path).convert("L")
        img_np = np.array(img)
        return shannon_entropy(img_np)

    img_paths = list(folder.glob("*.jpg"))
    mode1_entropies, mode2_entropies = [], []

    for path in img_paths:
        if f"_{mode1}" in path.stem:
            mode1_entropies.append(compute_entropy(path))
        elif f"_{mode2}" in path.stem:
            mode2_entropies.append(compute_entropy(path))

    print("--- Shannon Entropy Evaluation ---")
    print(
        f"Mode {mode1} (Without XOR): Average Entropy = {np.mean(mode1_entropies):.4f} bits")
    print(
        f"Mode {mode2} (With XOR)   : Average Entropy = {np.mean(mode2_entropies):.4f} bits")


def plot_histogram_comparison(img1_path: Path, img2_path: Path) -> None:
    """Plot histogram comparison between two grayscale images."""
    img1 = np.array(Image.open(img1_path).convert("L"))
    img2 = np.array(Image.open(img2_path).convert("L"))

    hist1, _ = np.histogram(img1.flatten(), bins=256, range=(0, 255))
    hist2, _ = np.histogram(img2.flatten(), bins=256, range=(0, 255))
    max_y = max(hist1.max(), hist2.max())

    fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    axs[0].bar(np.arange(256), hist1, width=1.0, color='gray')
    axs[0].set_title("Without XOR")
    axs[0].set_xlabel("Pixel Intensity")
    axs[0].set_ylabel("Frequency")
    axs[0].set_ylim(0, max_y * 1.1)

    axs[1].bar(np.arange(256), hist2, width=1.0, color='blue')
    axs[1].set_title("With XOR")
    axs[1].set_xlabel("Pixel Intensity")
    axs[1].set_ylim(0, max_y * 1.1)

    plt.tight_layout()
    plt.show()


def plot_psnr_vs_bpp(input_dir: Path, decrypted_dir: Path, mode: int = 15) -> None:
    """Plot PSNR vs BPP curve for a range of JPEG qualities."""
    qualities = list(range(70, 100, 5))
    bpp_list, psnr_list = [], []

    input_files = sorted(input_dir.glob("*.jpg"))

    for q in qualities:
        total_psnr, total_bpp, count = 0, 0, 0

        for input_img_path in input_files:
            filename = input_img_path.stem
            original = np.array(open_jpeg(str(input_img_path)))

            decrypted_img_path = decrypted_dir / \
                f"{filename}_decrypted_{mode}_q{q}.jpg"
            if not decrypted_img_path.exists():
                continue

            decrypted = np.array(open_jpeg(str(decrypted_img_path)))
            psnr_val = psnr(original, decrypted, data_range=255)
            size_bits = os.path.getsize(decrypted_img_path) * 8
            num_pixels = original.shape[0] * original.shape[1]
            bpp_val = size_bits / num_pixels

            total_psnr += psnr_val
            total_bpp += bpp_val
            count += 1

        if count > 0:
            bpp_list.append(total_bpp / count)
            psnr_list.append(total_psnr / count)

    plt.plot(bpp_list, psnr_list, marker='o')
    plt.xlabel('Bits Per Pixel (BPP)')
    plt.ylabel('PSNR (dB)')
    plt.title('Rate-Distortion Curve (PSNR vs BPP)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def evaluate_social_media_psnr_table(input_dir: Path, decrypted_dir: Path, mode: int = 15) -> None:
    """Print PSNR table for JPEG re-compressed images (e.g., social media downloads)."""
    qualities = list(range(70, 100, 5))
    input_files = sorted(input_dir.glob("*.jpg"))

    print(f"{'JPEG Quality':<15}{'Average PSNR (dB)':<20}")
    print("-" * 35)

    for q in qualities:
        psnr_sum, count = 0, 0

        for input_path in input_files:
            stem = input_path.stem
            downloaded_path = decrypted_dir / \
                f"{stem}_decrypted_{mode}_q{q}.jpg"

            if not downloaded_path.exists():
                continue

            original = np.array(open_jpeg(str(input_path)))
            downloaded = np.array(open_jpeg(str(downloaded_path)))

            min_h = min(original.shape[0], downloaded.shape[0])
            min_w = min(original.shape[1], downloaded.shape[1])

            original = original[:min_h, :min_w]
            downloaded = downloaded[:min_h, :min_w]

            psnr_val = psnr(original, downloaded, data_range=255)
            psnr_sum += psnr_val
            count += 1

        avg_psnr = psnr_sum / count if count else 0
        print(f"{q:<15}{avg_psnr:<20.4f}")


def plot_npcr_uaci(input_dir: Path, encrypted_dir: Path) -> None:
    """Plot mean NPCR and UACI comparison between basic and XOR modes."""
    npcr_basic_list, uaci_basic_list = [], []
    npcr_xor_list, uaci_xor_list = [], []

    for path in encrypted_dir.glob('*_14_q95.jpg'):
        base = path.stem.replace('_encrypted_14_q95', '')
        original = open_jpeg(str(input_dir / f"{base}.jpg"), as_array=True)
        enc_basic = open_jpeg(str(path), as_array=True)
        enc_xor = open_jpeg(
            str(encrypted_dir / f"{base}_encrypted_15_q95.jpg"), as_array=True)

        def extract_y_channel(stacked_image: np.ndarray) -> np.ndarray:
            """Extract Y (luma) channel from horizontally stacked grayscale YCbCr image."""
            return stacked_image[:, :stacked_image.shape[1] // 3]

        enc_basic_y = extract_y_channel(enc_basic)
        enc_xor_y = extract_y_channel(enc_xor)

        if original.shape != enc_basic_y.shape:
            enc_basic_y = np.array(Image.fromarray(enc_basic_y).resize(
                (original.shape[1], original.shape[0])))
        if original.shape != enc_xor_y.shape:
            enc_xor_y = np.array(Image.fromarray(enc_xor_y).resize(
                (original.shape[1], original.shape[0])))

        diff_basic = original != enc_basic_y
        diff_xor = original != enc_xor_y

        npcr_basic = np.sum(diff_basic) / diff_basic.size * 100
        uaci_basic = np.mean(np.abs(original.astype(
            np.int8) - enc_basic_y.astype(np.int8))) / 255 * 100

        npcr_xor = np.sum(diff_xor) / diff_xor.size * 100
        uaci_xor = np.mean(np.abs(original.astype(
            np.int8) - enc_xor_y.astype(np.int8))) / 255 * 100

        npcr_basic_list.append(npcr_basic)
        uaci_basic_list.append(uaci_basic)
        npcr_xor_list.append(npcr_xor)
        uaci_xor_list.append(uaci_xor)

    mean_npcr_basic = np.mean(npcr_basic_list)
    mean_uaci_basic = np.mean(uaci_basic_list)
    mean_npcr_xor = np.mean(npcr_xor_list)
    mean_uaci_xor = np.mean(uaci_xor_list)

    labels = ['NPCR', 'UACI']
    basic = [mean_npcr_basic, mean_uaci_basic]
    xor = [mean_npcr_xor, mean_uaci_xor]

    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(8, 6))
    bars1 = plt.bar(x - width/2, basic, width, label='Basic ETC')
    bars2 = plt.bar(x + width/2, xor, width, label='ETC + XOR')

    for bar in bars1 + bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height - 5, f'{height:.2f}%',
                 ha='center', va='top', color='white', fontweight='bold', fontsize=10)

    plt.xticks(x, labels)
    plt.ylabel('Percentage (%)')
    plt.title('Mean NPCR and UACI Comparison')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    plt.show()


def evaluate_block_adjacency(encrypted_dir: Path) -> None:
    """Evaluate and print mean block adjacency scores for basic and XOR modes."""
    block_basic, block_xor = [], []

    for path in encrypted_dir.glob('*_14_q95.jpg'):
        base = path.stem.replace('_encrypted_14_q95', '')
        enc_basic = open_jpeg(str(path), as_array=True)
        enc_xor = open_jpeg(
            str(encrypted_dir / f"{base}_encrypted_15_q95.jpg"), as_array=True)

        scores_basic, scores_xor = [], []

        for img, scores in [(enc_basic, scores_basic), (enc_xor, scores_xor)]:
            h, w = img.shape
            for i in range(0, h - BLOCK_SIZE, BLOCK_SIZE):
                for j in range(0, w - BLOCK_SIZE, BLOCK_SIZE):
                    block = img[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE]
                    right = img[i:i+BLOCK_SIZE, j+BLOCK_SIZE:j+2 *
                                BLOCK_SIZE] if j + 2*BLOCK_SIZE <= w else None
                    down = img[i+BLOCK_SIZE:i+2*BLOCK_SIZE, j:j +
                               BLOCK_SIZE] if i + 2*BLOCK_SIZE <= h else None
                    if right is not None:
                        scores.append(ssim(block, right))
                    if down is not None:
                        scores.append(ssim(block, down))

        block_basic.append(np.mean(scores_basic))
        block_xor.append(np.mean(scores_xor))

    print(f"Mean Block Adjacency Score Basic: {np.mean(block_basic):.6f}")
    print(f"Mean Block Adjacency Score XOR  : {np.mean(block_xor):.6f}")
