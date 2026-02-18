#!/usr/bin/env python3
"""
Plot SphinxSys observer .dat outputs for Poiseuille case.

- Axial: Vy vs y (uses only observer ordering; y reconstructed as linspace(0, full_length))
- Radial: Vy vs z (scatter-only by default to avoid zig-zag due to +z/-z ordering)
- Optional: plot analytical Poiseuille profile on radial plot if you pass --Umax and --R

Usage example:
  python3 SphInXsys_plot_poiseuille_observers.py \
    --axial /nishome/PaulS/Programms/sphinxsys/build/tests/3d_examples/test_3d_poiseuille_flow_shell/bin/output/fluid_observer_axial_Velocity.dat \
    --radial /nishome/PaulS/Programms/sphinxsys/build/tests/3d_examples/test_3d_poiseuille_flow_shell/bin/output/fluid_observer_radial_Velocity.dat \
    --diameter 0.00635 \
    --full-length 0.03175 \
    --Umax 0.105 \
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
    """Reads SphinxSys ObservedQuantityRecording .dat file."""
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


def extract_component(row: pd.Series, n_points: int, comp: int) -> np.ndarray:
    out = np.zeros(n_points, dtype=float)
    for k in range(n_points):
        out[k] = float(row.get(f"Velocity[{k}][{comp}]", np.nan))
    return out


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
    """
    Reconstruct z positions for the default C++ logic:
      for i=0..n_default-2:
        z = (diameter/2) * i / n_default
        emplace(+z), emplace(-z)
    -> order: +z,-z,+z,-z,...
    """
    z_list = []
    for i in range(n_default - 1):
        z = (diameter / 2.0) * i / float(n_default)
        z_list += [z, -z]
    z = np.array(z_list[:n_points], dtype=float)
    if len(z) < n_points:
        # fallback if mismatch
        z = np.arange(n_points, dtype=float)
    return z


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--axial", type=Path, required=True, help="fluid_observer_axial_Velocity.dat")
    ap.add_argument("--radial", type=Path, required=True, help="fluid_observer_radial_Velocity.dat")
    ap.add_argument("--diameter", type=float, required=True, help="Pipe diameter [m]")
    ap.add_argument("--full-length", type=float, required=True, help="Pipe length used for axial observers [m]")
    ap.add_argument("--Umax", type=float, default=None, help="Optional: plot analytical profile with this Umax [m/s]")
    ap.add_argument("--R", type=float, default=None, help="Optional: radius for analytical profile [m]. If omitted: diameter/2")
    ap.add_argument("--time", choices=["final", "first", "time"], default="final")
    ap.add_argument("--time-value", type=float, default=None, help="When --time=time, choose nearest run_time")
    ap.add_argument("--show-lines", action="store_true", help="Connect radial points with lines (usually misleading)")
    args = ap.parse_args()

    # --- Read files ---
    ax_df, ax_cols = read_observer_dat(args.axial)
    rad_df, rad_cols = read_observer_dat(args.radial)

    ax_row = choose_row(ax_df, args.time, args.time_value)
    rad_row = choose_row(rad_df, args.time, args.time_value)

    ax_n = infer_n_points(ax_cols)
    rad_n = infer_n_points(rad_cols)

    ax_vy = extract_component(ax_row, ax_n, comp=1)
    rad_vy = extract_component(rad_row, rad_n, comp=1)

    # --- Reconstruct coordinates (based on your C++ generator defaults) ---
    ax_y = np.linspace(0.0, args.full_length, ax_n)
    rad_z = reconstruct_radial_z(rad_n, args.diameter, n_default=11)

    t_ax = float(ax_row.get("run_time", np.nan))
    t_rad = float(rad_row.get("run_time", np.nan))

    # --- Plot axial ---
    plt.figure(figsize=(10, 5))
    plt.plot(ax_y, ax_vy, marker="o")
    plt.xlabel("y [m] (axial observer position)")
    plt.ylabel("Vy [m/s]")
    plt.title(f"Axial observer: Vy vs y (t={t_ax:.6g}s, N={ax_n})")
    plt.grid(True)

    # --- Plot radial ---
    plt.figure(figsize=(10, 5))
    if args.show_lines:
        plt.plot(rad_z, rad_vy, marker="o")
    else:
        plt.scatter(rad_z, rad_vy)

    # Optional analytical curve
    if args.Umax is not None:
        R = args.R if args.R is not None else args.diameter / 2.0
        z_sorted = np.linspace(-R, R, 300)
        v_ana = args.Umax * (1.0 - (z_sorted / R) ** 2)
        plt.plot(z_sorted, v_ana, linewidth=2.0, label="Analytical (parabolic)")
        plt.legend()

    plt.xlabel("z [m] (radial observer position at y=full_length/2)")
    plt.ylabel("Vy [m/s]")
    plt.title(f"Radial observer: Vy vs z (t={t_rad:.6g}s, N={rad_n})")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
