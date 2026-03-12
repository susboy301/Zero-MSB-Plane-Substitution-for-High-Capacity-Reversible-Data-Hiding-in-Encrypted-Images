"""
TABLE III: Statistical Analysis of Results
Generates summary statistics (correlation, entropy, chi2, NPCR, UACI)
for BOSSbase and BOWS-2 datasets — matching paper Table III style.
"""

import pandas as pd
import numpy as np

# ── Load ──────────────────────────────────────────────────────────────────────
boss = pd.read_csv("bossbase_results.csv")
bows = pd.read_csv("bows2_results_50.csv")

def summarise(df, label):
    numeric = df.select_dtypes(include=np.number)
    metrics = {
        "Dataset"          : label,
        "Corr_H (mean)"    : f"{numeric['correlation_h_enc'].mean():.4f}",
        "Corr_H (std)"     : f"{numeric['correlation_h_enc'].std():.4f}",
        "Corr_V (mean)"    : f"{numeric['correlation_v_enc'].mean():.4f}",
        "Corr_V (std)"     : f"{numeric['correlation_v_enc'].std():.4f}",
        "Entropy (mean)"   : f"{numeric['entropy_enc'].mean():.4f}",
        "Entropy (std)"    : f"{numeric['entropy_enc'].std():.4f}",
        "Chi2 (mean)"      : f"{numeric['chi2_enc'].mean():.2f}",
        "Chi2 (std)"       : f"{numeric['chi2_enc'].std():.2f}",
        "NPCR (mean %)"    : f"{numeric['npcr'].mean():.2f}",
        "NPCR (std)"       : f"{numeric['npcr'].std():.2f}",
        "UACI (mean %)"    : f"{numeric['uaci'].mean():.2f}",
        "UACI (std)"       : f"{numeric['uaci'].std():.2f}",
        "Capacity (mean bpp)": f"{numeric['capacity_bpp'].mean():.4f}",
        "Capacity (max bpp)": f"{numeric['capacity_bpp'].max():.4f}",
        "Capacity (min bpp)": f"{numeric['capacity_bpp'].min():.4f}",
        "Extraction Success": f"{(df['extraction_success'] == 'TRUE').mean()*100:.2f}%",
    }
    return metrics

rows = [summarise(boss, "BOSSbase"), summarise(bows, "BOWS-2")]
result = pd.DataFrame(rows).set_index("Dataset").T
print(result.to_string())
result.to_csv("table3_statistical_analysis.csv")
print("\nSaved to table3_statistical_analysis.csv")
