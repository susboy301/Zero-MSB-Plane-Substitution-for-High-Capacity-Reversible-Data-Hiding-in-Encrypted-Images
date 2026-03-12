"""
MASTER ANALYSIS SCRIPT
=======================
Run this from the directory containing your CSV files.
Generates all tables and figures needed for journal publication.

Usage:
    python run_all_analysis.py

Output files:
    Tables (CSV):
        table3_statistical_analysis.csv
        table6_payload_reversibility.csv

    Figures (PNG + PDF):
        fig_capacity_distribution_both.{png,pdf}
        fig_capacity_bossbase.{png,pdf}
        fig_capacity_bows2.{png,pdf}
        fig_zero_plane_distribution.{png,pdf}
        fig_cumulative_zero_plane.{png,pdf}
        fig_correlation_distribution.{png,pdf}
        fig_entropy_distribution.{png,pdf}
        fig_chi2_distribution.{png,pdf}
        fig_npcr_uaci_distribution.{png,pdf}
        fig_capacity_vs_npcr.{png,pdf}
        fig_comparison_bossbase.{png,pdf}
        fig_comparison_bows2.{png,pdf}
        fig_comparison_both_datasets.{png,pdf}
        fig_capacity_cdf.{png,pdf}
"""

import subprocess, sys, os

scripts = [
    "table3_statistical_analysis.py",
    "table6_payload_reversibility.py",
    "fig_capacity_distribution.py",
    "fig_zero_plane_distribution.py",
    "fig_security_analysis.py",
    "fig_comparison_sota.py",
    "fig_capacity_cdf.py",
]

print("=" * 60)
print("  RDHEI Publication Analysis — Master Runner")
print("=" * 60)

for script in scripts:
    print(f"\n▶  Running {script} ...")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(result.stdout.strip())
        print(f"   ✅  {script} completed.")
    else:
        print(f"   ❌  {script} FAILED:")
        print(result.stderr[-800:])

print("\n" + "=" * 60)
print("  All outputs generated.")
print("=" * 60)
