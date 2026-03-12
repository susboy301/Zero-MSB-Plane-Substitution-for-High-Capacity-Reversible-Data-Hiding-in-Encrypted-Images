import os
import cv2
import csv
import numpy as np

from core.residuals import compute_residuals
from core.compress import count_zero_msb_planes

t = 4
DATASET_DIR = r"C:\Users\Mayoo\Downloads\BOSSbase_1.01 (1)\BOSSbase_1.01"
OUTPUT_CSV = "mode_statistics.csv"

# -----------------------------
# Load already processed images
# -----------------------------
processed = set()

if os.path.exists(OUTPUT_CSV):
    with open(OUTPUT_CSV, "r") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if row:
                processed.add(row[0])

# -----------------------------
# Open CSV in append mode
# -----------------------------
file_exists = os.path.exists(OUTPUT_CSV)

with open(OUTPUT_CSV, "a", newline="") as f:
    writer = csv.writer(f)

    # Write header only if file didn't exist
    if not file_exists:
        writer.writerow(["Image", "Plane_Mode_%", "Residual_Mode_%"])

    for name in sorted(os.listdir(DATASET_DIR)):

        if not name.lower().endswith((".bmp", ".png", ".pgm", ".tif")):
            continue

        # Skip already processed images
        if name in processed:
            print(f"Skipping {name} (already processed)")
            continue

        img_path = os.path.join(DATASET_DIR, name)
        img = cv2.imread(img_path, 0)

        if img is None:
            continue

        res, _ = compute_residuals(img)

        plane_blocks = 0
        total_blocks = 0

        for i in range(0, img.shape[0], t):
            for j in range(0, img.shape[1], t):
                blk = res[i:i+t, j:j+t]

                if blk.shape != (t, t):
                    continue

                z = count_zero_msb_planes(blk)

                if z >= 3:
                    plane_blocks += 1

                total_blocks += 1

        plane_ratio = plane_blocks / total_blocks * 100
        residual_ratio = 100 - plane_ratio

        writer.writerow([name, plane_ratio, residual_ratio])

        # Flush ensures data is saved immediately
        f.flush()

        print(f"Processed {name}")

print("Processing complete. Data saved to:", OUTPUT_CSV)