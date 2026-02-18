#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combine and plot temperature-vs-time curves from:
1) an analytic CSV (e.g. T_vs_time_analytic_x005mm_z002mm.csv)
2) a simulation CSV (e.g. T_vs_time_all_Simulation.csv)

Expected (flexible) CSV formats:
- Semicolon-separated (preferred) or comma-separated.
- Time column named: "time_s" (preferred) or "Time_s" or otherwise first column.
- All remaining columns are treated as temperature columns.

Outputs:
- A single plot with all curves vs time.
- Optionally saves to PNG.

Usage:
  python plot_Simulation_Analytical_Temperatur.py \
    --analytic T_vs_time_analytic_x005mm_z002mm.csv \
    --simulation T_vs_time_all_Simulation_z002mm.csv

  python plot_Simulation_Analytical_Temperatur.py \
    --analytic T_vs_time_analytic_x005mm_z002mm.csv \
    --simulation T_vs_time_all_Simulation.csv \
    --out_png T_vs_time_combined_z002mm.png    

  python plot_Simulation_Analytical_Temperatur.py \
    --analytic T_vs_time_analytic_x005mm_z004mm.csv \
    --simulation T_vs_time_all_Simulation.csv \
    --out_png T_vs_time_combined_z004mm.png

  python plot_Simulation_Analytical_Temperatur.py \
    --analytic T_vs_time_analytic_x005mm_z006mm.csv \
    --simulation T_vs_time_all_Simulation.csv \
    --out_png T_vs_time_combined_z006mm.png    

  python plot_Simulation_Analytical_Temperatur.py \
    --analytic T_vs_time_analytic_x005mm_z004mm.csv \
    --simulation temp_vs_time_1D.csv \
    --out_png T_vs_time_combined_z004mm1D.png       

  python plot_Simulation_Analytical_Temperatur.py \
    --analytic T_vs_time_analytic_x005mm_z002mm.csv \
    --simulation temp_vs_time_1D.csv \
    --out_png T_vs_time_combined_z002mm1D.png   

  python plot_Simulation_Analytical_Temperatur.py \
    --analytic T_vs_time_analytic_x005mm_z006mmV2.csv \
    --simulation T_vs_time_all_Simulation.csv \
    --out_png T_vs_time_combined_z006mmV2.png   

  python plot_Simulation_Analytical_Temperatur.py \
    --analytic T_vs_time_analytic_x005mm_z004mmV2.csv \
    --simulation T_vs_time_all_Simulation.csv \
    --out_png T_vs_time_combined_z004mmV2.png        

  python plot_Simulation_Analytical_Temperatur.py \
    --analytic T_vs_time_analytic_x005mm_z002mmV2.csv \
    --simulation T_vs_time_all_Simulation.csv \
    --out_png T_vs_time_combined_z002mmV2.png  

python plot_Simulation_Analytical_Temperatur.py \
  --analytic T_vs_time_analytic_x005mm_z002mmV2.csv T_vs_time_analytic_x005mm_z004mmV2.csv T_vs_time_analytic_x005mm_z006mmV2.csv \
  --simulation T_vs_time_all_Simulation.csv \
  --out_png T_vs_time_combined.png   

python plot_Simulation_Analytical_Temperatur.py \
  --analytic T_vs_time_analytic_x005mm_z002mmV3_top.csv \
  --simulation _PointsTempConvergenz_Temp_with_Top_test.csv\
  --out_png T_vs_time_TEST.png   

python plot_Simulation_Analytical_Temperatur.py \
  --analytic T_vs_time_analytic_x005mm_z004mmV3_top.csv \
  --simulation _PointsTempConvergenz_Temp_with_Top_test.csv\
  --out_png T_vs_time_TEST.png   

python plot_Simulation_Analytical_Temperatur.py \
  --analytic T_vs_time_analytic_x005mm_z006mmV3_top.csv \
  --simulation _PointsTempConvergenz_Temp_with_Top_test.csv\
  --out_png T_vs_time_TEST.png             

python plot_Simulation_Analytical_Temperatur.py \
  --analytic T_vs_time_analytic_x005mm_z002mmV3_top.csv T_vs_time_analytic_x005mm_z004mmV3_top.csv T_vs_time_analytic_x005mm_z006mmV3_top.csv \
  --simulation _PointsTempConvergenz_Temp_with_Top_test.csv\
  --out_png T_vs_time_TEST.png  


python plot_Simulation_Analytical_Temperatur.py \
  --analytic T_vs_time_analytic_x005mm_z002mmV4_top.csv T_vs_time_analytic_x005mm_z004mmV4_top.csv \
  --simulation _PointsTempConvergenz_Temp_quader_gravtiy_Zero.csv\
  --out_png T_vs_time_TEST.png  

  

"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import pandas as pd
import matplotlib.pyplot as plt


def read_flexible_csv(path: Path) -> pd.DataFrame:
    """
    Read CSV that may be semicolon or comma separated.
    First try ';', then fall back to default (comma).
    """
    try:
        df = pd.read_csv(path, sep=";")
        if df.shape[1] < 2:
            raise ValueError("Too few columns with semicolon separator.")
        return df
    except Exception:
        return pd.read_csv(path)


def detect_time_col(df: pd.DataFrame) -> str:
    """Pick a time column name if present; otherwise use the first column."""
    if "time_s" in df.columns:
        return "time_s"
    if "Time_s" in df.columns:
        return "Time_s"
    return df.columns[0]


def to_numeric_sorted(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """Convert columns to numeric where possible and sort by time."""
    df = df.copy()
    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")
    for c in df.columns:
        if c == time_col:
            continue
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=[time_col]).sort_values(time_col)
    return df


def get_temp_cols(df: pd.DataFrame, time_col: str) -> List[str]:
    """All columns except time are treated as temperature columns."""
    return [c for c in df.columns if c != time_col]


def pretty_stem(p: Path) -> str:
    """Short label from filename."""
    return p.stem


def main() -> None:
    ap = argparse.ArgumentParser(description="Plot analytic + simulation temperature curves vs time.")
    # NOTE: nargs="+" means: one or more files allowed
    ap.add_argument(
        "--analytic",
        type=Path,
        nargs="+",
        required=True,
        help="Path(s) to analytic CSV(s). Provide one or many.",
    )
    ap.add_argument("--simulation", type=Path, required=True, help="Path to simulation CSV.")
    ap.add_argument("--out_png", type=Path, default=None, help="If set, save plot to this PNG path.")
    ap.add_argument("--title", type=str, default="Temperature vs time", help="Plot title.")
    args = ap.parse_args()

    # --- Simulation ---
    sim = read_flexible_csv(args.simulation)
    sim_time = detect_time_col(sim)
    sim = to_numeric_sorted(sim, sim_time)
    sim_temp_cols = get_temp_cols(sim, sim_time)

    plt.figure()

    # --- Analytic (multiple files) ---
    for ana_path in args.analytic:
        ana = read_flexible_csv(ana_path)
        ana_time = detect_time_col(ana)
        ana = to_numeric_sorted(ana, ana_time)
        ana_temp_cols = get_temp_cols(ana, ana_time)

        label_prefix = pretty_stem(ana_path)

        # Often there is just one temp column; but we support multiple.
        for c in ana_temp_cols:
            # If there are multiple temp cols, add them to label
            suffix = f":{c}" if len(ana_temp_cols) > 1 else ""
            plt.plot(
                ana[ana_time].to_numpy(),
                ana[c].to_numpy(),
                label = f"Analytic (z = {c} mm)"
                # label=f"Analytic ({label_prefix}{suffix})",
            )

    # --- Simulation curves (often multiple) ---
    sim_label_prefix = pretty_stem(args.simulation)
    for c in sim_temp_cols:
        plt.plot(
            sim[sim_time].to_numpy(),
            sim[c].to_numpy(),
            # label=f"Simulation ({sim_label_prefix}:{c})" if len(sim_temp_cols) > 1 else f"Simulation ({sim_label_prefix})",
            label = f"Simulation (z = {c} mm)"
        )

    plt.title(args.title)
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.grid(True)
    plt.legend()

    if args.out_png is not None:
        args.out_png.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(args.out_png, dpi=200, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
