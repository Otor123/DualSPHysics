#!/usr/bin/env python3
"""
Symmetry plot for SphinxSys radial observer .dat file.

Assumes points are stored as (+z, -z) pairs in this order:
  i=0..(n_default-2): z = (D/2)*i/n_default; push +z then -z

Outputs:
  1) absolute symmetry error |Vy(+z) - Vy(-z)| vs |z|
  2) relative symmetry error [%] vs |z|

Usage:
  python3 SphinXsys_plot_symmetry_radial.py \
    --radial /nishome/PaulS/Programms/sphinxsys/build/tests/3d_examples/test_3d_poiseuille_flow_shell/bin/output/fluid_observer_radial_Velocity.dat \
    --diameter 0.00635 \
    --time final
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_observer_dat(path: Path) -> Tuple[pd.DataFrame, list[str]]:
    with path.open("r", errors="ignore") as f:
        header = f.readline().strip()

    cols = re.findall(r'"[^"]+"|\S+', header)
    cols = [c[1:-1] if len(c) >= 2 and c[0] == '"' and c[-1] == '"' else c for c in cols]

    df = pd.read_csv(path, sep=r"\s+", skiprows=1, header=None)
    df = df.iloc[:, : len(cols)]
    df.columns = cols
    return df, cols


def infer_n_points(cols: list[str]) -> int:
    vcols = [c for c in cols if c.startswith("Velocity[")]
    return len(vcols) // 3


def extract_vy(row: pd.Series, n_points: int) -> np.ndarray:
    return np.array([float(row.get(f"Velocity[{k}][1]", np.nan)) for k in range(n_points)], dtype=float)


def choose_row(df: pd.DataFrame, time_mode: str, time_value: float | None) -> pd.Series:
    if time_mode == "final":
        return df.iloc[-1]
    if time_mode == "first":
        return df.iloc[0]
    if time_mode == "time":
        if time_value is None:
            raise ValueError("--time-value is required when --time=time")
        if "run_time" not in df.columns:
            raise ValueError("No 'run_time' column found in file.")
        idx = (df["run_time"] - time_value).abs().idxmin()
        return df.loc[idx]
    raise ValueError(f"Unknown time mode: {time_mode}")


def reconstruct_radial_z(n_points: int, diameter: float, n_default: int = 11) -> np.ndarray:
    z_list = []
    for i in range(n_default - 1):
        z = (diameter / 2.0) * i / float(n_default)
        z_list += [z, -z]
    z = np.array(z_list[:n_points], dtype=float)
    if len(z) < n_points:
        z = np.arange(n_points, dtype=float)
    return z


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radial", type=Path, required=True, help="fluid_observer_radial_Velocity.dat")
    ap.add_argument("--diameter", type=float, required=True, help="Pipe diameter [m]")
    ap.add_argument("--time", choices=["final", "first", "time"], default="final")
    ap.add_argument("--time-value", type=float, default=None)
    args = ap.parse_args()

    df, cols = read_observer_dat(args.radial)
    row = choose_row(df, args.time, args.time_value)

    n_points = infer_n_points(cols)
    vy = extract_vy(row, n_points)
    z = reconstruct_radial_z(n_points, args.diameter, n_default=11)

    pairs = n_points // 2
    z_abs = np.zeros(pairs)
    abs_err = np.zeros(pairs)
    rel_err = np.zeros(pairs)

    for i in range(pairs):
        v_pos = vy[2 * i]       # +z
        v_neg = vy[2 * i + 1]   # -z
        z_abs[i] = abs(z[2 * i])
        abs_err[i] = abs(v_pos - v_neg)
        denom = max(abs(v_pos), abs(v_neg), 1e-12)
        rel_err[i] = 100.0 * abs_err[i] / denom

    order = np.argsort(z_abs)
    z_abs, abs_err, rel_err = z_abs[order], abs_err[order], rel_err[order]

    t = float(row.get("run_time", np.nan))

    # nach dem Sortieren
    order = np.argsort(z_abs)
    z_abs, abs_err, rel_err = z_abs[order], abs_err[order], rel_err[order]

    # ---- invert axis ----
    z_plot = z_abs.max() - z_abs   # <-- hier drehen wir es um

    plt.figure(figsize=(9, 5))
    plt.plot(z_plot, abs_err, marker="o")
    plt.xlabel("Distance from boundary [m]")
    plt.ylabel("|Vy(+z) - Vy(-z)| [m/s]")
    plt.title(f"Radial symmetry error (t={t:.6g}s)")
    plt.grid(True)

    plt.figure(figsize=(9, 5))
    plt.plot(z_plot, rel_err, marker="o")
    plt.xlabel("Distance from boundary [m]")
    plt.ylabel("Relative symmetry error [%]")
    plt.title(f"Radial symmetry error (%) (t={t:.6g}s)")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
