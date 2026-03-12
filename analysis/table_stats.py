import cv2
from analysis.correlation import correlation
from analysis.entropy import entropy
from analysis.mae import mae
from analysis.chi_square import chi_square
from analysis.npcr_uaci import npcr, uaci

def compute_stats(I, If, Im):
    return {
        "Corr_H": correlation(I),
        "Corr_V": correlation(I, "vertical"),
        "SE": entropy(If),
        "MAE": mae(I, If),
        "Chi2": chi_square(If),
        "NPCR": npcr(If, Im),
        "UACI": uaci(If, Im)
    }
