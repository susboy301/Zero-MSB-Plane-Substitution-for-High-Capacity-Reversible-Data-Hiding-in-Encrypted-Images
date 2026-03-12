import numpy as np

def psnr(a, b):
    mse = np.mean((a.astype(float) - b.astype(float)) ** 2)
    if mse == 0:
        return float('inf')
    return 10 * np.log10(255 * 255 / mse)
