import os
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr
from graphic.utils import open_jpeg


def evaluate_entropy(folder: Path) -> None:
    """Evaluate and compare Shannon entropy for mode 14 and mode 15 images."""

    def compute_entropy(img_path: Path) -> float:
        img = Image.open(img_path).convert("L")
        img_np = np.array(img)
        histogram, _ = np.histogram(
            img_np.flatten(), bins=256, range=(0, 255), density=True)
        histogram = histogram[histogram > 0]
        entropy = -np.sum(histogram * np.log2(histogram))
        return entropy

    img_paths = list(folder.glob("*.jpg"))

    mode14_entropies = []
    mode15_entropies = []

    for path in img_paths:
        if "_14" in path.stem:
            mode14_entropies.append(compute_entropy(path))
        elif "_15" in path.stem:
            mode15_entropies.append(compute_entropy(path))

    print(f"--- Entropy Evaluation ---")
    print(
        f"Without Adaptive XOR: Average Entropy = {np.mean(mode14_entropies):.4f} bits")
    print(
        f"With Adaptive XOR: Average Entropy = {np.mean(mode15_entropies):.4f} bits")


def plot_histogram_comparison(folder: Path) -> None:
    """Plot histogram comparison between without and with adaptive XOR."""

    img_paths = list(folder.glob("*.jpg"))

    mode14_path = next((p for p in img_paths if "_14" in p.stem), None)
    mode15_path = next((p for p in img_paths if "_15" in p.stem), None)

    if mode14_path is None or mode15_path is None:
        print("Error: Images for both modes not found.")
        return

    # Load images
    img14 = Image.open(mode14_path).convert("L")
    img15 = Image.open(mode15_path).convert("L")
    img14_np = np.array(img14)
    img15_np = np.array(img15)

    # Compute histograms
    hist14, _ = np.histogram(img14_np.flatten(), bins=256, range=(0, 255))
    hist15, _ = np.histogram(img15_np.flatten(), bins=256, range=(0, 255))

    max_y = max(hist14.max(), hist15.max())

    # Plot
    fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    axs[0].bar(np.arange(256), hist14, width=1.0)
    axs[0].set_title("Without Adaptive XOR")
    axs[0].set_xlabel("Pixel Intensity")
    axs[0].set_ylabel("Frequency")
    axs[0].set_ylim(0, max_y * 1.1)

    axs[1].bar(np.arange(256), hist15, width=1.0)
    axs[1].set_title("With Adaptive XOR")
    axs[1].set_xlabel("Pixel Intensity")
    axs[1].set_ylim(0, max_y * 1.1)

    plt.tight_layout()
    plt.show()


def plot_psnr_vs_bpp(input_dir: Path, decrypted_dir: Path) -> None:
    """
    Plot PSNR vs BPP curve between original images and decrypted images.
    """

    qualities = list(range(70, 96))  # JPEG qualities 70 to 95
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

            # decrypted file pattern
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

    # Plot
    plt.plot(bpp_list, psnr_list, marker='o')
    plt.xlabel('Bits Per Pixel (BPP)')
    plt.ylabel('PSNR (dB)')
    plt.title('Rate-Distortion (PSNR vs BPP)')
    plt.grid(True)
    plt.show()


def evaluate_social_media_psnr_table(input_dir: Path, uploaded_decrypted_dir: Path) -> None:
    qualities = list(range(70, 100, 5))  # JPEG qualities from 70 to 95
    results = []

    input_files = sorted(input_dir.glob("*.jpg"))

    for q in qualities:
        psnr_sum = 0
        count = 0

        for input_path in input_files:
            stem = input_path.stem
            uploaded_path = uploaded_decrypted_dir / \
                f"{stem}_decrypted_15_q{q}.jpg"

            if not uploaded_path.exists():
                continue

            original = np.array(open_jpeg(str(input_path)))
            uploaded = np.array(open_jpeg(str(uploaded_path)))

            # Crop to the minimum dimensions
            min_h = min(original.shape[0], uploaded.shape[0])
            min_w = min(original.shape[1], uploaded.shape[1])

            original = original[:min_h, :min_w]
            uploaded = uploaded[:min_h, :min_w]

            psnr_val = psnr(original, uploaded, data_range=255)
            psnr_sum += psnr_val
            count += 1

        avg_psnr = psnr_sum / count if count > 0 else 0
        results.append((q, avg_psnr))

    # Print the table
    print(f"{'JPEG Quality':<15}{'Average PSNR (dB)':<20}")
    print("-" * 35)
    for q, p in results:
        print(f"{q:<15}{p:<20.4f}")
