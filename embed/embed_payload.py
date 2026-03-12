# ============================================================
# embed_payload.py  —  UPGRADED VERSION
# ============================================================
# CHANGES FROM ORIGINAL:
#   1. Instead of using a simple integer start_pixel cutoff,
#      payload embedding now explicitly AVOIDS the set of pixel
#      indices used by aux (aux_positions).
#      This is necessary because aux pixels are now scattered
#      pseudo-randomly, not confined to the first N pixels.
#
#   2. Accepts aux_positions as an optional parameter.
#      If not provided (aux_positions=None), falls back to the
#      original start_pixel behaviour for backward compatibility.
#
#   3. The payload permutation (key-seeded PRNG) is unchanged —
#      the random ordering already ensures uniform distribution.
# ============================================================

import numpy as np


def embed_payload(enc_img, payload_bits, start_pixel=None, key=999,
                  aux_positions=None):
    """
    Embed secret payload bits into the marked encrypted image.

    Parameters
    ----------
    enc_img       : np.ndarray (H, W) uint8
    payload_bits  : list of int (0/1)
    start_pixel   : int — (LEGACY) pixels < start_pixel are skipped.
                    Only used when aux_positions is None.
    key           : int — payload_key
    aux_positions : np.ndarray or None
                    Sorted array of pixel indices used by aux.
                    When provided, these pixels are EXCLUDED from
                    payload embedding (regardless of start_pixel).

    Returns
    -------
    np.ndarray (H, W) uint8 — image with payload embedded in LSBs
    """
    img  = enc_img.copy().astype(np.uint8)
    flat = img.flatten()
    N    = len(flat)

    # ── Build the set of forbidden pixel indices ──────────────────
    if aux_positions is not None:
        forbidden = set(int(p) for p in aux_positions)
    elif start_pixel is not None:
        # Legacy mode: any pixel index < start_pixel is forbidden
        forbidden = set(range(start_pixel))
    else:
        forbidden = set()

    # ── Generate payload embedding order via PRNG permutation ─────
    rng  = np.random.default_rng(key)
    perm = rng.permutation(N)

    # ── Embed payload bits into LSBs of non-forbidden pixels ──────
    idx = 0
    for p in perm:
        if p in forbidden:
            continue
        if idx >= len(payload_bits):
            break
        value     = int(flat[p])
        value     = (value & ~1) | payload_bits[idx]
        flat[p]   = np.uint8(value & 0xFF)
        idx      += 1

    if idx < len(payload_bits):
        raise ValueError(
            f"Not enough payload capacity: needed {len(payload_bits)} bits, "
            f"only {idx} available pixels."
        )

    return flat.reshape(img.shape)
