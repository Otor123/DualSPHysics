#!/usr/bin/env python3
"""
Plot temperature profiles for multiple times (Parts) from DualSPHysics
MeasureTool output like: _PointsTemp_Temp.csv

- Reads semicolon-separated CSV
- Extracts x positions from first header row
- Selects representative Parts (0%, 25%, 50%, 75%, 100%) and ensures Part 150 is included if present
- Plots temperature vs x for each selected Part

python TemperaturePlot.py _PointsTemp_Temp.csv --drop-zero-ends

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

    # columns: [Part, Time, Temp_0..Temp_N]
    data[0] = pd.to_numeric(data[0], errors="coerce")  # Part
    data[1] = pd.to_numeric(data[1], errors="coerce")  # Time
    data = data.dropna(subset=[0, 1]).copy()

    # make Part integer-ish
    data[0] = data[0].astype(int)

    return x, data


def select_representative_parts(parts_sorted: np.ndarray, ensure_part: int | None = 150) -> list[int]:
    n = len(parts_sorted)
    if n == 0:
        return []

    idxs = sorted(set([0, n // 4, n // 2, (3 * n) // 4, n - 1]))
    rep = parts_sorted[idxs].tolist()

    if ensure_part is not None and ensure_part in parts_sorted and ensure_part not in rep:
        rep.insert(len(rep) // 2, int(ensure_part))

    return sorted(set(int(p) for p in rep))


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="Path to _PointsTemp_Temp.csv")
    ap.add_argument("--ensure-part", type=int, default=150, help="Ensure this Part is included if present")
    ap.add_argument("--drop-zero-ends", action="store_true",
                    help="Drop first+last x point if their temperature is 0 (common dummy endpoints)")
    args = ap.parse_args()

    x, data = load_points_temp_csv(args.csv)

    parts_sorted = np.sort(data[0].unique())
    rep_parts = select_representative_parts(parts_sorted, ensure_part=args.ensure_part)

    if not rep_parts:
        raise SystemExit("No Parts found in file.")

    plt.figure()

    for p in rep_parts:
        row = data.loc[data[0] == p].iloc[0]
        t = float(row.iloc[1])
        temps = row.iloc[2:].astype(float).values

        # optional cleanup: drop endpoint dummy zeros
        x_plot = x
        temps_plot = temps
        if args.drop_zero_ends and len(temps) >= 2:
            if temps[0] == 0.0 and temps[-1] == 0.0:
                x_plot = x[1:-1]
                temps_plot = temps[1:-1]

        plt.plot(x_plot, temps_plot, marker="o", label=f"Part {p} (t={t:.3g}s)")

    plt.xlabel("x [m]")
    plt.ylabel("Temperature [K]")
    plt.title("Temperature profiles over time (selected parts)")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
