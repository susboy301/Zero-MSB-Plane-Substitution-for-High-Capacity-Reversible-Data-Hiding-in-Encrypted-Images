import os
import cv2
import numpy as np

from core.residuals import compute_residuals
from core.compress import count_zero_msb_planes

DATASET_DIR = r"C:\Users\Mayoo\Downloads\BOSSbase_1.01 (1)\BOSSbase_1.01"

block_sizes = [2, 4, 8]

for t in block_sizes:
    total_capacity = 0
    total_pixels = 0

    for name in sorted(os.listdir(DATASET_DIR)):
        if not name.lower().endswith((".bmp", ".png", ".pgm", ".tif")):
            continue

        img = cv2.imread(os.path.join(DATASET_DIR, name), 0)
        res, _ = compute_residuals(img)

        m, n = img.shape
        total_pixels += m * n

        for i in range(0, m, t):
            for j in range(0, n, t):
                blk = res[i:i+t, j:j+t]
                z = count_zero_msb_planes(blk)
                total_capacity += z * (t*t)

    bpp = total_capacity / total_pixels
    print(f"Block size {t}x{t} → Capacity: {bpp:.4f} bpp")