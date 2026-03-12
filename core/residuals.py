import numpy as np

# -------------------------------------------------
# LOCO-I (JPEG-LS) predictor — overflow safe
# -------------------------------------------------

def compute_residuals(img):
    img = img.astype(int)            # signed arithmetic
    h, w = img.shape
    res = np.zeros((h, w), dtype=int)

    first_pixel = img[0, 0]

    for i in range(h):
        for j in range(w):
            if i == 0 and j == 0:
                res[i, j] = 0
                continue

            left = img[i, j-1] if j > 0 else img[i-1, j]
            up   = img[i-1, j] if i > 0 else img[i, j-1]
            ul   = img[i-1, j-1] if (i > 0 and j > 0) else left

            # LOCO-I predictor
            if ul >= max(left, up):
                pred = min(left, up)
            elif ul <= min(left, up):
                pred = max(left, up)
            else:
                pred = left + up - ul

            res[i, j] = img[i, j] - pred

    return res, first_pixel


def recover_image(res, first_pixel):
    h, w = res.shape
    img = np.zeros((h, w), dtype=int)
    img[0, 0] = int(first_pixel)

    for i in range(h):
        for j in range(w):
            if i == 0 and j == 0:
                continue

            left = img[i, j-1] if j > 0 else img[i-1, j]
            up   = img[i-1, j] if i > 0 else img[i, j-1]
            ul   = img[i-1, j-1] if (i > 0 and j > 0) else left

            # LOCO-I predictor
            if ul >= max(left, up):
                pred = min(left, up)
            elif ul <= min(left, up):
                pred = max(left, up)
            else:
                pred = left + up - ul

            img[i, j] = pred + res[i, j]

    return (img & 0xFF).astype(np.uint8)
