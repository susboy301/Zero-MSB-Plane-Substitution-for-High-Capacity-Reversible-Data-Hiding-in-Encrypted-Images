import numpy as np

def chi_square(img):
    hist = np.bincount(img.flatten(), minlength=256)
    expected = np.mean(hist)
    return float(np.sum((hist - expected) ** 2 / expected))
