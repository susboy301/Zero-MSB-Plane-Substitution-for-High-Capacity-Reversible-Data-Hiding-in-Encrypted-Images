# utils/EncryptionString.py
def EncryptionString(bits, key):
    import numpy as np
    rng = np.random.default_rng(key)
    mask = rng.integers(0, 2, len(bits))
    return [b ^ m for b, m in zip(bits, mask)]
