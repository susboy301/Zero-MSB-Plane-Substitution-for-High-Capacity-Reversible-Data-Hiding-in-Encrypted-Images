import os
import cv2
import csv
import numpy as np

from core.residuals import compute_residuals
from core.block import ResidualBlock
from core.compress import count_zero_msb_planes

# ============================
# PARAMETERS
# ============================
t = 4
DATASET_DIR = r"C:\Users\Mayoo\Downloads\BOSSbase_1.01 (1)\BOSSbase_1.01"
OUTPUT_CSV = "zero_plane_distribution.csv"

# ============================
# LOAD ALREADY PROCESSED FILES
# ============================
processed = set()

if os.path.exists(OUTPUT_CSV):
    with open(OUTPUT_CSV, "r") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if row:
                processed.add(row[0])

# ============================
# PROCESS
# ============================
file_exists = os.path.exists(OUTPUT_CSV)

with open(OUTPUT_CSV, "a", newline="") as f:
    writer = csv.writer(f)

    # Write header if file is new
    if not file_exists:
        header = ["Image"] + [f"z={i}" for i in range(9)]
        writer.writerow(header)

    for name in sorted(os.listdir(DATASET_DIR)):

        if not name.lower().endswith((".bmp", ".png", ".pgm", ".tif")):
            continue

        # Skip already processed images
        if name in processed:
            print(f"Skipping {name}")
            continue

        img_path = os.path.join(DATASET_DIR, name)
        img = cv2.imread(img_path, 0)

        if img is None:
            continue

        res, _ = compute_residuals(img)

        counts = [0] * 9

        for i in range(0, img.shape[0], t):
            for j in range(0, img.shape[1], t):

                blk = res[i:i+t, j:j+t]

                if blk.shape != (t, t):
                    continue

                z = count_zero_msb_planes(blk)
                counts[z] += 1

        writer.writerow([name] + counts)

        # Save immediately
        f.flush()

        print(f"Processed {name}")

print("Zero-plane distribution saved to:", OUTPUT_CSV)