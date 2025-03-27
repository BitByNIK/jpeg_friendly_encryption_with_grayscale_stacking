import numpy as np
from skimage.measure import shannon_entropy


def compare_encryptions(encrypted_a: np.ndarray, encrypted_b: np.ndarray) -> None:
    print("📊 Comparing Encryption A vs B\n")

    print(f"Entropy A: {shannon_entropy(encrypted_a):.4f}")
    print(f"Entropy B: {shannon_entropy(encrypted_b):.4f}")
