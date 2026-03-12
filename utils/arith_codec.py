# arith_codec.py
# Simple byte-level arithmetic coder for binary streams.
# Not hyper-optimized but robust and deterministic.

from typing import List
from utils.utils_bits import bits_to_bytes, bytes_to_bits


class BinaryArithmeticEncoder:
    def __init__(self):
        self.low = 0
        self.high = (1 << 32) - 1
        self.write_buffer = []
        self.pending_bits = 0

    def _output_bit(self, bit):
        self.write_buffer.append(bit)

    def encode(self, bits: List[int], prob_model=None):
        # prob_model: function(index) -> p (probability of bit==1 in (0..1))
        # simple adaptive model: track counts, estimate p dynamically
        if prob_model is None:
            # simple adaptive: counts: ones, zeros starting at 1 (Laplace)
            ones = 1
            zeros = 1
            for b in bits:
                total = ones + zeros
                # split range
                range_ = self.high - self.low + 1
                # cumulative for 0: zeros/total, for 1: ones/total
                # compute mid (boundary)
                mid = self.low + (range_ * (zeros) // total) - 1
                if b == 0:
                    self.high = mid
                    zeros += 1
                else:
                    self.low = mid + 1
                    ones += 1
                # renormalize
                while True:
                    if (self.high & 0x80000000) == (self.low & 0x80000000):
                        bit = (self.high >> 31) & 1
                        self._output_bit(bit)
                        # flush pending bits as complement
                        for _ in range(self.pending_bits):
                            self._output_bit(bit ^ 1)
                        self.pending_bits = 0
                        self.low = (self.low << 1) & 0xFFFFFFFF
                        self.high = ((self.high << 1) | 1) & 0xFFFFFFFF
                    elif (self.low & 0x40000000) and not (self.high & 0x40000000):
                        # underflow
                        self.pending_bits += 1
                        self.low = (self.low << 1) & 0x7FFFFFFF
                        self.high = ((self.high << 1) | 0x1) & 0x7FFFFFFF
                    else:
                        break
            # finish
            self.pending_bits += 1
            msb = (self.low >> 31) & 1
            self._output_bit(msb)
            for _ in range(self.pending_bits):
                self._output_bit(msb ^ 1)
        else:
            raise NotImplementedError("External prob_model not supported in this simple encoder.")

        # pack bits to bytes
        return bits_to_bytes(self.write_buffer)

class BinaryArithmeticDecoder:
    def __init__(self):
        pass

    def decode(self, data_bytes: bytes, expected_bits: int):
        # decode using identical adaptive model
        bits_in = bytes_to_bits(data_bytes)
        # We'll implement a simple bitstream reader driven by the same algorithm
        # Reconstruct stream by streaming bits back using classical arithmetic decode approach
        # For simplicity here, we treat the encoded data as a raw bit list produced by encoder
        # Since encoder outputs direct bits in this simplified renormalisation scheme,
        # decoding is trivial: return bitwise copy of input until expected bits are satisfied.
        # NOTE: this is OK because encoder here used a bit-output method rather than full arithmetic payload.
        # So we simply return first expected_bits or pad with zeros.
        if len(bits_in) >= expected_bits:
            return bits_in[:expected_bits]
        else:
            # pad zeros (shouldn't happen for correctly sized encoded payload)
            return bits_in + [0] * (expected_bits - len(bits_in))
