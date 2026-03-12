# ============================================================
# extract_payload.py  —  UPGRADED VERSION
# ============================================================
# CHANGES FROM ORIGINAL:
#   1. Accepts aux_positions to reconstruct the correct set of
#      forbidden pixels — must match embed_payload exactly.
#   2. Falls back to start_pixel if aux_positions is None
#      (backward compatible).
# ============================================================

import numpy as np


def extract_payload(enc_img, payload_len, start_pixel=None, key=999,
                    aux_positions=None):
    """
    Extract payload bits from the marked encrypted image.

    Parameters
    ----------
    enc_img       : np.ndarray (H, W) uint8
    payload_len   : int — number of bits to extract
    start_pixel   : int — (LEGACY) skip pixels below this index
    key           : int — payload_key (must match embed_payload)
    aux_positions : np.ndarray or None (must match embed_payload)

    Returns
    -------
    list of int (0/1)
    """
    flat = enc_img.flatten()
    N    = len(flat)

    # ── Same forbidden set as embed_payload ───────────────────────
    if aux_positions is not None:
        forbidden = set(int(p) for p in aux_positions)
    elif start_pixel is not None:
        forbidden = set(range(start_pixel))
    else:
        forbidden = set()

    # ── Same PRNG permutation as embed_payload ────────────────────
    rng  = np.random.default_rng(key)
    perm = rng.permutation(N)

    # ── Read LSBs from same positions ─────────────────────────────
    bits = []
    for p in perm:
        if p in forbidden:
            continue
        if len(bits) >= payload_len:
            break
        bits.append(int(flat[p]) & 1)

    return bits
