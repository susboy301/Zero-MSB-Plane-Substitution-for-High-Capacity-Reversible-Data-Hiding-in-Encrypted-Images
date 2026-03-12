import os
import re
import cv2
import csv
import numpy as np

from analysis_metrics import (
    correlation,
    entropy,
    mae,
    chi_square,
    npcr,
    uaci
)

# ==========================================================
# PATHS (CHANGE ONLY THIS IF NEEDED)
# ==========================================================
BASE_PATH = r"C:\Users\Mayoo\Downloads\Reversible_Data_Hiding-2\Reversible_Data_Hiding_V2"

ORIGINAL_DIR  = os.path.join(BASE_PATH, "Testimages")
ENCRYPTED_DIR = os.path.join(BASE_PATH, "Encryptedimages_test")
MARKED_DIR    = os.path.join(BASE_PATH, "Markedimages_test")

OUTPUT_CSV = "ieee_statistical_results.csv"


# ==========================================================
# Helper: Normalize filename (remove (1), (2), spaces etc.)
# ==========================================================
def normalize_name(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r"\s*\(\d+\)", "", name)  # remove (1), (2)
    return name.lower().strip()


# ==========================================================
# Build filename dictionaries
# ==========================================================
def build_file_dict(folder):
    files = {}
    for f in os.listdir(folder):
        key = normalize_name(f)
        files[key] = f
    return files


orig_files = build_file_dict(ORIGINAL_DIR)
enc_files  = build_file_dict(ENCRYPTED_DIR)
mark_files = build_file_dict(MARKED_DIR)


# ==========================================================
# Prepare CSV
# ==========================================================
with open(OUTPUT_CSV, "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Image",
        "I_corr_h", "I_corr_v", "I_entropy", "I_chi2",
        "If_corr_h", "If_corr_v", "If_entropy", "If_MAE",
        "If_chi2", "If_NPCR", "If_UACI",
        "Im_corr_h", "Im_corr_v", "Im_entropy", "Im_MAE",
        "Im_chi2", "Im_NPCR", "Im_UACI"
    ])

    print("\n================ IEEE TABLE STYLE RESULTS ================\n")

    for key in orig_files:

        if key in enc_files and key in mark_files:

            I  = cv2.imread(os.path.join(ORIGINAL_DIR, orig_files[key]), 0)
            If = cv2.imread(os.path.join(ENCRYPTED_DIR, enc_files[key]), 0)
            Im = cv2.imread(os.path.join(MARKED_DIR, mark_files[key]), 0)

            # ---------------- ORIGINAL ----------------
            I_corr_h = correlation(I, "horizontal")
            I_corr_v = correlation(I, "vertical")
            I_entropy = entropy(I)
            I_chi2 = chi_square(I)

            # ---------------- ENCRYPTED ----------------
            If_corr_h = correlation(If, "horizontal")
            If_corr_v = correlation(If, "vertical")
            If_entropy = entropy(If)
            If_mae = mae(I, If)
            If_chi2 = chi_square(If)
            If_npcr = npcr(I, If)
            If_uaci = uaci(I, If)

            # ---------------- MARKED ----------------
            Im_corr_h = correlation(Im, "horizontal")
            Im_corr_v = correlation(Im, "vertical")
            Im_entropy = entropy(Im)
            Im_mae = mae(I, Im)
            Im_chi2 = chi_square(Im)
            Im_npcr = npcr(I, Im)
            Im_uaci = uaci(I, Im)

            # Console IEEE-style print
            print(f"---- {key.upper()} ----")
            print(f"I   : CorrH={I_corr_h:.4f}, CorrV={I_corr_v:.4f}, Ent={I_entropy:.4f}, Chi2={I_chi2:.2f}")
            print(f"If  : CorrH={If_corr_h:.4f}, CorrV={If_corr_v:.4f}, Ent={If_entropy:.4f}, "
                  f"MAE={If_mae:.4f}, Chi2={If_chi2:.2f}, NPCR={If_npcr:.2f}%, UACI={If_uaci:.2f}%")
            print(f"Im  : CorrH={Im_corr_h:.4f}, CorrV={Im_corr_v:.4f}, Ent={Im_entropy:.4f}, "
                  f"MAE={Im_mae:.4f}, Chi2={Im_chi2:.2f}, NPCR={Im_npcr:.2f}%, UACI={Im_uaci:.2f}%")
            print()

            # Write to CSV
            writer.writerow([
                key,
                I_corr_h, I_corr_v, I_entropy, I_chi2,
                If_corr_h, If_corr_v, If_entropy, If_mae,
                If_chi2, If_npcr, If_uaci,
                Im_corr_h, Im_corr_v, Im_entropy, Im_mae,
                Im_chi2, Im_npcr, Im_uaci
            ])

print("\nResults saved to:", OUTPUT_CSV)
