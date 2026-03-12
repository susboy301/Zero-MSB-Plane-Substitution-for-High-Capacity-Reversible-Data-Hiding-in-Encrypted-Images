import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plot_style import set_ieee_style

set_ieee_style()

boss = pd.read_csv("bossbase_results.csv")
bows = pd.read_csv("bows2_results_50.csv")

fig, ax = plt.subplots(figsize=(9,6))

for df, color, label in [
    (boss, "#2166AC", "BOSSbase"),
    (bows, "#D6604D", "BOWS-2"),
]:
    bpp = np.sort(df["capacity_bpp"].dropna().values)
    cdf = np.arange(1, len(bpp)+1) / len(bpp) * 100
    ax.plot(bpp, cdf, color=color, label=f"{label} (mean={bpp.mean():.3f})")

for ref in [1,2,3,4,5]:
    ax.axvline(ref, color="gray", linestyle=":", linewidth=1)

ax.set_xlabel("Embedding Capacity (bpp)")
ax.set_ylabel("Cumulative Percentage of Images (%)")
ax.set_title("CDF of Embedding Capacity")
ax.set_ylim(0,100)
ax.legend()

plt.tight_layout()
plt.savefig("fig_capacity_cdf.png", dpi=600, bbox_inches="tight")
plt.savefig("fig_capacity_cdf.pdf", bbox_inches="tight")
plt.close()