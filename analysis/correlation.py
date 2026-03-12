import numpy as np

def correlation(img, direction="horizontal"):
    """
    Correlation coefficient of adjacent pixels
    """
    img = img.astype(np.float64)

    if direction == "horizontal":
        x = img[:, :-1]
        y = img[:, 1:]
    elif direction == "vertical":
        x = img[:-1, :]
        y = img[1:, :]
    elif direction == "diagonal":
        x = img[:-1, :-1]
        y = img[1:, 1:]
    else:
        raise ValueError("direction must be horizontal / vertical / diagonal")

    x = x.flatten()
    y = y.flatten()

    mx, my = x.mean(), y.mean()
    num = np.mean((x - mx) * (y - my))
    den = np.sqrt(np.mean((x - mx)**2) * np.mean((y - my)**2))

    return float(num / den) if den != 0 else 0.0