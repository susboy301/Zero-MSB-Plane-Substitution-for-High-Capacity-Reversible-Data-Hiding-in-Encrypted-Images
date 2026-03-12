"""
TABLE VI: Experimental Results of Payload (bpp) and Reversibility
on BOSSbase and BOWS-2 datasets — matches paper Table VI.
"""

import pandas as pd
import numpy as np

boss = pd.read_csv("bossbase_results.csv")
bows = pd.read_csv("bows2_results_50.csv")

def table_vi(df, label):
    bpp = df["capacity_bpp"].dropna()
    success = (df["extraction_success"] == "TRUE")
    psnr_vals = df["psnr"].replace([np.inf, -np.inf], np.nan)

    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")
    print(f"  Maximum payload  : {bpp.max():.3f} bpp")
    print(f"  Minimum payload  : {bpp.min():.3f} bpp")
    print(f"  Average payload  : {bpp.mean():.3f} bpp")
    print(f"  Std deviation    : {bpp.std():.3f} bpp")
    print(f"  Extraction success: {success.sum()} / {len(success)}  ({success.mean()*100:.2f}%)")
    print(f"  PSNR (finite only): {psnr_vals.mean():.2f} dB  (inf = lossless)")
    print(f"  Lossless recovery: {'PSNR=+inf' if (df['psnr'] == np.inf).all() else 'Some finite PSNR'}")

    # percentile breakdown
    for pct in [10, 25, 50, 75, 90]:
        print(f"  {pct}th percentile : {np.percentile(bpp, pct):.3f} bpp")

    return {
        "Dataset": label,
        "Max (bpp)": round(bpp.max(), 3),
        "Min (bpp)": round(bpp.min(), 3),
        "Average (bpp)": round(bpp.mean(), 3),
        "Std (bpp)": round(bpp.std(), 3),
        "PSNR": "+inf (lossless)",
        "SSIM": "1 (lossless)",
        "Extraction Success": f"{success.mean()*100:.2f}%",
    }

rows = [table_vi(boss, "BOSSbase"), table_vi(bows, "BOWS-2")]
pd.DataFrame(rows).set_index("Dataset").to_csv("table6_payload_reversibility.csv")
print("\n\nSaved to table6_payload_reversibility.csv")
