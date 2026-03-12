# ============================================================
# extract_aux.py  —  UPGRADED VERSION
# ============================================================
# CHANGES FROM ORIGINAL:
#   1. Must now read from SCATTERED positions (not sequential).
#      Uses the same pos_key to regenerate aux_positions.
#   2. Must DECRYPT the aux bitstream after reading
#      (XOR with same enc_key stream used in embed_aux.py).
#   3. New parameter: key (was not needed in original because
#      sequential read needed no key).
#   4. New parameter: k (bits per pixel, returned by embed_aux).
#      Original read 1 bit/pixel; upgraded reads k bits/pixel.
#
# NOTE: num_bits and key must match exactly what was used in
# embed_aux.py for the same image.
# ============================================================

import numpy as np
import math


def _decrypt_bitstream(bits, key):
    """
    XOR a bit list with a key-derived pseudo-random 0/1 stream.
    Identical to _encrypt_bitstream — XOR is its own inverse.
    """
    rng  = np.random.default_rng(key)
    mask = rng.integers(0, 2, len(bits), dtype=np.uint8)
    return [b ^ int(m) for b, m in zip(bits, mask)]


def extract_aux(enc_img, num_bits, key, k):
    """
    Extract and decrypt the auxiliary bitstream from the marked image.

    Parameters
    ----------
    enc_img  : np.ndarray (H, W) uint8 — the marked encrypted image
    num_bits : int  — total aux bits (same as total_aux_bits in main.py)
    key      : int  — key_aux (same key used in embed_aux)
    k        : int  — bits per pixel (returned by embed_aux as aux_k)

    Returns
    -------
    list of int  — decrypted aux bitstream, length = num_bits
    """
    flat = enc_img.flatten()
    N    = len(flat)

    # ── Re-derive the same position permutation ──────────────────
    pos_key       = key ^ 0x5A5A5A5A
    pos_rng       = np.random.default_rng(pos_key)
    num_aux_pixels = math.ceil(num_bits / k)
    full_perm      = pos_rng.permutation(N)
    aux_positions  = np.sort(full_perm[:num_aux_pixels])

    # ── Read k bits per pixel from aux_positions ──────────────────
    raw_bits = []
    for px in aux_positions:
        v = int(flat[px])
        for bit in range(k):
            raw_bits.append((v >> bit) & 1)
            if len(raw_bits) >= num_bits:
                break
        if len(raw_bits) >= num_bits:
            break

    # ── Decrypt the aux bitstream ─────────────────────────────────
    enc_key = key ^ 0xA5A5A5A5
    return _decrypt_bitstream(raw_bits[:num_bits], enc_key)


# ── LEGACY WRAPPER ────────────────────────────────────────────────────────────
# If other code calls extract_aux(img, num_bits) with 2 args (old interface),
# this warns and falls back to the original sequential-read logic so existing
# analysis scripts don't break.
def extract_aux_legacy(enc_img, num_bits):
    """Original sequential extract — kept for backward compatibility."""
    import warnings
    warnings.warn(
        "extract_aux_legacy uses the OLD unencrypted sequential read. "
        "Update callers to use extract_aux(img, num_bits, key, k) instead.",
        DeprecationWarning
    )
    flat = enc_img.flatten()
    bits = []
    for v in flat:
        for b in range(8):
            bits.append((int(v) >> b) & 1)
            if len(bits) >= num_bits:
                return bits
    return bits


# ── Self-test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Round-trip test: embed then extract should give back original bits
    import numpy as np
    from core.block import ResidualBlock
    from core.compress import compress_block

    rng = np.random.default_rng(7)
    img = rng.integers(0, 256, (32, 32), dtype=np.uint8)

    blocks = []
    for i in range(0, 32, 4):
        for j in range(0, 32, 4):
            blk = img[i:i+4, j:j+4].astype(int) % 10 - 5
            b   = ResidualBlock(len(blocks), blk)
            from core.compress import compress_block
            compress_block(b)
            blocks.append(b)

    # Build expected bits manually
    expected = []
    for b in blocks:
        expected.extend([int(x) for x in format(b.zero_planes, "03b")])
        if b.zero_planes >= 3:
            expected.extend(b.compressed["plane_bits"])
        else:
            expected.extend(b.compressed["residual_bits"])

    from embed.embed_aux import embed_aux
    marked, k, _ = embed_aux(img, blocks, key=456)
    recovered    = extract_aux(marked, len(expected), key=456, k=k)

    assert recovered == expected, f"Mismatch! {sum(a!=b for a,b in zip(recovered,expected))} bits differ"
    print("extract_aux round-trip self-test PASSED")
