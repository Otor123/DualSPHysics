#!/usr/bin/env python3
"""
Overlay plots for symmetry CSV exports.

Reads one or more dataset pairs:
  - *_full.csv  (per-index table)
  - *_pairs.csv (per-pair table)

and overlays them into the same 5 plots:
  1) profile: y + analytical
  2) pointwise error vs analytical
  3) abs symmetry diff per pair
  4) rel symmetry error per pair (%)
  5) rel symmetry error vs umax per pair (%)

Usage examples:
  python3 CompareSymmetriePlot.py \
    --set small:symmetry_smallOneV2_full.csv:symmetry_smallOneV2_pairs.csv \
    --set big:symmetry_bigOneV2_full.csv:symmetry_bigOneV2_pairs.csv \
    --show

  python3 CompareSymmetriePlot.py \
    --set small:symmetry_smallOneV2_full.csv:symmetry_smallOneV2_pairs.csv \
    --set big:symmetry_bigOneV2_full.csv:symmetry_bigOneV2_pairs.csv \
    --outdir plots --prefix compare_small_big

  python3 CompareSymmetriePlot.py \
    --set small:symmetry_smallOneV2_full.csv:symmetry_smallOneV2_pairs.csv \
    --set big:symmetry_smallOneV2__setDRWTrue_full.csv:symmetry_smallOneV2_setDRWTrue_pairs.csv \
    --outdir plots --prefix compare_small_big

  python3 CompareSymmetriePlot.py \
    --set small:symmetry_smallOneV2_full.csv:symmetry_smallOneV2_pairs.csv \
    --set big:symmetry_smallOneV2__setDRWTrue_full.csv:symmetry_smallOneV2_setDRWTrue_pairs.csv \
    --outdir plots --prefix compare_small_big    

    
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class DataSet:
    name: str
    full_path: Path
    pairs_path: Path
    full: pd.DataFrame
    pairs: pd.DataFrame


def read_semicolon_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    return pd.read_csv(path, sep=";")


def parse_set_arg(s: str) -> tuple[str, Path, Path]:
    """
    Expected: NAME:FULL_CSV:PAIRS_CSV
    """
    parts = s.split(":", 2)
    if len(parts) != 3:
        raise ValueError(
            f"Invalid --set '{s}'. Expected format: NAME:FULL_CSV:PAIRS_CSV"
        )
    name, full, pairs = parts[0].strip(), Path(parts[1]).expanduser(), Path(parts[2]).expanduser()
    if not name:
        raise ValueError(f"Invalid --set '{s}': NAME is empty.")
    return name, full, pairs


def safe_has_col(df: pd.DataFrame, col: str) -> bool:
    return col in df.columns and df[col].notna().any()


def plot_overlay(datasets: List[DataSet]) -> List[plt.Figure]:
    figs: List[plt.Figure] = []

    # 1) profile y + analytical
    fig = plt.figure()
    for ds in datasets:
        plt.plot(ds.full["i"], ds.full["y"], marker="o")
        if safe_has_col(ds.full, "analytical"):
            plt.plot(ds.full["i"], ds.full["analytical"], marker="o")
    plt.xlabel("Index i")
    plt.ylabel("Value")
    plt.title("Profiles overlay (y + analytical)")
    plt.grid(True)

    # Build legend labels in the same order we plotted
    labels = []
    for ds in datasets:
        labels.append(f"{ds.name} y")
        if safe_has_col(ds.full, "analytical"):
            labels.append(f"{ds.name} analytical")
    plt.legend(labels)
    figs.append(fig)

    # 2) pointwise error vs analytical
    fig = plt.figure()
    for ds in datasets:
        if safe_has_col(ds.full, "err_vs_analytical_pct"):
            plt.plot(ds.full["i"], ds.full["err_vs_analytical_pct"], marker="o")
    plt.xlabel("Index i")
    plt.ylabel("Error vs analytical [%]")
    plt.title("Pointwise error vs analytical")
    plt.grid(True)
    plt.legend([ds.name for ds in datasets if safe_has_col(ds.full, "err_vs_analytical_pct")])
    figs.append(fig)

    # 3) abs symmetry diff per pair
    fig = plt.figure()
    for ds in datasets:
        plt.plot(ds.pairs["pair_i"], ds.pairs["abs_diff"], marker="o")
    plt.xlabel("Pair index (left side i)")
    plt.ylabel("|y[i] - y[n-1-i]|")
    plt.title("Symmetry absolute error per mirrored pair")
    plt.grid(True)
    plt.legend([ds.name for ds in datasets])
    figs.append(fig)

    # 4) relative symmetry error per pair (%)
    fig = plt.figure()
    for ds in datasets:
        plt.plot(ds.pairs["pair_i"], ds.pairs["rel_sym_err_pct"], marker="o")
    plt.xlabel("Pair index (left side i)")
    plt.ylabel("Relative symmetry error [%]")
    plt.title("Symmetry relative error per mirrored pair")
    plt.grid(True)
    plt.legend([ds.name for ds in datasets])
    figs.append(fig)

    # 5) relative symmetry error vs umax per pair (%)
    fig = plt.figure()
    for ds in datasets:
        plt.plot(ds.pairs["pair_i"], ds.pairs["rel_sym_err_pct_umax"], marker="o")
    plt.xlabel("Pair index (left side i)")
    plt.ylabel("Relative symmetry error vs umax [%]")
    plt.title("Symmetry relative error vs umax per mirrored pair")
    plt.grid(True)
    plt.legend([ds.name for ds in datasets])
    figs.append(fig)

    return figs


def save_figs(figs: List[plt.Figure], outdir: Path, prefix: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    names = [
        "01_profile",
        "02_err_vs_analytical",
        "03_sym_abs",
        "04_sym_rel",
        "05_sym_rel_umax",
    ]
    for fig, name in zip(figs, names):
        out = outdir / f"{prefix}_{name}.png"
        fig.savefig(out, dpi=200, bbox_inches="tight")
        print(f"Saved: {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Overlay plots for symmetry CSV exports.")
    ap.add_argument(
        "--set",
        action="append",
        default=[],
        help="Dataset triple: NAME:FULL_CSV:PAIRS_CSV (repeatable).",
    )
    ap.add_argument("--outdir", type=str, default="", help="If set, save PNGs into this folder.")
    ap.add_argument("--prefix", type=str, default="symmetry_overlay", help="Filename prefix for saved plots.")
    ap.add_argument("--show", action="store_true", help="Show plots interactively.")
    args = ap.parse_args()

    if not args.set:
        raise SystemExit(
            "No datasets provided. Use --set NAME:FULL_CSV:PAIRS_CSV (repeatable)."
        )

    datasets: List[DataSet] = []
    for s in args.set:
        name, full_path, pairs_path = parse_set_arg(s)
        full = read_semicolon_csv(full_path)
        pairs = read_semicolon_csv(pairs_path)

        # basic sanity checks
        for col in ["i", "y"]:
            if col not in full.columns:
                raise ValueError(f"{name}: missing column '{col}' in {full_path}")
        for col in ["pair_i", "abs_diff", "rel_sym_err_pct", "rel_sym_err_pct_umax"]:
            if col not in pairs.columns:
                raise ValueError(f"{name}: missing column '{col}' in {pairs_path}")

        datasets.append(DataSet(name, full_path, pairs_path, full, pairs))

    figs = plot_overlay(datasets)

    if args.outdir:
        save_figs(figs, Path(args.outdir).expanduser(), args.prefix)

    if args.show or not args.outdir:
        plt.show()


if __name__ == "__main__":
    main()
