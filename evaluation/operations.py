import os
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import shannon_entropy
from skimage.metrics import peak_signal_noise_ratio as psnr
from graphic.utils import open_jpeg


def evaluate_entropy(folder: Path, mode1: int = 14, mode2: int = 15) -> None:
    """Compare Shannon entropy between two modes."""

    def compute_entropy(img_path: Path) -> float:
        img = Image.open(img_path).convert("L")
        img_np = np.array(img)
        return shannon_entropy(img_np)

    img_paths = list(folder.glob("*.jpg"))

    mode1_entropies = []
    mode2_entropies = []

    for path in img_paths:
        if f"_{mode1}" in path.stem:
            mode1_entropies.append(compute_entropy(path))
        elif f"_{mode2}" in path.stem:
            mode2_entropies.append(compute_entropy(path))

    print(f"--- Shannon Entropy Evaluation ---")
    print(
        f"Mode {mode1} Without XOR: Average Entropy = {np.mean(mode1_entropies):.4f} bits")
    print(
        f"Mode {mode2} With XOR: Average Entropy = {np.mean(mode2_entropies):.4f} bits")


def plot_histogram_comparison(img1_path: Path, img2_path: Path) -> None:
    """Plot histogram comparison between two images."""

    img1 = Image.open(img1_path).convert("L")
    img2 = Image.open(img2_path).convert("L")

    img1_np = np.array(img1)
    img2_np = np.array(img2)

    hist1, _ = np.histogram(img1_np.flatten(), bins=256, range=(0, 255))
    hist2, _ = np.histogram(img2_np.flatten(), bins=256, range=(0, 255))

    max_y = max(hist1.max(), hist2.max())

    fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    axs[0].bar(np.arange(256), hist1, width=1.0)
    axs[0].set_title("Without XOR")
    axs[0].set_xlabel("Pixel Intensity")
    axs[0].set_ylabel("Frequency")
    axs[0].set_ylim(0, max_y * 1.1)

    axs[1].bar(np.arange(256), hist2, width=1.0)
    axs[1].set_title("With XOR")
    axs[1].set_xlabel("Pixel Intensity")
    axs[1].set_ylim(0, max_y * 1.1)

    plt.tight_layout()
    plt.show()


def plot_psnr_vs_bpp(input_dir: Path, decrypted_dir: Path) -> None:
    """Plot PSNR vs BPP curve between input images and decrypted images."""

    qualities = list(range(70, 100, 5))
    bpp_list = []
    psnr_list = []

    input_files = sorted(input_dir.glob("*.jpg"))

    for q in qualities:
        total_psnr = 0
        total_bpp = 0
        count = 0

        for input_img_path in input_files:
            filename = input_img_path.stem
            original = np.array(open_jpeg(str(input_img_path)))

            decrypted_img_path = decrypted_dir / \
                f"{filename}_decrypted_15_q{q}.jpg"
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
    plt.title('Rate-Distortion (PSNR vs BPP)')
    plt.grid(True)
    plt.show()


def evaluate_social_media_psnr_table(input_dir: Path, decrypted_dir: Path) -> None:
    """Print PSNR table for images uploaded and downloaded from social media."""

    qualities = list(range(70, 100, 5))
    results = []

    input_files = sorted(input_dir.glob("*.jpg"))

    for q in qualities:
        psnr_sum = 0
        count = 0

        for input_path in input_files:
            stem = input_path.stem
            uploaded_path = decrypted_dir / f"{stem}_decrypted_15_q{q}.jpg"

            if not uploaded_path.exists():
                continue

            original = np.array(open_jpeg(str(input_path)))
            uploaded = np.array(open_jpeg(str(uploaded_path)))

            min_h = min(original.shape[0], uploaded.shape[0])
            min_w = min(original.shape[1], uploaded.shape[1])

            original = original[:min_h, :min_w]
            uploaded = uploaded[:min_h, :min_w]

            psnr_val = psnr(original, uploaded, data_range=255)
            psnr_sum += psnr_val
            count += 1

        avg_psnr = psnr_sum / count if count > 0 else 0
        results.append((q, avg_psnr))

    print(f"{'JPEG Quality':<15}{'Average PSNR (dB)':<20}")
    print("-" * 35)
    for q, p in results:
        print(f"{q:<15}{p:<20.4f}")
