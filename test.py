from evaluation.operations import (
    evaluate_entropy,
    plot_histogram_comparison,
    plot_psnr_vs_bpp,
    evaluate_social_media_psnr_table,
    plot_npcr_uaci,
    evaluate_block_adjacency
)
from config import INPUT_DIR, ENCRYPTED_DIR, DECRYPTED_DIR, UPLOADED_DIR, UPLOADED_DECRYPTED_DIR

evaluate_entropy(ENCRYPTED_DIR)
plot_histogram_comparison(str(ENCRYPTED_DIR / "image-1_encrypted_14_q95.jpg"),
                          str(ENCRYPTED_DIR / "image-1_encrypted_15_q95.jpg"))
plot_psnr_vs_bpp(INPUT_DIR, DECRYPTED_DIR)
print()
evaluate_social_media_psnr_table(
    UPLOADED_DIR, UPLOADED_DECRYPTED_DIR)
plot_npcr_uaci(INPUT_DIR, ENCRYPTED_DIR)
evaluate_block_adjacency(ENCRYPTED_DIR)
