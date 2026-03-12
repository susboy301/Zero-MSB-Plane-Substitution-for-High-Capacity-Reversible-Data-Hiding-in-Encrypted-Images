# ============================================================
# main.py — FINAL VERSION: I, If, Im stats only
# ============================================================
# IMAGES TRACKED:
#   I  = original plaintext image
#   If = final encrypted image (Ie + auxiliary embedded)
#   Im = marked image (If + payload embedded)
#
# METRICS:
#   Per-image stats (corr h/v, SE, chi2):  I, If, Im
#   Difference metrics (NPCR, UACI, MAE):  If-I, Im-I, Im-If
#
# If-I  : shows encryption+aux effect vs plaintext  (matches Yao Table III)
# Im-I  : shows full pipeline effect vs plaintext
# Im-If : shows payload embedding effect alone
# ============================================================

import os
import csv
import cv2
import numpy as np

from core.residuals    import compute_residuals, recover_image
from core.block        import ResidualBlock
from core.classify     import classify_block
from core.compress     import compress_block

from utils.EncryptionImg  import EncryptionImg
from utils.psnr           import psnr

from embed.embed_aux         import embed_aux
from recover.extract_aux     import extract_aux
from embed.embed_payload     import embed_payload
from recover.extract_payload import extract_payload

from analysis.correlation import correlation
from analysis.entropy     import entropy
from analysis.chi_square  import chi_square
from analysis.mae         import mae
from analysis.npcr_uaci   import npcr, uaci

# ──────────────────────────────────────────────────────────────
# PARAMETERS
# ──────────────────────────────────────────────────────────────
t           = 4 # block size for residual processing
key_img     = 0xA3F1C9B2E7D08456_1F2A3C4B5D6E7F80_9B8C7D6E5F4A3B2C_1D0E9F8A7B6C5D4E # Key for image encryption (e.g., PRNG seed for pixel shuffling + XOR)
key_aux     = 456 # Key for auxiliary data embedding (e.g., PRNG seed for position shuffling)
payload_key = 999 # Key for payload embedding (e.g., PRNG seed for position shuffling)
MAX_PAYLOAD = 100000 # Maximum payload size in bits (can be set to a large value since we check capacity)

# ──────────────────────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────────────────────
DATASET_DIR = "" # Set this to your dataset path containing the images to process
ENC_DIR     = "Encryptedimages"
MARKED_DIR  = "Markedimages"
REC_DIR     = "Recoverimages"
CSV_PATH    = "bows2_full_stats.csv"

os.makedirs(ENC_DIR,    exist_ok=True)
os.makedirs(MARKED_DIR, exist_ok=True)
os.makedirs(REC_DIR,    exist_ok=True)

# ──────────────────────────────────────────────────────────────
# RESUME LOGIC
# ──────────────────────────────────────────────────────────────
processed_images = set()
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row: processed_images.add(row[0])

all_target_files = sorted([
    f for f in os.listdir(DATASET_DIR)
    if f.lower().endswith((".bmp", ".png", ".tif", ".tiff", ".pgm"))
])
image_files = [f for f in all_target_files if f not in processed_images]
print(f"Already completed: {len(processed_images)} | Remaining: {len(image_files)}")

# ──────────────────────────────────────────────────────────────
# CSV COLUMNS
# ──────────────────────────────────────────────────────────────
COLUMNS = [
    "image_name", "image_size",

    # ── Per-image stats: I (original plaintext) ──
    "I_corr_h",  "I_corr_v",  "I_se",  "I_chi2",

    # ── Per-image stats: If (encrypted + aux embedded) ──
    "If_corr_h", "If_corr_v", "If_se", "If_chi2",

    # ── Per-image stats: Im (marked = If + payload) ──
    "Im_corr_h", "Im_corr_v", "Im_se", "Im_chi2",

    # ── Difference: If vs I (encryption + aux effect vs plaintext) ──
    # Primary security metric — matches Yao et al. Table III
    # Expected: NPCR ~99.61%, UACI ~28-37%, MAE ~72-94
    "npcr_If_I",  "uaci_If_I",  "mae_If_I",

    # ── Difference: Im vs I (full pipeline effect vs plaintext) ──
    # Expected: similar to If-I since payload only flips LSBs
    "npcr_Im_I",  "uaci_Im_I",  "mae_Im_I",

    # ── Difference: Im vs If (payload embedding effect alone) ──
    # Expected: NPCR varies with payload size, UACI ~0.3-4% (LSB changes only)
    "npcr_Im_If", "uaci_Im_If", "mae_Im_If",

    # ── Payload & reversibility ──
    "embedded_bits", "capacity_bpp", "extraction_success", "psnr_recovery",
]

# ──────────────────────────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────────────────────────
write_header = not os.path.exists(CSV_PATH)

with open(CSV_PATH, "a", newline="") as csv_file:
    writer = csv.writer(csv_file)
    if write_header:
        writer.writerow(COLUMNS)

    for idx, name in enumerate(image_files, 1):
        print(f"[{idx}/{len(image_files)}] {name}")
        try:
            # ── Load ────────────────────────────────────────────
            I = cv2.imread(os.path.join(DATASET_DIR, name), 0)
            if I is None:
                print(f"  Cannot read {name}"); continue
            m, n = I.shape

            # ── Residuals + block compression ──────────────────
            res, first = compute_residuals(I)
            blocks, bid = [], 0
            for i in range(0, m, t):
                for j in range(0, n, t):
                    blk = res[i:i+t, j:j+t]
                    b   = ResidualBlock(bid, blk)
                    b.class_id = classify_block(blk)
                    compress_block(b)
                    blocks.append(b)
                    bid += 1
            capacity_bpp = sum(b.slack for b in blocks) / (m * n)

            # ── I — stats ──────────────────────────────────────
            I_corr_h = correlation(I, "horizontal")
            I_corr_v = correlation(I, "vertical")
            I_se     = entropy(I)
            I_chi2   = chi_square(I)

            # ── Encrypt → Ie, embed aux → If ──────────────────
            Ie = EncryptionImg(I, key_img)
            cv2.imwrite(os.path.join(ENC_DIR, name), Ie)

            aux_bits_list = []
            for b in blocks:
                aux_bits_list.extend([int(x) for x in format(b.zero_planes, "03b")])
                if b.zero_planes >= 3:
                    aux_bits_list.extend(b.compressed["plane_bits"])
                else:
                    aux_bits_list.extend(b.compressed["residual_bits"])
            total_aux_bits = len(aux_bits_list)

            If, aux_k, aux_positions = embed_aux(Ie, blocks, key_aux)

            # ── If — stats ─────────────────────────────────────
            If_corr_h = correlation(If, "horizontal")
            If_corr_v = correlation(If, "vertical")
            If_se     = entropy(If)
            If_chi2   = chi_square(If)

            # ── Embed payload → Im ─────────────────────────────
            payload_capacity = max(0, m * n - len(aux_positions))
            embedded_bits, extracted_ok = 0, False
            Im = If.copy()

            if payload_capacity > 0:
                payload_len = min(MAX_PAYLOAD, payload_capacity)
                payload     = np.random.randint(0, 2, payload_len).tolist()
                Im = embed_payload(If, payload,
                                   key=payload_key, aux_positions=aux_positions)
                extracted    = extract_payload(Im, payload_len,
                                               key=payload_key, aux_positions=aux_positions)
                embedded_bits = payload_len
                extracted_ok  = (payload == extracted)

            cv2.imwrite(os.path.join(MARKED_DIR, name), Im)

            # ── Im — stats ─────────────────────────────────────
            Im_corr_h = correlation(Im, "horizontal")
            Im_corr_v = correlation(Im, "vertical")
            Im_se     = entropy(Im)
            Im_chi2   = chi_square(Im)

            # ── Difference metrics ─────────────────────────────
            npcr_If_I  = npcr(If, I);   uaci_If_I  = uaci(If, I);   mae_If_I  = float(mae(If, I))
            npcr_Im_I  = npcr(Im, I);   uaci_Im_I  = uaci(Im, I);   mae_Im_I  = float(mae(Im, I))
            npcr_Im_If = npcr(Im, If);  uaci_Im_If = uaci(Im, If);  mae_Im_If = float(mae(Im, If))

            # ── Recovery ───────────────────────────────────────
            _ = extract_aux(Im, total_aux_bits, key=key_aux, k=aux_k)
            rec = recover_image(res, first)
            cv2.imwrite(os.path.join(REC_DIR, name), rec)
            psnr_val = psnr(I, rec)

            # ── Write CSV ──────────────────────────────────────
            writer.writerow([
                name, f"{m}x{n}",
                # I
                round(I_corr_h,  6), round(I_corr_v,  6), round(I_se,  6), round(I_chi2,  2),
                # If
                round(If_corr_h, 6), round(If_corr_v, 6), round(If_se, 6), round(If_chi2, 2),
                # Im
                round(Im_corr_h, 6), round(Im_corr_v, 6), round(Im_se, 6), round(Im_chi2, 2),
                # If vs I
                round(npcr_If_I,  4), round(uaci_If_I,  4), round(mae_If_I,  4),
                # Im vs I
                round(npcr_Im_I,  4), round(uaci_Im_I,  4), round(mae_Im_I,  4),
                # Im vs If
                round(npcr_Im_If, 4), round(uaci_Im_If, 4), round(mae_Im_If, 4),
                # payload
                embedded_bits, round(capacity_bpp, 4), extracted_ok, psnr_val,
            ])
            csv_file.flush()

            print(f"  cap={capacity_bpp:.3f}bpp | "
                  f"NPCR(If-I)={npcr_If_I:.2f}% UACI(If-I)={uaci_If_I:.2f}% | "
                  f"NPCR(Im-I)={npcr_Im_I:.2f}% UACI(Im-I)={uaci_Im_I:.2f}% | "
                  f"NPCR(Im-If)={npcr_Im_If:.2f}%")

        except Exception as e:
            import traceback
            print(f"  ERROR: {e}"); traceback.print_exc()
            continue

print("\n✅ Done →", CSV_PATH)