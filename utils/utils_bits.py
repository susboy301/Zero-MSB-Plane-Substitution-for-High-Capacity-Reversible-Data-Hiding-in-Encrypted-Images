"""
Bit / byte utility functions
Used by arithmetic coder and embedding pipeline
"""

def int_to_bits(value, length):
    """
    Convert non-negative integer to a list of bits (MSB first)
    """
    if value < 0:
        raise ValueError("int_to_bits expects non-negative integer")
    bits = [(value >> i) & 1 for i in range(length - 1, -1, -1)]
    return bits


def bits_to_int(bits):
    """
    Convert list of bits (MSB first) to integer
    """
    val = 0
    for b in bits:
        val = (val << 1) | int(b)
    return val


def bits_to_bytes(bits):
    """
    Convert list of bits (0/1) to bytes object
    Pads with zeros to complete last byte if needed.
    """
    if len(bits) == 0:
        return b""

    # pad to multiple of 8
    pad_len = (8 - (len(bits) % 8)) % 8
    bits = bits + [0] * pad_len

    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | int(b)
        out.append(byte)
    return bytes(out)


def bytes_to_bits(data):
    """
    Convert bytes object to list of bits (MSB first per byte)
    """
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits
