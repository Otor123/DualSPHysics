#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot ΔT [K] over time for multiple z positions.

This script loads "diff" CSVs (e.g., diff_z002.csv, diff_z004.csv, diff_z006.csv),
auto-detects delimiter (semicolon/comma/whitespace) and column names, and plots ΔT(t).

Expected columns (flexible):
- a time column: contains "time" (e.g., time_s, Time [s], t, etc.)
- a delta-T column: contains "dt" or "dT" or "delta" (e.g., dT_K, ΔT, deltaT, etc.)

Usage:
  # Overlay all on one plot and show interactively
  python plot_dt_over_time_multi_z.py diff_z002.csv diff_z004.csv diff_z006.csv

  # Save overlay to PNG (no GUI)
  python plot_dt_over_time_multi_z.py diff_z002.csv diff_z004.csv diff_z006.csv --out overlay_dt.png

  # Also save individual plots per file
  python plot_dt_over_time_multi_z.py diff_z002.csv diff_z004.csv diff_z006.csv --out overlay_dt.png --save_individual

  # If auto-detection fails, specify columns explicitly
  python plot_dt_over_time_multi_z.py diff_z002.csv --time_col time_s --dt_col dT_K

  python plot_dt_over_time_multi_z.py diff_z002test.csv diff_z004test.csv diff_z006test.csv --out overlay_dtLong.png

  python plot_dt_over_time_multi_z.py diff_z002test.csv diff_z004test.csv diff_z006test.csv

Notes:
- The legend label is derived from the filename (tries to parse z002/z004/z006 etc.).
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def read_csv_flexible(path: Path) -> pd.DataFrame:
    """
    Read CSV with unknown delimiter. Tries: ';', ',', whitespace.
    """
    # Try common delimiters first for speed and better robustness
    for sep in [";", ",", r"\s+"]:
        try:
            df = pd.read_csv(path, sep=sep, engine="python")
            if df.shape[1] >= 2:
                return df
        except Exception:
            pass

    # Last resort: pandas autodetect (python engine)
    df = pd.read_csv(path, sep=None, engine="python")
    return df


def find_time_col(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    # First pass: keywords
    for c in cols:
        if "time" in str(c).lower() or re.fullmatch(r"t", str(c).strip().lower()):
            return c
    # Fallback: first column
    return cols[0]


def find_dt_col(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    # Strong hints first
    patterns = ["dt", "dT", "delta", "Δ"]
    for c in cols:
        cl = str(c).lower()
        if any(p.lower() in cl for p in patterns):
            # Avoid picking time column accidentally
            if "time" not in cl and cl.strip() != "t":
                return c
    # Fallback: second column
    if len(cols) >= 2:
        return cols[1]
    raise ValueError("Could not infer ΔT column (need at least 2 columns).")


def label_from_filename(p: Path) -> str:
    name = p.stem.lower()
    # Try patterns like z002, z004, z006
    m = re.search(r"z(\d{3})", name)
    if m:
        mm = int(m.group(1))  # e.g. 2,4,6 in mm if you encoded 002/004/006
        # If it's 002 => 0.002 m
        z_m = mm / 1000.0
        return f"z = {z_m:.3f} m"
    # Try z0.002 etc
    m = re.search(r"z0?([0-9]+(?:\.[0-9]+)?)", name)
    if m:
        return f"z = {m.group(1)}"
    return p.stem


def plot_overlay(dfs: list[tuple[str, pd.DataFrame]], time_col: str | None, dt_col: str | None, out: Path | None):
    plt.figure()
    for label, df in dfs:
        tc = time_col or find_time_col(df)
        dc = dt_col or find_dt_col(df)

        # Ensure numeric
        x = pd.to_numeric(df[tc], errors="coerce")
        y = pd.to_numeric(df[dc], errors="coerce")
        mask = x.notna() & y.notna()
        plt.plot(x[mask], y[mask], label=label)

    plt.xlabel("Time [s]")
    plt.ylabel("ΔT [K]")
    plt.title("ΔT over time for different z positions")
    plt.legend()
    plt.tight_layout()

    if out is not None:
        plt.savefig(out, dpi=200)
        print(f"[saved] {out}")
    else:
        plt.show()


def plot_individual(dfs: list[tuple[str, pd.DataFrame]], time_col: str | None, dt_col: str | None, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    for label, df in dfs:
        tc = time_col or find_time_col(df)
        dc = dt_col or find_dt_col(df)

        x = pd.to_numeric(df[tc], errors="coerce")
        y = pd.to_numeric(df[dc], errors="coerce")
        mask = x.notna() & y.notna()

        plt.figure()
        plt.plot(x[mask], y[mask])
        plt.xlabel("Time [s]")
        plt.ylabel("ΔT [K]")
        plt.title(f"ΔT over time ({label})")
        plt.tight_layout()

        safe = re.sub(r"[^a-zA-Z0-9_\-\.]+", "_", label)
        out = out_dir / f"dt_over_time_{safe}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print(f"[saved] {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csvs", nargs="+", help="Input diff CSV files (e.g., diff_z002.csv diff_z004.csv diff_z006.csv)")
    ap.add_argument("--time_col", default=None, help="Explicit name of the time column (optional)")
    ap.add_argument("--dt_col", default=None, help="Explicit name of the ΔT column (optional)")
    ap.add_argument("--out", default=None, help="Save overlay plot to this PNG (optional)")
    ap.add_argument("--save_individual", action="store_true", help="Also save individual plots per input file")
    ap.add_argument("--out_dir", default="dt_plots", help="Directory for individual plots (default: dt_plots)")

    args = ap.parse_args()

    dfs: list[tuple[str, pd.DataFrame]] = []
    for f in args.csvs:
        p = Path(f)
        df = read_csv_flexible(p)
        label = label_from_filename(p)
        dfs.append((label, df))

    out_path = Path(args.out) if args.out else None
    plot_overlay(dfs, args.time_col, args.dt_col, out_path)

    if args.save_individual:
        plot_individual(dfs, args.time_col, args.dt_col, Path(args.out_dir))


if __name__ == "__main__":
    main()
