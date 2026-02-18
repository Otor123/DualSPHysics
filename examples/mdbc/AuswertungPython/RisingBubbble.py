#!/usr/bin/env python3
"""
rayleigh_plesset_rising_bubble.py

Simulates:
  (A) Bubble radial dynamics via Rayleigh–Plesset (RP) equation (second-order ODE).
  (B) Bubble rise (z, w) with a simple buoyancy - drag model.
Coupling: hydrostatic pressure depends on depth z, and buoyancy/drag depend on R(t).

Units: SI (m, s, Pa, kg, N)

Run:
  python3 rayleigh_plesset_rising_bubble.py

Optional:
  python3 rayleigh_plesset_rising_bubble.py --t-end 0.02 --R0 5e-4 --z0 0.2
"""

from __future__ import annotations

import argparse
import numpy as np

from dataclasses import dataclass
from typing import Tuple

try:
    from scipy.integrate import solve_ivp
except ImportError as e:
    raise SystemExit(
        "This script needs SciPy. Install with: pip install scipy"
    ) from e

import matplotlib.pyplot as plt


@dataclass
class FluidProps:
    rho: float = 1000.0      # liquid density [kg/m^3]
    mu: float = 1.0e-3       # dynamic viscosity [Pa*s]
    sigma: float = 0.072     # surface tension [N/m]
    g: float = 9.81          # gravity [m/s^2]


@dataclass
class BubbleGasModel:
    kappa: float = 1.4       # polytropic exponent (1.4 ~ adiabatic air, 1.0 isothermal)
    Pv: float = 2330.0       # vapor pressure [Pa] (water ~ 2.3kPa at ~20°C)


@dataclass
class Ambient:
    Patm: float = 101325.0   # atmospheric pressure [Pa]


@dataclass
class Forcing:
    # Optional acoustic forcing: P_infty(t) = ... + A*sin(2π f t)
    A: float = 0.0           # forcing amplitude [Pa]
    f: float = 0.0           # forcing frequency [Hz]


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Rayleigh–Plesset + rising bubble toy model (SI units).")
    p.add_argument("--t-end", type=float, default=0.01, help="End time [s].")
    p.add_argument("--dt", type=float, default=1e-5, help="Output time step [s].")
    p.add_argument("--R0", type=float, default=1e-3, help="Initial radius [m].")
    p.add_argument("--Rdot0", type=float, default=0.0, help="Initial radial velocity [m/s].")
    p.add_argument("--z0", type=float, default=0.2, help="Initial depth below free surface [m]. z increases downward.")
    p.add_argument("--w0", type=float, default=0.0, help="Initial vertical velocity [m/s]. Positive is upward.")
    p.add_argument("--kappa", type=float, default=1.4, help="Polytropic exponent (gas).")
    p.add_argument("--rho", type=float, default=1000.0, help="Liquid density [kg/m^3].")
    p.add_argument("--mu", type=float, default=1e-3, help="Liquid viscosity [Pa*s].")
    p.add_argument("--sigma", type=float, default=0.072, help="Surface tension [N/m].")
    p.add_argument("--Patm", type=float, default=101325.0, help="Atmospheric pressure [Pa].")
    p.add_argument("--Pv", type=float, default=2330.0, help="Vapor pressure [Pa].")
    p.add_argument("--forcing-A", type=float, default=0.0, help="Acoustic forcing amplitude [Pa].")
    p.add_argument("--forcing-f", type=float, default=0.0, help="Acoustic forcing frequency [Hz].")
    p.add_argument("--drag-cd", type=float, default=0.8, help="Quadratic drag coefficient Cd (toy).")
    p.add_argument("--use-stokes", action="store_true",
                   help="Use Stokes drag 6πμR w (low-Re) instead of quadratic drag.")
    return p


def pressure_infty(t: float, z_down: float, fluid: FluidProps, amb: Ambient, forcing: Forcing) -> float:
    """
    Ambient pressure at bubble location in the liquid.
    z_down: depth below surface (positive downward) [m]
    """
    p = amb.Patm + fluid.rho * fluid.g * z_down
    if forcing.A != 0.0 and forcing.f != 0.0:
        p += forcing.A * np.sin(2.0 * np.pi * forcing.f * t)
    return p


def gas_pressure(R: float, R0: float, p0_infty: float, fluid: FluidProps, gas: BubbleGasModel) -> float:
    """
    Polytropic gas model inside bubble.
    Common RP choice:
      Pg(R) = (p0_infty + 2σ/R0 - Pv) * (R0/R)^(3κ) + Pv
    """
    # Ensure positive radius
    R = max(R, 1e-12)
    pref = (p0_infty + 2.0 * fluid.sigma / R0 - gas.Pv)
    return pref * (R0 / R) ** (3.0 * gas.kappa) + gas.Pv


def rp_rising_ode(
    t: float,
    y: np.ndarray,
    *,
    R0: float,
    fluid: FluidProps,
    gas: BubbleGasModel,
    amb: Ambient,
    forcing: Forcing,
    Cd: float,
    use_stokes: bool,
) -> np.ndarray:
    """
    State y = [R, Rdot, z_down, w_up]
      R: bubble radius [m]
      Rdot: dR/dt [m/s]
      z_down: depth below free surface [m] (positive down)
      w_up: upward velocity [m/s] (positive up)
    """

    R, Rdot, z_down, w_up = y
    # Keep radius from going nonphysical
    R = max(R, 1e-9)

    # Ambient pressure at bubble position
    p_inf = pressure_infty(t, z_down, fluid, amb, forcing)

    # Reference p_inf at initial position for gas law
    p0_inf = pressure_infty(0.0, z_down= z_down if np.isfinite(z_down) else 0.0, fluid=fluid, amb=amb, forcing=Forcing(0.0, 0.0))
    # (We use no acoustic forcing for the reference, but same hydrostatic depth.)

    # Gas pressure
    p_g = gas_pressure(R, R0, p0_infty=p0_inf, fluid=fluid, gas=gas)

    # Rayleigh–Plesset:
    # R*Rdd + 3/2 Rdot^2 = (1/ρ)(Pg - Pinf - 2σ/R - 4μ Rdot / R)
    # => Rdd = (1/R)*[(1/ρ)(...) - 3/2 Rdot^2]
    term = (p_g - p_inf - 2.0 * fluid.sigma / R - 4.0 * fluid.mu * Rdot / R) / fluid.rho
    Rdd = (term - 1.5 * Rdot * Rdot) / R

    # Rising model:
    # Use added mass approximation m_a = C_a ρ V, with C_a ~ 0.5 for a sphere in potential flow
    V = (4.0 / 3.0) * np.pi * R ** 3
    Ca = 0.5
    m_added = Ca * fluid.rho * V

    # Buoyancy force upward ~ ρ g V (neglect gas density)
    F_b = fluid.rho * fluid.g * V

    # Drag (downward) opposing motion:
    # Option 1: Stokes drag (low Re): F_d = 6π μ R * w
    # Option 2: Quadratic drag: F_d = 0.5 ρ Cd A w|w|, A=πR^2
    if use_stokes:
        F_d = 6.0 * np.pi * fluid.mu * R * w_up
    else:
        A = np.pi * R ** 2
        F_d = 0.5 * fluid.rho * Cd * A * w_up * abs(w_up)

    # Equation: m_added * dw/dt = F_b - F_d
    # (very simplified: ignores history force, lift, bubble deformation, added-mass derivative terms, etc.)
    if m_added < 1e-15:
        wdot = 0.0
    else:
        wdot = (F_b - F_d) / m_added

    # Kinematics: depth decreases when bubble moves up
    zdot = -w_up

    return np.array([Rdot, Rdd, zdot, wdot], dtype=float)


def main() -> int:
    args = make_parser().parse_args()

    fluid = FluidProps(rho=args.rho, mu=args.mu, sigma=args.sigma)
    gas = BubbleGasModel(kappa=args.kappa, Pv=args.Pv)
    amb = Ambient(Patm=args.Patm)
    forcing = Forcing(A=args.forcing_A, f=args.forcing_f)

    t_eval = np.arange(0.0, args.t_end + args.dt, args.dt, dtype=float)

    # Initial state
    y0 = np.array([args.R0, args.Rdot0, args.z0, args.w0], dtype=float)

    # Integrate
    sol = solve_ivp(
        fun=lambda t, y: rp_rising_ode(
            t, y,
            R0=args.R0,
            fluid=fluid,
            gas=gas,
            amb=amb,
            forcing=forcing,
            Cd=args.drag_cd,
            use_stokes=args.use_stokes,
        ),
        t_span=(t_eval[0], t_eval[-1]),
        y0=y0,
        t_eval=t_eval,
        method="RK45",
        rtol=1e-7,
        atol=1e-10,
    )

    if not sol.success:
        print("Integration failed:", sol.message)
        return 2

    t = sol.t
    R = sol.y[0]
    Rdot = sol.y[1]
    z_down = sol.y[2]
    w_up = sol.y[3]

    # Basic derived quantities
    V = (4.0 / 3.0) * np.pi * np.maximum(R, 0.0) ** 3
    buoyancy = fluid.rho * fluid.g * V

    # ---- Plots ----
    plt.figure()
    plt.plot(t, R * 1e3)
    plt.xlabel("t [s]")
    plt.ylabel("R [mm]")
    plt.title("Rayleigh–Plesset bubble radius")

    plt.figure()
    plt.plot(t, w_up)
    plt.xlabel("t [s]")
    plt.ylabel("w (upward) [m/s]")
    plt.title("Bubble rise velocity")

    plt.figure()
    plt.plot(t, z_down)
    plt.xlabel("t [s]")
    plt.ylabel("z (depth, +down) [m]")
    plt.title("Bubble depth (decreases as it rises)")

    plt.figure()
    plt.plot(t, buoyancy)
    plt.xlabel("t [s]")
    plt.ylabel("Buoyancy force [N]")
    plt.title("Buoyancy (from R(t))")

    plt.show()

    # Print a quick summary
    print(f"Final time: {t[-1]:.6g} s")
    print(f"Final radius: {R[-1]:.6g} m")
    print(f"Final depth: {z_down[-1]:.6g} m (positive down)")
    print(f"Final upward velocity: {w_up[-1]:.6g} m/s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
