"""
FIGURE: Average Payload Comparison against State-of-the-Art Methods
Replicates paper Fig. 10 style bar chart for BOSSbase and BOWS-2
Values for compared methods are taken directly from paper Table VII / Fig. 10.
"""

import matplotlib.pyplot as plt
import numpy as np

# plt.rcParams.update({"font.family": "serif", "font.size": 11})
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 16,
    "axes.titlesize": 20,
    "axes.labelsize": 18,
    "xtick.labelsize": 15,
    "ytick.labelsize": 15,
    "legend.fontsize": 15,
    "lines.linewidth": 2.5
})
# ── Data from paper (Fig 10 / Table VII) ─────────────────────────────────────
# BOSSbase average bpp
methods_boss = {
    "Yu et al. [33]"       : 3.205,
    "Yin et al. [24]"      : 3.361,
    "Gao et al. [29]"      : 3.458,
    "Yin et al. [26]"      : 3.625,
    "Yu et al. [27]"       : 3.682,
    "Xu et al. [28]"       : 3.755,
    "Proposed Method"      : 3.793,   # ← your result
}

# BOWS-2 average bpp
methods_bows = {
    "Mohammadi et al. [25]": 2.900,
    "Yu et al. [33]"       : 3.115,
    "Yin et al. [24]"      : 3.246,
    "Gao et al. [29]"      : 3.314,
    "Yu et al. [27]"       : 3.457,
    "Yin et al. [26]"      : 3.495,
    "Xu et al. [28]"       : 3.664,
    "Proposed Method"      : 3.705,   # ← your result
}

PROPOSED_COLOR = "#D6604D"
OTHER_COLOR    = "#4393C3"

def make_bar_chart(data, title, fname, xlabel_start=2.7):
    names = list(data.keys())
    values = list(data.values())
    colors = [PROPOSED_COLOR if "Proposed" in n else OTHER_COLOR for n in names]

    fig, ax = plt.subplots(figsize=(8, 0.7 * len(names) + 1.5))
    y = np.arange(len(names))
    bars = ax.barh(y, values, color=colors, edgecolor="white", linewidth=0.5, height=0.6)

    for bar, val, color in zip(bars, values, colors):
        ax.text(val + 0.01, bar.get_y() + bar.get_height()/2,
                f"{val:.3f}", va="center", fontsize=10,
                fontweight="bold" if color == PROPOSED_COLOR else "normal")

    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=11)
    ax.set_xlabel("Average Embedding Capacity (bpp)", fontsize=12)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlim(xlabel_start, max(values) + 0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.invert_yaxis()

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=PROPOSED_COLOR, label="Proposed Method"),
        Patch(facecolor=OTHER_COLOR,    label="Compared Methods"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{fname}.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{fname}.pdf", bbox_inches="tight")
    print(f"Saved {fname}.png/.pdf")
    plt.close()

make_bar_chart(methods_boss,
               "Average Payload Comparison — BOSSbase Dataset",
               "fig_comparison_bossbase", xlabel_start=3.0)

make_bar_chart(methods_bows,
               "Average Payload Comparison — BOWS-2 Dataset",
               "fig_comparison_bows2", xlabel_start=2.7)

# ── Combined side-by-side ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for ax, data, title, xlim in [
    (axes[0], methods_boss, "(a) BOSSbase", (3.0, 3.87)),
    (axes[1], methods_bows, "(b) BOWS-2",  (2.7, 3.78)),
]:
    names = list(data.keys())
    values = list(data.values())
    colors = [PROPOSED_COLOR if "Proposed" in n else OTHER_COLOR for n in names]
    y = np.arange(len(names))
    bars = ax.barh(y, values, color=colors, edgecolor="white", linewidth=0.5, height=0.6)

    for bar, val, color in zip(bars, values, colors):
        ax.text(val + 0.005, bar.get_y() + bar.get_height()/2,
                f"{val:.3f}", va="center", fontsize=9,
                fontweight="bold" if color == PROPOSED_COLOR else "normal")

    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel("Average Embedding Capacity (bpp)", fontsize=11)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlim(*xlim)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.invert_yaxis()

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=PROPOSED_COLOR, label="Proposed Method"),
    Patch(facecolor=OTHER_COLOR,    label="Compared Methods"),
]
axes[1].legend(handles=legend_elements, loc="lower right", fontsize=10)

plt.suptitle("Comparison of Average Payload (bpp) on Two Datasets", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("fig_comparison_both_datasets.png", dpi=300, bbox_inches="tight")
plt.savefig("fig_comparison_both_datasets.pdf", bbox_inches="tight")
print("Saved fig_comparison_both_datasets.png/.pdf")
plt.close()
