#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute temperature difference: ΔT(x) = T_sim(x) - T_analytic(x)

Works with either:
A) Analytic file already contains x, T_sim, T_analytic (like your Test.csv)
   -> then it will just compute/overwrite delta columns and export.

B) Simulation file contains Points:0 and Temp (like Temp_over_Points0.csv),
   analytic file contains x and T_analytic
   -> then it interpolates T_analytic onto sim x and computes delta.

Outputs:
- sim_minus_analytic_diff.csv (semicolon-separated)
- sim_minus_analytic_diff.png (plot)

Usage examples:
  python paraviewConverterVSC.py --ana Test.csv
  python diff_sim_analytic.py --sim Temp_over_Points0.csv --ana analytic.csv
"""

from __future__ import annotations
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_csv_flexible(path: Path) -> pd.DataFrame:
    """Try ';' first, then ','."""
    try:
        df = pd.read_csv(path, sep=";")
        # if it parsed as single column, fallback to comma
        if df.shape[1] == 1:
            df = pd.read_csv(path)
        return df
    except Exception:
        return pd.read_csv(path)


def find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Find first column whose lowercase name contains any candidate substring."""
    cols = list(df.columns)
    low = [str(c).strip().lower() for c in cols]
    for cand in candidates:
        for i, c in enumerate(low):
            if cand in c:
                return cols[i]
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", type=str, default="", help="Simulation CSV (optional). Example: Temp_over_Points0.csv")
    ap.add_argument("--ana", type=str, required=True, help="Analytic CSV. Example: Test.csv")
    ap.add_argument("--out_csv", type=str, default="sim_minus_analytic_diff.csv", help="Output CSV (semicolon-separated)")
    ap.add_argument("--out_png", type=str, default="sim_minus_analytic_diff.png", help="Output plot PNG")
    args = ap.parse_args()

    ana_path = Path(args.ana)
    if not ana_path.exists():
        raise FileNotFoundError(f"Analytic file not found: {ana_path}")

    ana = read_csv_flexible(ana_path)

    # --- Case A: analytic file already has x, T_sim, T_analytic
    x_col_a = find_col(ana, ["x", "points:0", "points0"])
    sim_col_a = find_col(ana, ["t_sim", "sim"])
    ana_col_a = find_col(ana, ["t_analytic", "analytic", "ana"])

    if x_col_a and sim_col_a and ana_col_a:
        out = ana[[x_col_a, sim_col_a, ana_col_a]].copy()
        out["delta_T_sim_minus_ana"] = out[sim_col_a] - out[ana_col_a]
        out["abs_error"] = out["delta_T_sim_minus_ana"].abs()
        out["pct_error_of_ana"] = np.where(
            out[ana_col_a] != 0,
            100.0 * out["delta_T_sim_minus_ana"] / out[ana_col_a],
            np.nan,
        )

    else:
        # --- Case B: need sim file + analytic file with x, T_analytic
        sim_path = Path(args.sim)
        if not sim_path.exists():
            raise ValueError(
                "Could not detect (x, T_sim, T_analytic) in the analytic CSV.\n"
                "Provide --sim with simulation CSV (e.g. Temp_over_Points0.csv)."
            )

        sim = read_csv_flexible(sim_path)

        # simulation expected cols
        x_sim_col = find_col(sim, ["points:0", "points0", "x"])
        t_sim_col = find_col(sim, ["temp", "t_sim", "t"])

        if not x_sim_col or not t_sim_col:
            raise ValueError(f"Could not find simulation columns in {sim_path.name}. "
                             f"Found columns: {list(sim.columns)}")

        # analytic expected cols
        x_ana_col = find_col(ana, ["x", "points:0", "points0"])
        t_ana_col = find_col(ana, ["t_analytic", "analytic", "ana", "temp"])

        if not x_ana_col or not t_ana_col:
            raise ValueError(f"Could not find analytic columns in {ana_path.name}. "
                             f"Found columns: {list(ana.columns)}")

        # Sort for interpolation stability
        sim = sim.sort_values(x_sim_col)
        ana = ana.sort_values(x_ana_col)

        x_sim = sim[x_sim_col].to_numpy(dtype=float)
        t_sim = sim[t_sim_col].to_numpy(dtype=float)

        x_ana = ana[x_ana_col].to_numpy(dtype=float)
        t_ana = ana[t_ana_col].to_numpy(dtype=float)

        # Interpolate analytic onto sim x (clamp ends)
        t_ana_interp = np.interp(x_sim, x_ana, t_ana)

        out = pd.DataFrame({
            "x [m]": x_sim,
            "T_sim": t_sim,
            "T_analytic": t_ana_interp,
        })
        out["delta_T_sim_minus_ana"] = out["T_sim"] - out["T_analytic"]
        out["abs_error"] = out["delta_T_sim_minus_ana"].abs()
        out["pct_error_of_ana"] = np.where(
            out["T_analytic"] != 0,
            100.0 * out["delta_T_sim_minus_ana"] / out["T_analytic"],
            np.nan,
        )

    # Metrics
    rmse = float(np.sqrt(np.mean(out["delta_T_sim_minus_ana"] ** 2)))
    mae = float(np.mean(out["abs_error"]))
    max_abs = float(out["abs_error"].max())
    idx_max = int(out["abs_error"].idxmax())
    x_at_max = float(out.iloc[idx_max, 0])  # first column is x

    print(f"RMSE: {rmse:.6g} K")
    print(f"MAE : {mae:.6g} K")
    print(f"Max |error|: {max_abs:.6g} K at x={x_at_max:.6g} m")

    # Export
    out_csv = Path(args.out_csv)
    out.to_csv(out_csv, index=False, sep=";")
    print(f"Wrote: {out_csv.resolve()}")

    # Plot
    plt.figure()
    plt.plot(out.iloc[:, 0], out["delta_T_sim_minus_ana"])
    plt.xlabel("x [m]")
    plt.ylabel("ΔT = T_sim - T_analytic [K]")
    plt.title("Simulation - Analytic Temperature Difference")
    plt.grid(True)
    out_png = Path(args.out_png)
    plt.savefig(out_png, dpi=200, bbox_inches="tight")
    print(f"Wrote: {out_png.resolve()}")


if __name__ == "__main__":
    main()
