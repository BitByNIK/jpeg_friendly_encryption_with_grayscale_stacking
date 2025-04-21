from evaluation.operations import compare_encryptions, plot_histograms, get_rate_distortion_curve, run_psnr_ssim_batch_evaluation
from graphic.utils import open_jpeg
from config import INPUT_DIR, ENCRYPTED_DIR, DECRYPTED_DIR

# Compare shannon entropy of encrypted images
encrypted_img_np_xor = open_jpeg(
    str(ENCRYPTED_DIR / "test_encrypted_15.jpg"), True)
encrypted_img_np_wxor = open_jpeg(
    str(ENCRYPTED_DIR / "test_encrypted_14.jpg"), True)
compare_encryptions(encrypted_img_np_xor, "With XOR",
                    encrypted_img_np_wxor, "Without XOR")

# Plot histograms of encrypted images
plot_histograms(encrypted_img_np_xor, encrypted_img_np_wxor)

# Get rate-distortion curve
get_rate_distortion_curve(encrypted_img_np_xor, encrypted_img_np_wxor)

# Run PSNR and SSIM evaluation on decrypted images
run_psnr_ssim_batch_evaluation(INPUT_DIR, DECRYPTED_DIR)
