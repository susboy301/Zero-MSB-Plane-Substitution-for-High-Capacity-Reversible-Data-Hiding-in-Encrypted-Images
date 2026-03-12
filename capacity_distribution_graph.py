import pandas as pd
import matplotlib.pyplot as plt

# load dataset results
df = pd.read_csv("bossbase_results.csv")

bpp = df["capacity_bpp"]

plt.figure(figsize=(6,4))
plt.hist(bpp, bins=40)

plt.xlabel("Embedding Capacity (bpp)")
plt.ylabel("Number of Images")
plt.title("Embedding Capacity Distribution (BOSSbase)")

plt.grid(alpha=0.3)

plt.savefig("capacity_distribution.png", dpi=300, bbox_inches="tight")
plt.show()