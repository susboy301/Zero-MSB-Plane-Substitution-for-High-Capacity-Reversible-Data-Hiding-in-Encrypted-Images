import numpy as np
import cv2

# ==========================================================
# 1. CORRELATION (Horizontal / Vertical)
# ==========================================================
def correlation(img, direction="horizontal"):
    img = img.astype(np.float64)

    if direction == "horizontal":
        x = img[:, :-1]
        y = img[:, 1:]

    elif direction == "vertical":
        x = img[:-1, :]
        y = img[1:, :]

    else:
        raise ValueError("direction must be 'horizontal' or 'vertical'")

    x = x.flatten()
    y = y.flatten()

    mx = np.mean(x)
    my = np.mean(y)

    num = np.mean((x - mx) * (y - my))
    den = np.sqrt(np.mean((x - mx)**2) * np.mean((y - my)**2))

    if den == 0:
        return 0.0

    return float(num / den)


# ==========================================================
# 2. SHANNON ENTROPY
# ==========================================================
def entropy(img):
    hist = np.bincount(img.flatten(), minlength=256)
    p = hist / np.sum(hist)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


# ==========================================================
# 3. MAE (Mean Absolute Error)
# ==========================================================
def mae(a, b):
    return float(np.mean(np.abs(a.astype(np.int16) - b.astype(np.int16))))


# ==========================================================
# 4. CHI-SQUARE TEST
# ==========================================================
def chi_square(img):
    hist = np.bincount(img.flatten(), minlength=256)
    expected = np.mean(hist)

    # Avoid division by zero
    if expected == 0:
        return 0.0

    chi2 = np.sum((hist - expected) ** 2 / expected)
    return float(chi2)


# ==========================================================
# 5. NPCR
# ==========================================================
def npcr(a, b):
    diff = a != b
    return float(np.sum(diff) / diff.size * 100)


# ==========================================================
# 6. UACI
# ==========================================================
def uaci(a, b):
    return float(
        np.mean(np.abs(a.astype(np.int16) - b.astype(np.int16))) / 255 * 100
    )


# ==========================================================
# 7. FULL STATISTICS COMPUTATION
# ==========================================================
def compute_full_statistics(I, If, Im):
    results = {}

    # ---- ORIGINAL IMAGE ----
    results["I_corr_h"] = correlation(I, "horizontal")
    results["I_corr_v"] = correlation(I, "vertical")
    results["I_entropy"] = entropy(I)
    results["I_chi2"] = chi_square(I)

    # ---- ENCRYPTED IMAGE ----
    results["If_corr_h"] = correlation(If, "horizontal")
    results["If_corr_v"] = correlation(If, "vertical")
    results["If_entropy"] = entropy(If)
    results["If_mae"] = mae(I, If)
    results["If_chi2"] = chi_square(If)
    results["If_npcr"] = npcr(I, If)
    results["If_uaci"] = uaci(I, If)

    # ---- MARKED IMAGE ----
    results["Im_corr_h"] = correlation(Im, "horizontal")
    results["Im_corr_v"] = correlation(Im, "vertical")
    results["Im_entropy"] = entropy(Im)
    results["Im_mae"] = mae(I, Im)
    results["Im_chi2"] = chi_square(Im)
    results["Im_npcr"] = npcr(I, Im)
    results["Im_uaci"] = uaci(I, Im)

    return results
