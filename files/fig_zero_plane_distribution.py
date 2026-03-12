import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plot_style import set_ieee_style

set_ieee_style()

df=pd.read_csv("zero_plane_distribution.csv")

plane_cols=[f"z={i}" for i in range(9)]

totals=df[plane_cols].sum()
fractions=(totals/totals.sum()*100).values

fig,ax=plt.subplots(figsize=(9,6))

x=np.arange(9)

bars=ax.bar(
    x,
    fractions,
    color="#2166AC",
    edgecolor="black",
    linewidth=0.7
)

for bar,val in zip(bars,fractions):
    ax.text(
        bar.get_x()+bar.get_width()/2,
        val+0.4,
        f"{val:.1f}%",
        ha="center"
    )

ax.set_xlabel("Number of consecutive zero MSB-planes ($z_{k}$)")
ax.set_ylabel("Proportion of Blocks (%)")
ax.set_title("Distribution of $z_{k}$ across BOSSbase")
ax.set_xticks(x)
ax.set_xticklabels([f"z={i}" for i in range(9)])

plt.tight_layout()
plt.savefig("fig_zero_plane_distribution.png",dpi=600,bbox_inches="tight")
plt.savefig("fig_zero_plane_distribution.pdf",bbox_inches="tight")
plt.close()