# utils/bin_to_dec.py
def bin_to_dec(bits):
    v = 0
    for b in bits:
        v = (v << 1) | b
    return v