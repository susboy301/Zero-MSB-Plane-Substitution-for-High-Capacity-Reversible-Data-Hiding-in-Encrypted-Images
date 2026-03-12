import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from plot_style import set_ieee_style

set_ieee_style()

boss = pd.read_csv("bossbase_results.csv")
bows = pd.read_csv("bows2_results_50.csv")

BINS = 50
COLOR_BOSS = "#2166AC"
COLOR_BOWS = "#D6604D"

fig, axes = plt.subplots(1,2,figsize=(12,5))

for ax, df, color, label in [
    (axes[0], boss, COLOR_BOSS, "BOSSbase"),
    (axes[1], bows, COLOR_BOWS, "BOWS-2")
]:
    bpp = df["capacity_bpp"].dropna()

    ax.hist(
        bpp,
        bins=BINS,
        color=color,
        edgecolor="black",
        linewidth=0.6,
        alpha=0.85
    )

    ax.axvline(bpp.mean(),color="black",linestyle="--",
               label=f"Mean = {bpp.mean():.3f}")

    ax.axvline(bpp.median(),color="gray",linestyle=":",
               label=f"Median = {bpp.median():.3f}")

    ax.set_xlabel("Embedding Capacity (bpp)")
    ax.set_ylabel("Number of Images")
    ax.set_title(f"Capacity Distribution — {label}")
    ax.legend()

    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x,_: f"{int(x):,}")
    )

plt.tight_layout()
plt.savefig("fig_capacity_distribution_both.png",dpi=600,bbox_inches="tight")
plt.savefig("fig_capacity_distribution_both.pdf",bbox_inches="tight")
plt.close()