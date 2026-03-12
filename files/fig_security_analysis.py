import pandas as pd
import matplotlib.pyplot as plt
from plot_style import set_ieee_style

set_ieee_style()

boss = pd.read_csv("bossbase_results.csv")
bows = pd.read_csv("bows2_results_50.csv")

COLOR_BOSS="#2166AC"
COLOR_BOWS="#D6604D"

fig, axes = plt.subplots(1,2,figsize=(12,5))

for ax,col,title in [
    (axes[0],"correlation_h_enc","Horizontal Pixel Correlation"),
    (axes[1],"correlation_v_enc","Vertical Pixel Correlation")
]:
    ax.hist(boss[col],bins=60,color=COLOR_BOSS,alpha=0.6,label="BOSSbase",density=True)
    ax.hist(bows[col],bins=60,color=COLOR_BOWS,alpha=0.6,label="BOWS-2",density=True)

    ax.axvline(0,color="black",linestyle="--")
    ax.set_xlabel("Correlation Coefficient")
    ax.set_ylabel("Density")
    ax.set_title(title)
    ax.legend()

plt.tight_layout()
plt.savefig("fig_correlation_distribution.png",dpi=600,bbox_inches="tight")
plt.savefig("fig_correlation_distribution.pdf",bbox_inches="tight")
plt.close()