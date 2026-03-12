import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from core.residuals import compute_residuals

DATASET_DIR = r"C:\Users\Mayoo\Downloads\BOSSbase_1.01 (1)\BOSSbase_1.01"

all_residuals = []

for name in sorted(os.listdir(DATASET_DIR)):
    if not name.lower().endswith((".bmp", ".png", ".pgm", ".tif")):
        continue

    img = cv2.imread(os.path.join(DATASET_DIR, name), 0)
    res, _ = compute_residuals(img)
    all_residuals.extend(res.flatten())

plt.hist(all_residuals, bins=100)
plt.title("Residual Value Distribution")
plt.xlabel("Residual")
plt.ylabel("Frequency")
plt.show()