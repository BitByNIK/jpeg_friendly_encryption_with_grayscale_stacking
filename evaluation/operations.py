from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import shannon_entropy


def compare_encryptions(encrypted_a: np.ndarray, encrypted_b: np.ndarray) -> None:
    print("📊 Comparing Encryption A vs B\n")

    print(f"Entropy A: {shannon_entropy(encrypted_a):.4f}")
    print(f"Entropy B: {shannon_entropy(encrypted_b):.4f}")


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
