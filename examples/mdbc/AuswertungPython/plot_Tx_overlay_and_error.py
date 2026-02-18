#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate two plots from the three comparison CSVs:
1) T(x): analytic (solid) vs simulation (dashed) for each CSV
2) Error over x: (sim - analytic) for each CSV

Expected CSV columns (as in your files):
- x [m]
- T_sim [K]
- T_analytic [K]
- sim - analytic [K]

Usage examples:

  python plot_Tx_overlay_and_error.py --csv T_x_comparison_tableV2.csv --csv T_x_comparison_tableV2_dp_lower.csv --csv T_x_comparison_tableV2_dp_lowerlower.csv --csv T_x_comparison_tableV2_dp_lowerlowerlower.csv --labels V2 V2_dp_lower V2_dp_lowerlower V2_dp_lowerlowerlower --out_prefix T_x --smooth none 

  python plot_Tx_overlay_and_error.py --csv T_x_comparison_tableV2_dp_0.0001.csv --csv T_x_comparison_tableV2_dp_0.00005.csv --csv T_x_comparison_tableV2_dp_0.000025.csv --csv T_x_comparison_tableV2_dp_0.0000125.csv --labels dp_0.0001 dp_0.00005 dp_0.0000025 dp_0.00000125 --out_prefix T_x --smooth none 


  python plot_Tx_overlay_and_error.py \
    --csv T_x_comparison_tableV2.csv \
    --csv T_x_comparison_tableV2_dp_lower.csv \
    --csv T_x_comparison_tableV2_dp_lowerlower.csv \
    --labels V2 V2_dp_lower V2_dp_lowerlower \
    --out_prefix T_x \
    --smooth ma \
    --smooth_window 9


python plot_Tx_overlay_and_error.py --csv T_x_comparison_tableV2.csv --csv T_x_comparison_tableV2_dp_lower.csv --csv T_x_comparison_tableV2_dp_lowerlower.csv --smooth savgol --smooth_window 10 --savgol_poly 3


If you omit --labels, the script uses the file stem as label.
Output files:
  <out_prefix>_T_overlay.png
  <out_prefix>_sim_minus_analytic.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

COL_X = "x [m]"
COL_SIM = "T_sim [K]"
COL_ANA = "T_analytic [K]"
COL_DIFF = "sim - analytic [K]"


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in (COL_X, COL_SIM, COL_ANA, COL_DIFF) if c not in df.columns]
    if missing:
        raise ValueError(
            f"{path} is missing columns {missing}. "
            f"Found columns: {list(df.columns)}"
        )
    return df


def smooth_series(y: pd.Series, mode: str, window: int, polyorder: int) -> pd.Series:
    if mode == "none" or window <= 1:
        return y

    if mode == "ma":
        # centered moving average
        return y.rolling(window=window, center=True, min_periods=1).mean()

    if mode == "savgol":
        try:
            from scipy.signal import savgol_filter
        except ImportError as e:
            raise SystemExit(
                "You selected --smooth savgol but SciPy is not installed.\n"
                "Install it via: pip install scipy\n"
                "Or use: --smooth ma"
            ) from e

        # SavGol needs odd window and window > polyorder
        w = int(window)
        if w % 2 == 0:
            w += 1
        if w <= polyorder:
            w = polyorder + 2
            if w % 2 == 0:
                w += 1

        y_np = y.to_numpy()
        y_f = savgol_filter(y_np, window_length=w, polyorder=polyorder, mode="interp")
        return pd.Series(y_f, index=y.index)

    raise ValueError(f"Unknown smoothing mode: {mode}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Plot T(x) overlay + error from comparison CSVs.")
    ap.add_argument("--csv", action="append", required=True,
                    help="Path to a comparison CSV. Provide this flag 3 times for 3 CSVs.")
    ap.add_argument("--labels", nargs="*", default=None,
                    help="Optional labels for each CSV (same order as --csv).")
    ap.add_argument("--out_prefix", default="T_x",
                    help="Output prefix for PNG files (default: T_x).")

    # NEW:
    ap.add_argument("--smooth", choices=["none", "ma", "savgol"], default="none",
                    help="Smoothing mode: none, ma (moving average), savgol (Savitzky-Golay).")
    ap.add_argument("--smooth_window", type=int, default=11,
                    help="Smoothing window size (ma: any int, savgol: will be forced odd). Default: 11")
    ap.add_argument("--savgol_poly", type=int, default=3,
                    help="Savitzky-Golay polynomial order (default: 3).")

    args = ap.parse_args()

    csv_paths = [Path(p) for p in args.csv]
    labels = args.labels
    if labels is None or len(labels) == 0:
        labels = [p.stem for p in csv_paths]
    if len(labels) != len(csv_paths):
        raise SystemExit(
            f"Number of labels ({len(labels)}) must match number of CSVs ({len(csv_paths)})."
        )

    colors = ["green", "orange", "blue", "red"]

    # ---- Plot 1: T(x) overlay (analytic solid, sim dashed) ----
    plt.figure(figsize=(9, 5.5))
    for i, (p, lab) in enumerate(zip(csv_paths, labels)):
        df = load_csv(p)

        x = df[COL_X]
        tsim = smooth_series(df[COL_SIM], args.smooth, args.smooth_window, args.savgol_poly)
        tana = smooth_series(df[COL_ANA], args.smooth, args.smooth_window, args.savgol_poly)

        color = colors[i] if i < len(colors) else None
        plt.plot(x, tsim, linestyle="--", color=color, label=f"{lab} sim")
        plt.plot(x, tana, linestyle="-", color=color, alpha=0.9, label=f"{lab} analytic")

    plt.xlabel("x [m]")
    plt.ylabel("Temperature [K]")
    plt.title("T(x): Simulation vs Analytic")
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=2, fontsize=9)
    plt.tight_layout()
    out1 = Path(f"{args.out_prefix}_T_overlay.png")
    plt.savefig(out1, dpi=200)

    # ---- Plot 2: error (sim - analytic) over x ----
    plt.figure(figsize=(9, 5.5))
    for i, (p, lab) in enumerate(zip(csv_paths, labels)):
        df = load_csv(p)

        x = df[COL_X]
        diff = smooth_series(df[COL_DIFF], args.smooth, args.smooth_window, args.savgol_poly)

        color = colors[i] if i < len(colors) else None
        plt.plot(x, diff, color=color, label=lab)

    plt.axhline(0, linewidth=1, alpha=0.5)
    plt.xlabel("x [m]")
    plt.ylabel("sim − analytic [K]")
    plt.title("Temperature error over x")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    out2 = Path(f"{args.out_prefix}_sim_minus_analytic.png")
    plt.savefig(out2, dpi=200)

    print(f"Saved: {out1.resolve()}")
    print(f"Saved: {out2.resolve()}")
    plt.show()


if __name__ == "__main__":
    main()
