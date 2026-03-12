import numpy as np

def classify_block(residuals):
    vals, counts = np.unique(residuals, return_counts=True)
    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log2(probs + 1e-12))

    if entropy < 1.5:
        return 0
    elif entropy < 2.5:
        return 1
    elif entropy < 3.5:
        return 2
    else:
        return 3
