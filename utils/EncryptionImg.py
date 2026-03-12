# ============================================================
# EncryptionImg.py  —  UPGRADED VERSION
# ============================================================
# CHANGES FROM ORIGINAL:
#   1. Added ChaCha20 stream cipher (cryptographically secure)
#      Original used NumPy PCG64 PRNG which is statistically
#      strong but NOT a CSPRNG — an adversary with known-plaintext
#      could potentially recover the keystream.
#   2. Key is now a 32-byte bytes object (256-bit) instead of int.
#      If you pass an int (backward compat), it is auto-converted.
#   3. A nonce (12 bytes) is derived deterministically from the key
#      using SHA-256 so no extra parameter is needed.
#   4. Interface is identical: EncryptionImg(img, key) → encrypted img
#      Decryption is the same call (XOR is its own inverse).
# ============================================================

import numpy as np
import hashlib

# ── Try to import pycryptodome (ChaCha20). If not installed,
#    fall back to the original NumPy PRNG with a warning.
try:
    from Crypto.Cipher import ChaCha20 as _ChaCha20
    _CHACHA_AVAILABLE = True
except ImportError:
    _CHACHA_AVAILABLE = False
    import warnings
    warnings.warn(
        "pycryptodome not found. Using NumPy PCG64 (statistical security only). "
        "Install with:  pip install pycryptodome",
        RuntimeWarning
    )


def _normalise_key(key):
    """
    Accept either:
      - bytes of any length  → SHA-256 to get 32 bytes
      - int                  → convert to bytes then SHA-256
    Returns: 32-byte key (bytes)
    """
    if isinstance(key, int):
        # Convert int to minimal byte representation, then hash
        key_bytes = key.to_bytes((key.bit_length() + 7) // 8 or 1, 'big')
    elif isinstance(key, (bytes, bytearray)):
        key_bytes = bytes(key)
    else:
        raise TypeError(f"key must be int or bytes, got {type(key)}")
    
    # Always hash to exactly 32 bytes — safe even if key is already 32 bytes
    return hashlib.sha256(key_bytes).digest()


def _derive_nonce(key32):
    """Derive a deterministic 12-byte ChaCha20 nonce from the 32-byte key."""
    # Use the first 12 bytes of SHA-256(key) — fully determined by key
    return hashlib.sha256(b"nonce:" + key32).digest()[:12]


def EncryptionImg(img, key):
    """
    Encrypt / decrypt a grayscale image using XOR with a keystream.

    Parameters
    ----------
    img  : np.ndarray  (H, W) uint8 grayscale image
    key  : int or bytes
           Original code used small ints like 123.
           Upgraded code accepts any int or bytes.
           Recommendation: use os.urandom(32) for production keys.

    Returns
    -------
    np.ndarray  (H, W) uint8  —  encrypted (or decrypted) image.
    Call twice with the same key to recover the original.
    """
    img_u8 = img.astype(np.uint8)
    flat   = img_u8.flatten()
    n      = len(flat)

    key32 = _normalise_key(key)

    if _CHACHA_AVAILABLE:
        # ── CHACHA20 PATH (cryptographically secure) ──────────────
        nonce  = _derive_nonce(key32)
        cipher = _ChaCha20.new(key=key32, nonce=nonce)
        # Encrypt n bytes of zeros → pure keystream
        keystream = np.frombuffer(cipher.encrypt(bytes(n)), dtype=np.uint8)
    else:
        # ── FALLBACK: NumPy PCG64 (original behaviour) ────────────
        # key32 interpreted as a big-endian integer for the seed
        seed = int.from_bytes(key32, 'big') % (2**63)   # PCG64 needs < 2^63
        rng  = np.random.default_rng(seed)
        keystream = rng.integers(0, 256, n, dtype=np.uint8)

    encrypted = np.bitwise_xor(flat, keystream).reshape(img_u8.shape)
    return encrypted


# ── Quick self-test (run this file directly to verify) ──────────────────────
if __name__ == "__main__":
    import os
    # Use a proper random key
    test_key = os.urandom(32)
    img = np.random.randint(0, 256, (8, 8), dtype=np.uint8)
    enc = EncryptionImg(img, test_key)
    dec = EncryptionImg(enc, test_key)
    assert np.array_equal(img, dec), "Decryption failed!"
    print("EncryptionImg self-test PASSED")
    print(f"  ChaCha20 available: {_CHACHA_AVAILABLE}")
    print(f"  Sample pixel original={img[0,0]}  encrypted={enc[0,0]}  recovered={dec[0,0]}")
