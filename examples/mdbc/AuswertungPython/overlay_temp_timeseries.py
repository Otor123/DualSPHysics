#!/usr/bin/env python3
"""
Time-series overlay at fixed positions:
DualSPH MeasureTool temperatures vs analytic 1D heat conduction (two Dirichlet walls).

Assumes MeasureTool CSV like _PointsTemp_Temp.csv:
- semicolon-separated
- row 0, columns 2..end: positions (x)
- data starts at row 3: columns [Part, Time, Temp_0..Temp_N]

Example:
  python overlay_temp_timeseries.py _PointsTempConvergenz_Temp_2D_long.csv --x 0.002 0.004 0.006 --TL 363 --TR 363 --T0 293 --L 0.01
Optional:
  --drop-zero-ends
  --part 150
  --tmax 100
"""

from __future__ import annotations

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# DualSPH CSV loading
# -----------------------------
def load_points_temp_csv(path: str | Path) -> tuple[np.ndarray, pd.DataFrame]:
    path = Path(path)
    raw = pd.read_csv(path, sep=";", header=None)

    # positions in row 0, columns 2..end
    x = raw.iloc[0, 2:].astype(float).values

    # data starts at row 3
    data = raw.iloc[3:].copy()

    # columns: [Part, Time, Temp_0..Temp_N]
    data[0] = pd.to_numeric(data[0], errors="coerce")  # Part
    data[1] = pd.to_numeric(data[1], errors="coerce")  # Time
    data = data.dropna(subset=[0, 1]).copy()
    data[0] = data[0].astype(int)

    # ensure temp columns are numeric
    for c in data.columns[2:]:
        data[c] = pd.to_numeric(data[c], errors="coerce")

    data = data.dropna(subset=data.columns[2:], how="all")
    return x, data


def pick_part(data: pd.DataFrame, part: int | None) -> int:
    if part is not None:
        return int(part)
    # choose most frequent Part
    vc = data[0].value_counts()
    return int(vc.index[0])


def build_timeseries(data: pd.DataFrame, part: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns:
      times: (Nt,)
      temps: (Nt, Nx)  where Nx = number of positions in CSV
    """
    df = data[data[0] == part].copy()
    if df.empty:
        raise SystemExit(f"No rows found for Part={part}. Use --part to select an existing Part.")

    # sort by time
    df = df.sort_values(by=1)
    times = df[1].astype(float).values
    temps = df.iloc[:, 2:].astype(float).values  # shape (Nt, Nx)
    return times, temps


def find_nearest_indices(grid: np.ndarray, targets: list[float]) -> list[int]:
    idxs = []
    for t in targets:
        idxs.append(int(np.argmin(np.abs(grid - t))))
    return idxs


# -----------------------------
# Analytic solution: two Dirichlet walls
# T_t = alpha T_xx,  T(0,t)=TL, T(L,t)=TR, initial T(x,0)=T0 constant
# -----------------------------
def analytic_two_walls_scalar_x(
    x: float,
    t: np.ndarray,
    L: float,
    TL: float,
    TR: float,
    T0: float,
    alpha: float,
    n_terms: int = 300,
) -> np.ndarray:
    """
    Compute analytic T(x,t) for one position x and array of times t.
    (Vectorized in t, loop over Fourier terms.)
    """
    t = np.asarray(t, dtype=float)
    Ts = TL + (TR - TL) * (x / L)  # steady linear part

    out = np.full_like(t, fill_value=T0, dtype=float)
    mask = t > 0
    if not np.any(mask):
        return out

    tt = t[mask]
    s = np.zeros_like(tt)

    for n in range(1, n_terms + 1):
        Bn = (2.0 / (n * np.pi)) * (
            (T0 - TL) * (1.0 - (-1.0) ** n) + (TR - TL) * ((-1.0) ** n)
        )
        lam = n * np.pi / L
        s += Bn * np.sin(lam * x) * np.exp(-alpha * lam**2 * tt)

    out[mask] = Ts + s
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="Path to _PointsTemp_Temp.csv")

    ap.add_argument(
        "--x",
        type=float,
        nargs="+",
        required=True,
        help="Positions along the 1D axis where you want T(t), e.g. --x 0.002 0.004 0.006",
    )

    # optional selection / cropping
    ap.add_argument("--part", type=int, default=None, help="Select Part id (default: most frequent Part in file)")
    ap.add_argument("--tmax", type=float, default=None, help="Optional: only plot up to this time [s]")

    # geometry + temps
    ap.add_argument("--L", type=float, default=0.01, help="Domain length [m]")
    ap.add_argument("--TL", type=float, default=363.0, help="Left wall temperature [K]")
    ap.add_argument("--TR", type=float, default=363.0, help="Right wall temperature [K]")
    ap.add_argument("--T0", type=float, default=293.0, help="Initial fluid temperature [K]")

    # material
    ap.add_argument("--k", type=float, default=0.6, help="Thermal conductivity [W/(mK)]")
    ap.add_argument("--rho", type=float, default=1000.0, help="Density [kg/m^3]")
    ap.add_argument("--cp", type=float, default=4182.0, help="Specific heat capacity [J/(kgK)]")

    ap.add_argument("--n-terms", type=int, default=300, help="Number of Fourier terms")
    ap.add_argument(
        "--drop-zero-ends",
        action="store_true",
        help="Drop first+last position if their temperatures are dummy zeros (common in MeasureTool exports)",
    )

    args = ap.parse_args()

    x_grid, data = load_points_temp_csv(args.csv)

    # optional: drop dummy endpoints if BOTH ends are 0 for (almost) all times
    # We check the first filtered part only (practical & robust enough).
    part = pick_part(data, args.part)
    times, temps = build_timeseries(data, part)

    if args.drop_zero_ends and temps.shape[1] >= 2:
        left_all_zero = np.allclose(temps[:, 0], 0.0)
        right_all_zero = np.allclose(temps[:, -1], 0.0)
        if left_all_zero and right_all_zero:
            x_grid = x_grid[1:-1]
            temps = temps[:, 1:-1]

    # optional: crop by tmax
    if args.tmax is not None:
        m = times <= float(args.tmax)
        times = times[m]
        temps = temps[m, :]

    # compute alpha
    alpha = args.k / (args.rho * args.cp)

    # find nearest indices for requested positions
    idxs = find_nearest_indices(x_grid, args.x)
    picked_positions = [float(x_grid[i]) for i in idxs]

    # plot: one curve per position, sim solid, analytic dashed
    plt.figure()

    for req_x, i, x_used in zip(args.x, idxs, picked_positions):
        T_sim_t = temps[:, i]
        T_ana_t = analytic_two_walls_scalar_x(
            x=x_used,
            t=times,
            L=args.L,
            TL=args.TL,
            TR=args.TR,
            T0=args.T0,
            alpha=alpha,
            n_terms=args.n_terms,
        )

        label_pos = f"x={x_used:.6g} m"
        if abs(req_x - x_used) > 1e-12:
            label_pos += f" (nearest to {req_x:.6g})"

        plt.plot(times, T_sim_t, label=f"DualSPH {label_pos}")
        plt.plot(times, T_ana_t, linestyle="--", label=f"Analytic {label_pos}")

    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.title(f"Temperature vs time at fixed positions (Part {part})")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
