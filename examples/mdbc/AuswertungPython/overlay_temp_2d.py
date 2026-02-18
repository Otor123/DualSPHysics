#!/usr/bin/env python3
"""
Overlay DualSPH MeasureTool temperature profile vs analytic 2D heat diffusion
in a rectangle with 3 hot walls (left, right, bottom at Tw) and top adiabatic.

BCs for theta = T-Tw:
  theta(0,z,t)=theta(Lx,z,t)=theta(x,0,t)=0
  dtheta/dz(x,Lz,t)=0
IC:
  theta(x,z,0)=T0-Tw (constant)

We compare along a line z = z_line: T(x, z_line, t).

Usage:
  python overlay_temp_2d.py _PointsTemp_Temp.csv --t 7.5 --Lx 0.01 --Lz 0.007 --z 0.005
Optional:
  --drop-zero-ends
  --error
"""

from __future__ import annotations
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_points_temp_csv(path: str | Path) -> tuple[np.ndarray, pd.DataFrame]:
    raw = pd.read_csv(Path(path), sep=";", header=None)
    x = raw.iloc[0, 2:].astype(float).values
    data = raw.iloc[3:].copy()
    data[0] = pd.to_numeric(data[0], errors="coerce")  # Part
    data[1] = pd.to_numeric(data[1], errors="coerce")  # Time
    data = data.dropna(subset=[0, 1]).copy()
    data[0] = data[0].astype(int)
    return x, data


def get_profile_at_time(data: pd.DataFrame, t_target: float) -> tuple[int, float, np.ndarray]:
    times = data[1].astype(float).values
    idx = int(np.argmin(np.abs(times - t_target)))
    row = data.iloc[idx]
    part = int(row.iloc[0])
    t_found = float(row.iloc[1])
    temps = row.iloc[2:].astype(float).values
    return part, t_found, temps


def analytic_2d_three_hot_walls_line(
    x: np.ndarray, z_line: float, t: float,
    Lx: float, Lz: float,
    Tw: float, T0: float,
    alpha: float,
    Nn: int = 81, Nm: int = 81
) -> np.ndarray:
    """
    Analytic 2D solution evaluated at fixed z=z_line.
    Uses series with n=1..Nn and m=0..Nm-1.
    Only odd n contribute; we still loop all n for clarity.
    """
    if t <= 0:
        return T0 * np.ones_like(x)

    theta0 = T0 - Tw
    T = Tw + np.zeros_like(x, dtype=float)

    pi = np.pi
    for n in range(1, Nn + 1):
        # factor (1 - (-1)^n): 2 for odd n, 0 for even n
        odd_factor = 1.0 - (-1.0)**n
        if odd_factor == 0.0:
            continue

        sinx = np.sin(n * pi * x / Lx)

        for m in range(0, Nm):
            kz = (m + 0.5) * pi / Lz
            kn = n * pi / Lx
            lam2 = kn*kn + kz*kz

            # coefficient for constant theta0
            A = (8.0 * theta0 / (n*pi * (m + 0.5)*pi)) * odd_factor

            T += A * sinx * np.sin(kz * z_line) * np.exp(-alpha * lam2 * t)

    return T

def analytic_2d_three_hot_walls_top_T0_line(
    x: np.ndarray, z_line: float, t: float,
    Lx: float, Lz: float,
    Tw: float, T0: float,
    alpha: float,
    Nn: int = 61, Nm: int = 61
) -> np.ndarray:
    """
    2D analytic reference:
      - left/right/bottom at Tw (Dirichlet)
      - top at T0 (Dirichlet)
      - initial fluid everywhere T0

    Returns T(x, z_line, t) along a horizontal line.

    Implementation:
      T = S + u
      S: steady Laplace solution (computed as 1D sine series in x with sinh in z)
      u: transient double-sine series with coefficients obtained by numerical projection
    """
    pi = np.pi
    Delta = T0 - Tw  # negative if Tw > T0

    # ---- helper: steady part S(x,z)
    def S_xz(xv, zv):
        # S = Tw + sum_n Bn sin(nπx/Lx) * sinh(nπ z/Lx)/sinh(nπ Lz/Lx)
        s = Tw + np.zeros_like(xv, dtype=float)
        for n in range(1, Nn + 1):
            odd_factor = 1.0 - (-1.0)**n
            if odd_factor == 0.0:
                continue
            Bn = (2.0 * Delta / (n * pi)) * odd_factor
            kn = n * pi / Lx
            s += Bn * np.sin(kn * xv) * np.sinh(kn * zv) / np.sinh(kn * Lz)
        return s

    # If t=0, enforce initial condition exactly
    if t <= 0:
        return T0 * np.ones_like(x)

    # ---- compute steady on the query line
    S_line = S_xz(x, z_line)

    # ---- transient u: compute coefficients by projection on a grid
    # Choose a projection grid (moderate size is enough)
    Nx = max(80, 2*Nn)
    Nz = max(80, 2*Nm)
    xg = np.linspace(0.0, Lx, Nx)
    zg = np.linspace(0.0, Lz, Nz)
    X, Z = np.meshgrid(xg, zg, indexing="xy")  # X: (Nz,Nx)

    S_grid = S_xz(X, Z)
    u0 = (T0 - S_grid)  # initial transient field

    # Precompute sines on grids
    sinx = np.zeros((Nn, Nx))
    for n in range(1, Nn + 1):
        sinx[n-1, :] = np.sin(n*pi*xg/Lx)

    sinz = np.zeros((Nm, Nz))
    for m in range(1, Nm + 1):
        sinz[m-1, :] = np.sin(m*pi*zg/Lz)

    # Numerical integration weights (trapezoidal)
    wx = np.ones(Nx); wx[0] = wx[-1] = 0.5
    wz = np.ones(Nz); wz[0] = wz[-1] = 0.5
    dx = Lx/(Nx-1)
    dz = Lz/(Nz-1)

    # Compute coefficients A_nm
    # A_nm = 4/(Lx Lz) ∬ u0 sin(nπx/Lx) sin(mπz/Lz) dx dz
    A = np.zeros((Nn, Nm), dtype=float)

    # Integrate via separable sums:
    # ∬ u0(z,x) sinx_n(x) sinz_m(z) dx dz
    # = Σ_z Σ_x u0[z,x] sinx_n[x] sinz_m[z] * wx[x]*wz[z]*dx*dz
    for n in range(Nn):
        sx = sinx[n, :][None, :]  # (1,Nx)
        # inner x integration for each z:
        Ix = np.sum(u0 * sx * wx[None, :], axis=1) * dx  # (Nz,)
        for m in range(Nm):
            integr = np.sum(Ix * sinz[m, :] * wz) * dz
            A[n, m] = (4.0 / (Lx * Lz)) * integr

    # Evaluate u on the query line z=z_line
    # u(x,z_line,t) = Σ_n Σ_m A_nm sin(nπx/Lx) sin(mπz/Lz) exp(-α λ^2 t)
    u_line = np.zeros_like(x, dtype=float)
    for n in range(1, Nn + 1):
        kn = n*pi/Lx
        sinx_line = np.sin(kn * x)
        for m in range(1, Nm + 1):
            kz = m*pi/Lz
            lam2 = kn*kn + kz*kz
            u_line += A[n-1, m-1] * sinx_line * np.sin(kz * z_line) * np.exp(-alpha * lam2 * t)

    return S_line + u_line


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="Path to _PointsTemp_Temp.csv")
    ap.add_argument("--t", type=float, required=True, help="Target time [s] (closest row used)")

    ap.add_argument("--Lx", type=float, default=0.01, help="Domain length in x [m]")
    ap.add_argument("--Lz", type=float, default=0.007, help="Fluid height in z [m]")
    ap.add_argument("--z", type=float, default=None, help="z-line for analytic evaluation [m] (default=Lz/2)")

    ap.add_argument("--Tw", type=float, default=363.0, help="Hot wall temperature [K]")
    ap.add_argument("--T0", type=float, default=293.0, help="Initial fluid temperature [K]")

    ap.add_argument("--k", type=float, default=0.6, help="Fluid thermal conductivity [W/(mK)]")
    ap.add_argument("--rho", type=float, default=1000.0, help="Fluid density [kg/m^3]")
    ap.add_argument("--cp", type=float, default=4182.0, help="Fluid cp [J/(kgK)]")

    ap.add_argument("--Nn", type=int, default=81, help="Number of x-modes (n)")
    ap.add_argument("--Nm", type=int, default=81, help="Number of z-modes (m)")

    ap.add_argument("--drop-zero-ends", action="store_true",
                    help="Drop endpoints if first and last temp are 0 (dummy points).")
    ap.add_argument("--error", action="store_true", help="Show (sim - analytic) as second plot.")
    args = ap.parse_args()

    z_line = args.Lz/2 if args.z is None else args.z

    x_sim, data = load_points_temp_csv(args.csv)
    part, t_found, T_sim = get_profile_at_time(data, args.t)

    x_plot = x_sim
    T_sim_plot = T_sim
    if args.drop_zero_ends and len(T_sim) >= 2 and T_sim[0] == 0.0 and T_sim[-1] == 0.0:
        x_plot = x_sim[1:-1]
        T_sim_plot = T_sim[1:-1]

    alpha = args.k / (args.rho * args.cp)

    #T_ana = analytic_2d_three_hot_walls_line(
    #    x_plot, z_line, t_found,
    #    args.Lx, args.Lz,
    #    args.Tw, args.T0,
    #    alpha,
    #    Nn=args.Nn, Nm=args.Nm
    #)

    T_ana = analytic_2d_three_hot_walls_top_T0_line(
        x_plot, z_line, t_found,
        args.Lx, args.Lz,
        args.Tw, args.T0,
        alpha,
        Nn=args.Nn, Nm=args.Nm
    )    

    plt.figure()
    plt.plot(x_plot, T_sim_plot, marker="o", label=f"DualSPH (Part {part}, t={t_found:.6g}s)")
    plt.plot(x_plot, T_ana, linestyle="--",
             label=f"Analytic 2D (z={z_line:.4g} m, Nn={args.Nn}, Nm={args.Nm})")
    plt.xlabel("x [m]")
    plt.ylabel("Temperature [K]")
    plt.title("Temperature profile: Simulation vs Analytic (2D, 3 hot walls + top adiabatic)")
    plt.grid(True)
    plt.legend()
    plt.show()

    if args.error:
        plt.figure()
        plt.plot(x_plot, T_sim_plot - T_ana, marker="o")
        plt.xlabel("x [m]")
        plt.ylabel("ΔT = T_sim - T_analytic [K]")
        plt.title("Error profile")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    main()
