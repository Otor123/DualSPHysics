#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Overlay + Difference plot: Simulation vs Analytic temperature vs time (z = 0.002 m)

- Reads simulation CSV: expects columns like
    time_s ; temperature_K_z0.002m ; temperature_K_z0.004m ; temperature_K_z0.006m ...
- Reads analytic CSV: expects columns like
    time_s ; temperature_K

- Overlays T(t) curves
- Computes ΔT(t) = T_sim(t) - T_ana(t) on the simulation time grid
  (analytic is interpolated to simulation time stamps)

Usage:
  python compare_temp_time_z002.py \
    --sim /path/to/T_vs_time_all_Simulation.csv \
    --ana /path/to/T_vs_time_analytic_x005mm_z002mmV2.csv \
    --z 0.002

  python compare_temp_time_z002.py \
    --sim T_vs_time_all_Simulation.csv \
    --ana T_vs_time_analytic_x005mm_z002mmV2.csv \
    --z 0.002 \
    --out_prefix z002  

  python compare_temp_time_z002.py \
    --sim T_vs_time_all_Simulation.csv \
    --ana T_vs_time_analytic_x005mm_z004mmV2.csv \
    --z 0.004 \
    --out_prefix z004  

  python compare_temp_time_z002.py \
    --sim T_vs_time_all_Simulation.csv \
    --ana T_vs_time_analytic_x005mm_z006mmV2.csv \
    --z 0.006 \
    --out_prefix z006  

  python compare_temp_time_z002.py \
    --sim T_vs_time_all_Simulation.csv \
    --ana T_vs_time_analytic_x005mm_z002mmV2.csv \
    --z 0.002 \
    --out_csv diff_z002.csv   

  python compare_temp_time_z002.py \
    --sim T_vs_time_all_Simulation.csv \
    --ana T_vs_time_analytic_x005mm_z004mmV2.csv \
    --z 0.004 \
    --out_csv diff_z004.csv 

  python compare_temp_time_z002.py \
    --sim T_vs_time_all_Simulation.csv \
    --ana T_vs_time_analytic_x005mm_z006mmV2.csv \
    --z 0.006 \
    --out_csv diff_z006.csv     

  python compare_temp_time_z002.py \
    --sim _PointsTempConvergenz_Temp_with_Top.csv \
    --ana T_vs_time_analytic_x005mm_z006mmV2.csv \
    --z 0.006 \
    --out_csv diff_z006.csv   

  python compare_temp_time_z002.py \
    --sim T_vs_time_all_Simulation_converted.csv \
    --ana T_vs_time_analytic_x005mm_z002mmV4_long.csv \
    --z 0.002 \
    --out_csv diff_z002test.csv                
    

  python compare_temp_time_z002.py \
    --sim _PointsTempConvergenz_Temp_200secTest.csv \
    --ana T_vs_time_analytic_x005mm_z002mmV4_long.csv \
    --z 0.002 \
    --out_csv diff_z002test.csv           

  python compare_temp_time_z002.py \
    --sim _PointsTempConvergenz_Temp_200secTest.csv \
    --ana T_vs_time_analytic_x005mm_z004mmV4_long.csv \
    --z 0.004 \
    --out_csv diff_z004test.csv      

  python compare_temp_time_z002.py \
    --sim _PointsTempConvergenz_Temp_200secTest.csv \
    --ana T_vs_time_analytic_x005mm_z006mmV4_long.csv \
    --z 0.006 \
    --out_csv diff_z006test.csv                     

Optional:
  --out_prefix out_z002     (saves out_z002_overlay.png and out_z002_diff.png)
  --sep ;                  (CSV separator; default ';')
  --no_show                (do not open interactive windows)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_csv(path: Path, sep: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=sep)
    # Strip whitespace from column names just in case
    df.columns = [str(c).strip() for c in df.columns]
    return df


def find_sim_column(df_sim: pd.DataFrame, z: float) -> str:
    """
    Find the simulation column name matching a z value.
    By default expects: temperature_K_z0.002m for z=0.002

    If not found, tries a tolerant search.
    """
    target = f"temperature_K_z{z:.3f}m"  # e.g. z0.002m
    if target in df_sim.columns:
        return target

    # fallback: look for columns containing 'temperature' and 'z' and the numeric substring
    z_str = f"{z:.3f}".rstrip("0").rstrip(".")  # '0.002'
    candidates = [c for c in df_sim.columns if "temp" in c.lower() and "z" in c.lower()]
    for c in candidates:
        if z_str in c:
            return c

    raise KeyError(
        f"Could not find simulation temperature column for z={z}. "
        f"Tried '{target}'. Available columns: {list(df_sim.columns)}"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", required=True, type=Path, help="Simulation CSV (semicolon-separated by default).")
    ap.add_argument("--ana", required=True, type=Path, help="Analytic CSV (semicolon-separated by default).")
    ap.add_argument("--z", type=float, default=0.002, help="z position in meters (default: 0.002).")
    ap.add_argument("--sep", default=";", help="CSV separator (default: ';').")
    ap.add_argument("--out_prefix", default=None, help="If set, saves PNGs with this prefix.")
    ap.add_argument("--no_show", action="store_true", help="Do not show figures interactively.")
    ap.add_argument("--out_csv", type=Path, default=None,
                help="Optional: path to write CSV export (time, T_sim, T_ana_interp, dT, rel_err%). "
                     "If not set but --out_prefix is set, writes <out_prefix>_diff.csv")
    ap.add_argument("--export_rel_err", action="store_true",
                    help="Also export relative error in percent: 100*(T_sim-T_ana)/T_ana")
    args = ap.parse_args()

    df_sim = load_csv(args.sim, args.sep)
    df_ana = load_csv(args.ana, args.sep)

    # Required columns
    if "time_s" not in df_sim.columns:
        raise KeyError(f"Simulation CSV missing 'time_s'. Columns: {list(df_sim.columns)}")
    if "time_s" not in df_ana.columns:
        raise KeyError(f"Analytic CSV missing 'time_s'. Columns: {list(df_ana.columns)}")

    sim_col = find_sim_column(df_sim, args.z)

    # Extract arrays
    t_sim = df_sim["time_s"].to_numpy(dtype=float)
    T_sim = df_sim[sim_col].to_numpy(dtype=float)

    # Analytic temperature column
    if "temperature_K" in df_ana.columns:
        ana_col = "temperature_K"
    else:
        # fallback: first non-time column
        other_cols = [c for c in df_ana.columns if c != "time_s"]
        if not other_cols:
            raise KeyError(
                f"Analytic CSV has no temperature column. Columns: {list(df_ana.columns)}"
            )
        ana_col = other_cols[0]

    t_ana = df_ana["time_s"].to_numpy(dtype=float)
    T_ana = df_ana[ana_col].to_numpy(dtype=float)

    # Interpolate analytic onto simulation time grid
    T_ana_interp = np.interp(t_sim, t_ana, T_ana)

    # Difference
    dT = T_sim - T_ana_interp

    # Optional: CSV export
    out_csv = args.out_csv
    if out_csv is None and args.out_prefix:
        out_csv = Path(f"{args.out_prefix}_diff.csv")

    if out_csv is not None:
        export = pd.DataFrame({
            "time_s": t_sim,
            "T_sim_K": T_sim,
            "T_ana_interp_K": T_ana_interp,
            "dT_K": dT,
        })

    if args.export_rel_err:
        # avoid division by zero (shouldn't happen here, but safe)
        with np.errstate(divide="ignore", invalid="ignore"):
            rel = 100.0 * dT / T_ana_interp
        export["rel_err_percent"] = rel

    export.to_csv(out_csv, index=False, sep=args.sep)
    print(f"Saved: {out_csv.resolve()}")    

    # 1) Overlay plot
    plt.figure()
    plt.plot(t_sim, T_sim, label=f"Simulation ({sim_col})")
    plt.plot(t_ana, T_ana, label=f"Analytic ({ana_col})")
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.title(f"Temperature vs Time at z = {args.z:g} m")
    plt.legend()
    plt.tight_layout()

    if args.out_prefix:
        out1 = Path(f"{args.out_prefix}_overlay.png")
        plt.savefig(out1, dpi=200)
        print(f"Saved: {out1.resolve()}")

    # 2) Difference plot
    plt.figure()
    plt.plot(t_sim, dT, label="ΔT = T_sim - T_ana (interp)")
    plt.axhline(0.0)
    plt.xlabel("Time [s]")
    plt.ylabel("ΔT [K]")
    plt.title(f"Difference vs Time at z = {args.z:g} m")
    plt.legend()
    plt.tight_layout()

    if args.out_prefix:
        out2 = Path(f"{args.out_prefix}_diff.png")
        plt.savefig(out2, dpi=200)
        print(f"Saved: {out2.resolve()}")

    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
