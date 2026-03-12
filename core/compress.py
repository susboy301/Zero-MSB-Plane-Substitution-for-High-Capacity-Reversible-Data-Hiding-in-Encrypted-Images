import numpy as np
from utils.dec_to_bin import dec_to_bin

# -------------------------------------------------
# Count leading zero MSB planes (BPZS)
# -------------------------------------------------
def count_zero_msb_planes(block):
    absb = np.abs(block)
    k = 0
    for b in range(7, -1, -1):   # MSB → LSB
        if np.any((absb >> b) & 1):
            break
        k += 1
    return k


# -------------------------------------------------
# Hybrid compression: BPZS + residual fallback
# -------------------------------------------------
def compress_block(block):
    res = block.residuals
    n = res.size

    # --- BPZS analysis ---
    k = count_zero_msb_planes(res)
    block.zero_planes = k

    # implicit mode:
    # zero_planes >= 3 → plane mode
    # zero_planes < 3  → residual mode

    # =================================================
    # PLANE MODE (smooth blocks)
    # =================================================
    if k >= 3:
        absb = np.abs(res)
        bits = []

        # encode only non-zero planes
        for b in range(7 - k, -1, -1):
            plane = ((absb >> b) & 1).flatten().tolist()
            bits.extend(plane)

        block.compressed["plane_bits"] = bits
        block.slack = k * n
        return

    # =================================================
    # RESIDUAL MODE (textured blocks)
    # =================================================
    flat = res.flatten()
    bits = []

    for r in flat:
        sign = 1 if r < 0 else 0
        mag = abs(int(r))
        bits.append(sign)
        bits.extend(dec_to_bin(mag, 8))

    block.compressed["residual_bits"] = bits
    block.slack = max(0, n * 9 - len(bits))
