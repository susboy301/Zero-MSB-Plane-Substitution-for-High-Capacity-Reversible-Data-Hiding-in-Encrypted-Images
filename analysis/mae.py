import numpy as np

def mae(a, b):
    return np.mean(np.abs(a.astype(np.int16) - b.astype(np.int16)))
