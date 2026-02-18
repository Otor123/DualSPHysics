#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

import csv



# ----------------------------------------------------
# Parameter aus der Excel-Tabelle
# ----------------------------------------------------
dpdx = -8.0e-3        # Pressure gradient [Pa/m]
rho  = 1000.0        # Density [kg/m^3]
mu   = 1.0           # Dynamic viscosity [Pa*s]  (nur Info)
nu0  = 1.0e-3        # Kinematic viscosity [m^2/s]
R    = 0.03          # Radius / half-domain width [m]
t    = 0.25          # transient time [s]

# ----------------------------------------------------
# Abgeleitete Größen
# ----------------------------------------------------
L = 2.0 * R          # Plattenabstand [m]
#F = dpdx / rho       # body-force / acceleration [m/s^2]

F = dpdx

# ----------------------------------------------------
# z-Koordinate: von -R bis +R (wie "half domain width")
# ----------------------------------------------------
Nz = 201
z_center = np.linspace(-R, R, Nz)   # [-R, ..., +R]
z_for_formula = z_center + L/2.0    # Shift auf [0, L] für die Formel

# ----------------------------------------------------
# Analytische Lösung für z in [0, L]
# ----------------------------------------------------
def vx_transient_0L(z, t, F, nu, L, N=500):
    """
    v_x(z,t) = F/(2*nu)*z*(z-L) +
               sum_{n=0}^N  4*F*L^2 / (nu*pi^3*(2n+1)^3)
                            * sin(pi*z/L*(2n+1))
                            * exp(-(2n+1)^2*pi^2*nu/L^2 * t)

    z erwartet im Bereich [0, L]
    """
    z = np.asarray(z)

    # stationärer Anteil
    term0 = F / (2.0 * nu) * z * (z - L)

    # Fourierreihen-Anteil
    n = np.arange(0, N)[:, None]    # (N,1)
    k = 2 * n + 1                   # (2n+1)
    z_row = z[None, :]              # (1,Nz)

    pref = 4.0 * F * L**2 / (nu * np.pi**3 * k**3)
    sine = np.sin(np.pi * z_row / L * k)
    expo = np.exp(-(k**2) * np.pi**2 * nu / L**2 * t)

    series = np.sum(pref * sine * expo, axis=0)
    return (term0 + series)*0.5


def vx_steady_0L(z, F, nu, L):
    """Stationäre Poiseuille-Lösung für z in [0,L]."""
    z = np.asarray(z)
    return (F / (4 * nu) * z* (z - L))


# ----------------------------------------------------
# Profile auf deinem z-Gitter berechnen
# ----------------------------------------------------
vx_t  = vx_transient_0L(z_for_formula, t, F, nu0, L, N=500)
vx_ss = vx_steady_0L(z_for_formula, F, nu0, L)

# ----------------------------------------------------
# CSV EXPORT im MeasureTool-Format (13 Werte)
# ----------------------------------------------------

csv_filename = "_Analytical_Poiseuille_13points_MeasureToolFormat.csv"

# 13 Punkte exakt zwischen -0.03 und +0.03
z_positions = np.linspace(-0.03, 0.03, 13)

# analytische Werte auf genau diesen 13 z-Positionen berechnen
z_for_formula_13 = z_positions + L/2.0
vx_t_13  = vx_transient_0L(z_for_formula_13, t, F, nu0, L, N=500)

with open(csv_filename, "w", newline="") as f:
    writer = csv.writer(f, delimiter=';')

    # Kopfzeilen
    writer.writerow(["", "PosX [m]"] + [f"{x:.8f}" for x in z_positions])
    writer.writerow(["", "PosY [m]"] + [0.0 for _ in z_positions])
    writer.writerow(["", "PosZ [m]"] + [0.025 for _ in z_positions])  # Beispiel Z-Koordinate

    # Daten-Header
    writer.writerow(
        ["Part", "Time [s]"] + [f"Vel.z_{i}" for i in range(len(z_positions))]
    )

    # Datenzeile (Part = 0)
    writer.writerow(
        [0, t] + [f"{v:.10f}" for v in vx_t_13]
    )

print(f"CSV exportiert nach: {csv_filename}")

# ----------------------------------------------------
# Plot
# ----------------------------------------------------
plt.figure()
plt.plot(z_center, vx_t, label=f"Transient, t = {t} s")
plt.plot(z_center, vx_ss, "--", label="Steady state (t → ∞)")

plt.xlabel("z [m] (von -R bis +R)")
plt.ylabel(r"$v_x(z)$ [m/s]")
plt.title("Poiseuille-Flow")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
