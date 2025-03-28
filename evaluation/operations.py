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
