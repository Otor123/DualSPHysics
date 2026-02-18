#!/usr/bin/env python3
"""
Heatmap of temperature evolution over time (x vs time) from DualSPHysics
MeasureTool output like: _PointsTemp_Temp.csv

- Reads semicolon-separated CSV
- Extracts x positions from first header row
- Builds T(time_index, x_index) temperature matrix (optionally sampled)
- Plots imshow heatmap with colorbar

python plot_temp_heatmap.py _PointsTemp_Temp.csv --drop-zero-ends

"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_points_temp_csv(path: str | Path) -> tuple[np.ndarray, pd.DataFrame]:
    path = Path(path)
    raw = pd.read_csv(path, sep=";", header=None)

    # x positions are stored in row 0, columns 2..end
    x = raw.iloc[0, 2:].astype(float).values

    # data starts at row 3
    data = raw.iloc[3:].copy()
    data[0] = pd.to_numeric(data[0], errors="coerce")  # Part
    data[1] = pd.to_numeric(data[1], errors="coerce")  # Time
    data = data.dropna(subset=[0, 1]).copy()

    data[0] = data[0].astype(int)
    return x, data


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="Path to _PointsTemp_Temp.csv")
    ap.add_argument("--max-rows", type=int, default=200,
                    help="Max number of time steps to plot (sampled evenly if more exist)")
    ap.add_argument("--drop-zero-ends", action="store_true",
                    help="Drop first+last x point if they are dummy endpoints (often 0 K)")
    args = ap.parse_args()

    x, data = load_points_temp_csv(args.csv)

    parts_sorted = np.sort(data[0].unique())
    n = len(parts_sorted)
    if n == 0:
        raise SystemExit("No Parts found in file.")

    # sampling of parts to keep plot readable
    if n > args.max_rows:
        sample_idxs = np.linspace(0, n - 1, args.max_rows).astype(int)
        sample_parts = parts_sorted[sample_idxs]
    else:
        sample_parts = parts_sorted

    Tmat = []
    times = []

    for p in sample_parts:
        row = data.loc[data[0] == int(p)].iloc[0]
        times.append(float(row.iloc[1]))
        temps = row.iloc[2:].astype(float).values

        if args.drop_zero_ends and len(temps) >= 2 and temps[0] == 0.0 and temps[-1] == 0.0:
            temps = temps[1:-1]

        Tmat.append(temps)

    Tmat = np.array(Tmat)
    times = np.array(times)

    # adjust x if we dropped endpoints
    x_plot = x
    if args.drop_zero_ends and len(x) == Tmat.shape[1] + 2:
        x_plot = x[1:-1]

    plt.figure()
    plt.imshow(
        Tmat,
        aspect="auto",
        origin="lower",
        extent=[x_plot.min(), x_plot.max(), times.min(), times.max()],
    )
    plt.xlabel("x [m]")
    plt.ylabel("time [s]")
    plt.title("Temperature evolution heatmap (sampled parts)")
    plt.colorbar(label="Temperature [K]")
    plt.show()


if __name__ == "__main__":
    main()
