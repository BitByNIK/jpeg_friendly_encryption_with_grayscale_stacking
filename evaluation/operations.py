from io import BytesIO
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import shannon_entropy
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def compare_encryptions(encrypted_a: np.ndarray, a_name: str, encrypted_b: np.ndarray, b_name: str) -> None:
    print(f"Comparing Encryption {a_name} vs {b_name}\n")

    print(f"Entropy {a_name}: {shannon_entropy(encrypted_a):.4f}")
    print(f"Entropy {b_name}: {shannon_entropy(encrypted_b):.4f}\n")


def plot_histograms(encrypted_a: np.ndarray, encrypted_b: np.ndarray) -> None:
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.hist(encrypted_a.ravel(), bins=256, color='gray', alpha=0.8)
    plt.title(
        f"Histogram: Encryption A \nEntropy: {shannon_entropy(encrypted_a):.4f} bits")
    plt.xlabel('Pixel value')
    plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    plt.hist(encrypted_b.ravel(), bins=256, color='blue', alpha=0.8)
    plt.title(
        f"Histogram: Encryption B \nEntropy: {shannon_entropy(encrypted_b):.4f} bits")
    plt.xlabel('Pixel value')

    plt.tight_layout()
    plt.show()


def get_rate_distortion_curve(encrypted_a: np.ndarray, encrypted_b: np.ndarray, qualities: list = [100, 90, 80, 70, 60, 50]) -> None:
    def get_sizes(img_array):
        sizes = []
        for q in qualities:
            img = Image.fromarray(img_array)
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=q)
            size_kb = len(buffer.getvalue()) / 1024
            sizes.append(size_kb)
        return sizes

    sizes_no_xor = get_sizes(encrypted_a)
    sizes_xor = get_sizes(encrypted_b)

    plt.figure(figsize=(8, 5))
    plt.plot(qualities, sizes_no_xor, marker='o',
             label='Encrypted Without XOR')
    plt.plot(qualities, sizes_xor, marker='x', label='Encrypted With XOR')
    plt.xlabel('JPEG Quality Factor')
    plt.ylabel('File Size (KB)')
    plt.title('Rate-Distortion Curve')
    plt.gca().invert_xaxis()
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def evaluate_psnr_ssim(original: np.ndarray, decrypted: np.ndarray):
    psnr = peak_signal_noise_ratio(original, decrypted, data_range=255)
    ssim = structural_similarity(original, decrypted, data_range=255)
    return psnr, ssim


def run_psnr_ssim_batch_evaluation(original_dir: Path, decrypted_dir: Path):
    psnr_total = 0.0
    ssim_total = 0.0
    count = 0

    for original_path in original_dir.glob("*.jpg"):
        name = original_path.stem
        decrypted_path = decrypted_dir / f"{name}_decrypted_15.jpg"

        if not decrypted_path.exists():
            print(f"Skipped: {name} — decrypted image not found.")
            continue

        orig_img = np.array(Image.open(original_path).convert("L"))
        decr_img = np.array(Image.open(decrypted_path).convert("L"))

        psnr, ssim = evaluate_psnr_ssim(orig_img, decr_img)
        print(f"{name}: PSNR = {psnr:.2f} dB, SSIM = {ssim:.4f}")

        psnr_total += psnr
        ssim_total += ssim
        count += 1

    if count > 0:
        print("\n--- AVERAGE ---")
        print(f"PSNR: {psnr_total / count:.2f} dB")
        print(f"SSIM: {ssim_total / count:.4f}")
    else:
        print("No images evaluated.")
