import matplotlib.pyplot as plt

def set_ieee_style():
    plt.rcParams.update({
        "font.family": "serif",

        # global font
        "font.size": 16,

        # titles
        "axes.titlesize": 20,
        "axes.titleweight": "bold",

        # axis labels
        "axes.labelsize": 18,

        # ticks
        "xtick.labelsize": 15,
        "ytick.labelsize": 15,

        # legend
        "legend.fontsize": 15,

        # lines
        "lines.linewidth": 2.5,

        # remove top/right spines
        "axes.spines.top": False,
        "axes.spines.right": False,

        # improve layout
        "figure.dpi": 600,
    })