#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot temperature convergence (T vs time) for multiple probe points exported by DualSPHysics MeasureTool.

This script is tailored to files like:
  _PointsTempConvergenz_Temp.csv

Typical header layout (semicolon separated):
  ;PosX [m]:;0.005;0.005;0.005
  ;PosY [m]:;0;0;0
  ;PosZ [m]:;0.002;0.004;0.006
  Part;Time [s];Temp_0;Temp_1;Temp_2
  0;0;293;293;293
  1;0.0200017;293;293;293
  ...

Features:
- Automatically parses the PosZ row to label curves (z positions)
- Plots T(t) for all temperature columns
- Optional: plot dT/dt
- Optional: plot normalized convergence (T-T0)/(Tinf-T0)
- Optional: save figures to PNG

Usage examples:
  python plot_temp_convergence_points.py _PointsTempConvergenz_Temp_2D_long.csv
  python plot_temp_convergence_points.py _PointsTempConvergenz_Temp_200sec.csv
  python plot_temp_convergence_points.py _PointsTempConvergenz_Temp_with_Top.csv
  python plot_temp_convergence_points.py _PointsTemp_Temp.csv
  python plot_temp_convergence_points.py _PointsTempConvergenz_Temp_1D_long.csv
  python plot_temp_convergence_points.py _PointsTempConvergenz_Temp.csv --save_prefix conv
  python plot_temp_convergence_points.py _PointsTempConvergenz_Temp.csv --plot_dtdt --plot_norm

  python plot_temp_convergence_points.py _PointsTempConvergenz_Temp_Boundary.csv
  """

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _read_raw_semicolon(csv_path: Path) -> pd.DataFrame:
    """Read the file as semicolon-separated with no header (raw rows)."""
    return pd.read_csv(csv_path, sep=";", header=None, dtype=str, engine="python")


def parse_points_temp_csv(csv_path: Path) -> Tuple[pd.DataFrame, List[float]]:
    """
    Parse a DualSPHysics PointsTemp CSV and return:
      - data DataFrame with numeric columns: Time_s, Temp_0..Temp_N
      - z_positions list aligned with Temp columns, if available (else empty)
    """
    raw = _read_raw_semicolon(csv_path)

    # Find rows containing PosZ and header row containing "Time [s]"
    posz_row_idx = None
    header_row_idx = None

    for i in range(min(len(raw), 80)):  # header is near the top
        row = raw.iloc[i].astype(str).tolist()
        if any("PosZ" in cell for cell in row):
            posz_row_idx = i
        if any(cell.strip() == "Time [s]" for cell in row):
            header_row_idx = i

    if header_row_idx is None:
        raise ValueError("Could not find header row with 'Time [s]' in the file. Is this a PointsTemp CSV?")

    # Extract z positions if row exists
    z_positions: List[float] = []
    if posz_row_idx is not None:
        posz_row = raw.iloc[posz_row_idx].tolist()
        # expected: ["", "PosZ [m]:", z0, z1, ...]
        for v in posz_row[2:]:
            try:
                z_positions.append(float(str(v).strip()))
            except Exception:
                z_positions.append(float("nan"))

    # Build header names
    header = [str(h).strip() for h in raw.iloc[header_row_idx].tolist()]
    header = ["Time_s" if h == "Time [s]" else h for h in header]

    # Data starts right after header row
    data = raw.iloc[header_row_idx + 1 :].copy()
    data.columns = header

    temp_cols = [c for c in data.columns if str(c).startswith("Temp_")]
    keep = ["Time_s"] + temp_cols
    data = data.loc[:, keep]

    # Convert to numeric, drop invalid rows
    for c in data.columns:
        data[c] = pd.to_numeric(data[c], errors="coerce")
    data = data.dropna(subset=["Time_s"]).sort_values("Time_s")

    # If z_positions length doesn't match, discard labels
    if len(z_positions) != len(temp_cols):
        z_positions = []

    return data, z_positions


def compute_dtdt(time_s: np.ndarray, temp: np.ndarray) -> np.ndarray:
    """Compute numerical derivative dT/dt (works with non-uniform dt)."""
    return np.gradient(temp, time_s)


def normalize_convergence(temp: np.ndarray) -> np.ndarray:
    """Normalize (T - T0) / (Tinf - T0) using first and last sample."""
    t0 = temp[0]
    tinf = temp[-1]
    denom = tinf - t0
    if np.isclose(denom, 0.0):
        return np.zeros_like(temp)
    return (temp - t0) / denom


def export_vsc_csv(
    df: pd.DataFrame,
    temp_cols: List[str],
    z_positions: List[float],
    out_path: Path,
) -> None:
    """
    Export a semicolon CSV compatible with the 'time_s;temperature_K' style.

    - If exactly one temperature column exists -> writes:
        time_s;temperature_K
    - If multiple temp columns -> writes:
        time_s;temperature_K_<label>
      where <label> uses z position if available else the original column name.
    """
    out = pd.DataFrame()
    out["time_s"] = df["Time_s"].astype(float)

    if len(temp_cols) == 1:
        out["temperature_K"] = df[temp_cols[0]].astype(float)
    else:
        for i, c in enumerate(temp_cols):
            if z_positions:
                label = f"z{z_positions[i]:g}m"
            else:
                label = c
            out[f"temperature_K_{label}"] = df[c].astype(float)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, sep=";", index=False, lineterminator="\n")



def main() -> None:
    ap = argparse.ArgumentParser(description="Plot temperature convergence for PointsTemp CSV.")
    ap.add_argument("csv", type=Path, help="Path to _PointsTemp*_Temp.csv (semicolon-separated).")
    ap.add_argument("--save_prefix", type=str, default="", help="If set, save plots as <prefix>_T.png etc.")
    ap.add_argument("--plot_dtdt", action="store_true", help="Also plot dT/dt vs time.")
    ap.add_argument("--plot_norm", action="store_true", help="Also plot normalized convergence.")
    ap.add_argument("--export_vsc", type=Path, default=None,
                help="Export a semicolon CSV like the attachment: time_s;temperature_K ...")
    ap.add_argument("--export_vsc_split", type=str, default="",
                help="If set, export one CSV per probe: <prefix>_<label>.csv (2 columns like attachment).")

    args = ap.parse_args()

    df, zpos = parse_points_temp_csv(args.csv)
    time = df["Time_s"].to_numpy()
    temp_cols = [c for c in df.columns if c.startswith("Temp_")]

        # --- Optional: VSCode/attachment-style CSV export ---
    if args.export_vsc is not None:
        export_vsc_csv(df, temp_cols, zpos, args.export_vsc)

    if args.export_vsc_split:
        base = args.export_vsc_split
        for i, c in enumerate(temp_cols):
            if zpos:
                label = f"z{zpos[i]:g}m"
            else:
                label = c
            out_path = Path(f"{base}_{label}.csv")

            tmp = pd.DataFrame({
                "time_s": df["Time_s"].astype(float),
                "temperature_K": df[c].astype(float),
            })
            tmp.to_csv(out_path, sep=";", index=False, lineterminator="\n")


    # --- Plot T(t) ---
    plt.figure()
    plt.title("HeattransferSimulation Convergenz 1D")
    for i, c in enumerate(temp_cols):
        label = f"z = {zpos[i]:g} m" if zpos else c
        plt.plot(time, df[c].to_numpy(), label=label)
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.grid(True)
    plt.legend()
    if args.save_prefix:
        plt.savefig(f"{args.save_prefix}_T.png", dpi=200, bbox_inches="tight")
    else:
        plt.show()

    # --- Optional: dT/dt ---
    if args.plot_dtdt:
        plt.figure()
        for i, c in enumerate(temp_cols):
            label = f"z = {zpos[i]:g} m" if zpos else c
            dtdt = compute_dtdt(time, df[c].to_numpy())
            plt.plot(time, dtdt, label=label)
        plt.xlabel("Time [s]")
        plt.ylabel("dT/dt [K/s]")
        plt.grid(True)
        plt.legend()
        if args.save_prefix:
            plt.savefig(f"{args.save_prefix}_dTdt.png", dpi=200, bbox_inches="tight")
        else:
            plt.show()

    # --- Optional: normalized convergence ---
    if args.plot_norm:
        plt.figure()
        for i, c in enumerate(temp_cols):
            label = f"z = {zpos[i]:g} m" if zpos else c
            norm = normalize_convergence(df[c].to_numpy())
            plt.plot(time, norm, label=label)
        plt.xlabel("Time [s]")
        plt.ylabel("Normalized convergence (T-T0)/(T∞-T0)")
        plt.grid(True)
        plt.legend()
        if args.save_prefix:
            plt.savefig(f"{args.save_prefix}_norm.png", dpi=200, bbox_inches="tight")
        else:
            plt.show()


if __name__ == "__main__":
    main()
