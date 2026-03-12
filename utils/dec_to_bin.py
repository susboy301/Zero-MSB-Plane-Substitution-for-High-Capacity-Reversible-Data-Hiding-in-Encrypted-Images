# utils/dec_to_bin.py
def dec_to_bin(x, bits):
    return [(x >> (bits - 1 - i)) & 1 for i in range(bits)]