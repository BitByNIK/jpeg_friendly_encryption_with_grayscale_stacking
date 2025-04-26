from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def evaluate_entropy(folder: Path):
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

    return mode14_entropies, mode15_entropies


def plot_histogram_comparison(folder: Path):
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
