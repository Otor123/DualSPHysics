#!/usr/bin/env python3
"""
Overlay: DualSPH MeasureTool temperature profile vs analytic 1D heat conduction (two hot walls).

Assumes MeasureTool CSV like _PointsTemp_Temp.csv:
- semicolon-separated
- row 0, columns 2..end: x positions
- data starts at row 3: columns [Part, Time, Temp_0..Temp_N]

Usage:
  python overlay_temp.py _PointsTemp_Temp.csv --t 7.5 --TL 363 --TR 363 --T0 293 --L 0.01
Optional:
  --drop-zero-ends     drop dummy endpoints (if first & last temp are 0)
  --error             show second figure with (sim-analytic)

python AnalyticalAndSimulativPlotTemperature.py _PointsTemp_Temp_1D.csv --t 7.5 --TL 363 --TR 363 --T0 293 --L 0.01 --drop-zero-ends --error --error-percent


# absolut + Prozent bezogen auf T_ana
python AnalyticalAndSimulativPlotTemperature.py _PointsTemp_Temp.csv --t 7.5 --drop-zero-ends --error --error-percent


# Prozent bezogen auf Temperaturerhöhung (oft sinnvoller)
python AnalyticalAndSimulativPlotTemperature.py _PointsTemp_Temp.csv --t 7.5 --drop-zero-ends --error-percent-rise

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

    # x positions are stored in row 0, columns 2..end
    x = raw.iloc[0, 2:].astype(float).values

    # data starts at row 3
    data = raw.iloc[3:].copy()

    # columns: [Part, Time, Temp_0..Temp_N]
    data[0] = pd.to_numeric(data[0], errors="coerce")  # Part
    data[1] = pd.to_numeric(data[1], errors="coerce")  # Time
    data = data.dropna(subset=[0, 1]).copy()
    data[0] = data[0].astype(int)  # Part int

    return x, data


def get_profile_at_time(data: pd.DataFrame, t_target: float) -> tuple[int, float, np.ndarray]:
    """Return (Part, t_found, temps) for the row with Time closest to t_target."""
    times = data[1].astype(float).values
    idx = int(np.argmin(np.abs(times - t_target)))
    row = data.iloc[idx]
    part = int(row.iloc[0])
    t_found = float(row.iloc[1])
    temps = row.iloc[2:].astype(float).values
    return part, t_found, temps


# -----------------------------
# Analytic solution: two Dirichlet walls
# T_t = alpha T_xx,  T(0,t)=TL, T(L,t)=TR, initial T(x,0)=T0 constant
# -----------------------------
def analytic_two_walls(x: np.ndarray, t: float, L: float, TL: float, TR: float, T0: float,
                      alpha: float, n_terms: int = 300) -> np.ndarray:
    Ts = TL + (TR - TL) * (x / L)  # steady linear part

    if t <= 0:
        return T0 * np.ones_like(x)

    s = np.zeros_like(x, dtype=float)
    for n in range(1, n_terms + 1):
        # Closed-form coefficient for uniform initial T0
        Bn = (2.0 / (n * np.pi)) * (
            (T0 - TL) * (1.0 - (-1.0) ** n) + (TR - TL) * ((-1.0) ** n)
        )
        lam = n * np.pi / L
        s += Bn * np.sin(lam * x) * np.exp(-alpha * lam**2 * t)

    return Ts + s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="Path to _PointsTemp_Temp.csv")
    ap.add_argument("--t", type=float, required=True, help="Target time in seconds (closest row will be used)")

    # geometry + temps
    ap.add_argument("--L", type=float, default=0.01, help="Domain length in x [m]")
    ap.add_argument("--TL", type=float, default=363.0, help="Left wall temperature [K]")
    ap.add_argument("--TR", type=float, default=363.0, help="Right wall temperature [K]")
    ap.add_argument("--T0", type=float, default=293.0, help="Initial fluid temperature [K]")

    # material
    ap.add_argument("--k", type=float, default=0.6, help="Thermal conductivity [W/(mK)]")
    ap.add_argument("--rho", type=float, default=1000.0, help="Density [kg/m^3]")
    ap.add_argument("--cp", type=float, default=4182.0, help="Specific heat capacity [J/(kgK)]")

    ap.add_argument("--n-terms", type=int, default=300, help="Number of Fourier terms")
    ap.add_argument("--drop-zero-ends", action="store_true",
                    help="Drop first+last point if both temperatures are 0 (dummy endpoints)")
    ap.add_argument("--error", action="store_true", help="Show a second plot of (sim - analytic)")
    ap.add_argument("--error-percent", action="store_true",
                    help="Show percent error: 100*(sim-analytic)/analytic")
    ap.add_argument("--error-percent-rise", action="store_true",
                    help="Show percent error w.r.t. temperature rise: 100*(sim-analytic)/(analytic-T0)")
    ap.add_argument("--eps", type=float, default=1e-12,
                    help="Small number to avoid division by zero in percent error plots")

    args = ap.parse_args()

    x_sim, data = load_points_temp_csv(args.csv)

    part, t_found, T_sim = get_profile_at_time(data, args.t)

    # optional: drop dummy endpoints
    x_plot = x_sim
    T_sim_plot = T_sim
    if args.drop_zero_ends and len(T_sim) >= 2 and T_sim[0] == 0.0 and T_sim[-1] == 0.0:
        x_plot = x_sim[1:-1]
        T_sim_plot = T_sim[1:-1]

    # alpha
    alpha = args.k / (args.rho * args.cp)

    # analytic computed on the SAME x grid (so overlay is direct)
    T_ana = analytic_two_walls(x_plot, t_found, args.L, args.TL, args.TR, args.T0, alpha, args.n_terms)

    # --- Plot overlay
    plt.figure()
    plt.plot(x_plot, T_sim_plot, marker="o", label=f"DualSPH (Part {part}, t={t_found:.6g}s)")
    plt.plot(x_plot, T_ana, linestyle="--", label=f"Analytic (t={t_found:.6g}s, N={args.n_terms})")
    plt.xlabel("x [m]")
    plt.ylabel("Temperature [K]")
    plt.title("Temperature profile: Simulation vs Analytic (two hot walls)")
    plt.grid(True)
    plt.legend()
    plt.show()

    # --- Optional error plot
    if args.error:
        plt.figure()
        plt.plot(x_plot, T_sim_plot - T_ana, marker="o")
        plt.xlabel("x [m]")
        plt.ylabel("ΔT = T_sim - T_analytic [K]")
        plt.title("Error profile")
        plt.grid(True)
        plt.show()

    if args.error_percent:
        denom = np.where(np.abs(T_ana) < args.eps, np.nan, T_ana)
        err_pct = 100.0 * (T_sim_plot - T_ana) / denom

        plt.figure()
        plt.plot(x_plot, err_pct, marker="o")
        plt.xlabel("x [m]")
        plt.ylabel("Error [%] = 100*(T_sim - T_ana)/T_ana")
        plt.title("Error profile (percent vs analytic temperature)")
        plt.grid(True)
        plt.show()

    if args.error_percent_rise:
        denom = (T_ana - args.T0)
        denom = np.where(np.abs(denom) < args.eps, np.nan, denom)
        err_pct_rise = 100.0 * (T_sim_plot - T_ana) / denom

        plt.figure()
        plt.plot(x_plot, err_pct_rise, marker="o")
        plt.xlabel("x [m]")
        plt.ylabel("Error [%] = 100*(T_sim - T_ana)/(T_ana - T0)")
        plt.title("Error profile (percent vs temperature rise)")
        plt.grid(True)
        plt.show()        


if __name__ == "__main__":
    main()
