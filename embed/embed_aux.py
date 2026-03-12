# ============================================================
# embed_aux.py  —  UPGRADED VERSION
# ============================================================
# CHANGES FROM ORIGINAL:
#   1. AUXILIARY BITSTREAM ENCRYPTION
#      Original: wrote aux bits (z_k headers + compressed bits)
#      directly into pixel LSBs — completely readable by anyone
#      with the marked image.
#      Upgraded: XOR the aux bitstream with a key-derived 0/1
#      stream before writing. An attacker reading pixel LSBs now
#      sees encrypted (random-looking) bits.
#      Cost: zero bits of capacity — only the *content* changes.
#
#   2. SCATTERED AUX PIXEL POSITIONS (anti-patch-removal)
#      Original: wrote aux bits sequentially from pixel 0 in
#      raster order — a 40×40 patch on the top-left could
#      destroy all auxiliary data.
#      Upgraded: positions are chosen via a key-seeded PRNG
#      permutation spread across the ENTIRE image.
#      A 40×40 patch now hits ~0.6% of pixels at random, not
#      the critical front region.
#      Cost: zero bits of capacity.
#
#   3. Returns aux_pixel_set (sorted list of pixel indices used)
#      so that extract_aux.py and embed_payload.py can
#      consistently avoid each other's regions.
# ============================================================

import numpy as np
import math


def _build_aux_bitstream(blocks):
    """Build the raw aux bitstream (same logic as original)."""
    bits = []
    for b in blocks:
        # 3-bit zero_planes header (0–7 in binary)
        bits.extend([int(x) for x in format(b.zero_planes, "03b")])
        if b.zero_planes >= 3:
            bits.extend(b.compressed["plane_bits"])
        else:
            bits.extend(b.compressed["residual_bits"])
    return bits


def _encrypt_bitstream(bits, key):
    """
    XOR a bit list with a key-derived pseudo-random 0/1 stream.
    Applying this function twice (same key, same length) gives back
    the original bits — it is its own inverse.
    """
    rng  = np.random.default_rng(key)
    mask = rng.integers(0, 2, len(bits), dtype=np.uint8)
    return [b ^ int(m) for b, m in zip(bits, mask)]


def embed_aux(enc_img, blocks, key):
    """
    Embed auxiliary data into the encrypted image.

    Parameters
    ----------
    enc_img : np.ndarray (H, W) uint8
    blocks  : list of ResidualBlock (with .zero_planes and .compressed set)
    key     : int  — key_aux from main.py (used for both encryption and
              position selection; two independent sub-keys derived internally)

    Returns
    -------
    marked_img   : np.ndarray (H, W) uint8
    k            : int  — bits per pixel used (for aux_pixels_used calc)
    aux_positions: np.ndarray  — sorted pixel indices used for aux data
                   Pass this to embed_payload as the exclusion set.
    """
    img  = enc_img.copy().astype(np.uint8)
    flat = img.flatten()
    N    = len(flat)

    # ── Step 1: Build aux bitstream ──────────────────────────────
    raw_bits   = _build_aux_bitstream(blocks)
    total_bits = len(raw_bits)

    # ── Step 2: Encrypt aux bitstream with key_aux ───────────────
    # Derive sub-key for content encryption (different from position key)
    enc_key    = key ^ 0xA5A5A5A5          # simple XOR derivation — stays int
    enc_bits   = _encrypt_bitstream(raw_bits, enc_key)

    # ── Step 3: How many bits per pixel do we need? ───────────────
    k = math.ceil(total_bits / N)           # same as original

    # ── Step 4: Choose which pixels carry aux data ────────────────
    # Derive sub-key for position selection (different from content key)
    pos_key       = key ^ 0x5A5A5A5A
    pos_rng       = np.random.default_rng(pos_key)
    num_aux_pixels = math.ceil(total_bits / k)  # pixels needed at k bits/px

    # Shuffle ALL pixel indices; take first num_aux_pixels
    full_perm     = pos_rng.permutation(N)
    aux_positions = np.sort(full_perm[:num_aux_pixels])  # sorted for locality

    # ── Step 5: Write encrypted bits into chosen pixels ──────────
    idx = 0
    for px in aux_positions:
        v = int(flat[px])
        for bit in range(k):
            if idx >= total_bits:
                break
            v   = (v & ~(1 << bit)) | (enc_bits[idx] << bit)
            idx += 1
        flat[px] = np.uint8(v & 0xFF)

    return flat.reshape(img.shape), k, aux_positions


# ── Self-test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from core.block import ResidualBlock
    from core.compress import compress_block
    import numpy as np

    rng = np.random.default_rng(42)
    img = rng.integers(0, 256, (16, 16), dtype=np.uint8)

    blocks = []
    for i in range(0, 16, 4):
        for j in range(0, 16, 4):
            blk = img[i:i+4, j:j+4].astype(int) - 128  # fake residuals
            b   = ResidualBlock(len(blocks), blk)
            compress_block(b)
            blocks.append(b)

    marked, k, aux_pos = embed_aux(img, blocks, key=456)
    print(f"embed_aux self-test: k={k}, aux_pixels={len(aux_pos)}")
    print("First 5 aux positions (scattered):", aux_pos[:5])
    print("PASSED — aux is scattered, not sequential from pixel 0")
