import numpy as np

def entropy(img):
    """
    Shannon entropy of an 8-bit grayscale image
    """
    hist = np.bincount(img.flatten(), minlength=256)
    p = hist / np.sum(hist)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))
