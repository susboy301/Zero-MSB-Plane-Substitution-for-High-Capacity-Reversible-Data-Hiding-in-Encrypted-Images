import numpy as np

def recover_from_planes(blocks, shape):
    out = np.zeros(shape, dtype=int)
    idx = 0

    for b in blocks:
        h, w = b.residuals.shape
        if b.mode == "plane":
            k = b.zero_planes
            n = h * w
            planes = [[0]*n for _ in range(8)]
            pidx = 0
            for bit in range(7 - k, -1, -1):
                for i in range(n):
                    planes[bit][i] = b.compressed["plane_bits"][pidx]
                    pidx += 1
            flat = np.zeros(n, dtype=int)
            for bit in range(8):
                flat |= (np.array(planes[bit]) << bit)
            block_res = flat.reshape(h, w)
        else:
            flat = []
            bits = b.compressed["plane_bits"]
            p = 0
            for _ in range(h*w):
                sign = bits[p]; p+=1
                mag = int("".join(str(x) for x in bits[p:p+8]),2); p+=8
                flat.append(-mag if sign else mag)
            block_res = np.array(flat).reshape(h,w)

        out[idx:idx+h, :w] = block_res
        idx += h

    return out
