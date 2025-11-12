#!/usr/bin/env python3
"""
Postprocessing für DualSPHysics / ParaView:
- liest eine Serie von PartFluid_*.vtk Dateien ein
- wendet einen Z-Bereich (zwischen zwei "Clip-Planes") an
- berechnet im jeweiligen Clip:
    * Anzahl der Partikel (N)
    * mittlere Geschwindigkeit (Betrag von 'Vel')
    * SPH-geglättete mittlere Geschwindigkeit (Wendland-Quintic-Kernel)
    * mittlere Dichte Rhop

Ergebnis wird in eine CSV-Datei geschrieben.

Voraussetzungen:
    pip install pyvista numpy
"""

import os
import glob
import csv

import numpy as np
import pyvista as pv


# ---------------------------------------------------------------------------
# KONFIGURATION
# ---------------------------------------------------------------------------

DATA_DIR = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/xx_CasetestSimulationMassFlow_Terminal_V3Simple/SimplaeTest_Aufangbehälter_V2/SimplaeTest_Aufangbehälter_V2_out_T_6s/particles"  # <- hier ggf. Pfad anpassen


# Dateimuster für deine Partikel-Dateien
FILE_PATTERN = "PartFluid_*.vtk"
VEL_ARRAY_NAME = "Vel"
RHOP_ARRAY_NAME = "Rhop"

# SPH-Parameter
DP    = 0.003
COEFH = 0.87
# h = coefh * sqrt(3 * dp^2)
H_SMOOTH = COEFH * np.sqrt(3.0 * DP**2)

# Bereich zwischen den beiden Clip-Planes (Z-Koordinaten)
# In:
Z_MIN = 1.05
Z_MAX = 1.10

# Out:
#Z_MIN = 0.75
#Z_MAX = 0.80

OUTPUT_CSV = "MassFlow_dp_0.0015_out_sphvel.csv"


# ---------------------------------------------------------------------------
# Wendland-Quintic-Kernel (3D)
# ---------------------------------------------------------------------------

def wendland_quintic_kernel(r, h):
    """
    3D Wendland Quintic Kernel (Monaghan 2000):

        W(r,h) = α_D * (1 - q/2)^4 * (2q + 1),   0 <= q <= 2
        q = r / h
        α_D = 21 / (16 π h^3)

    Parameter
    ---------
    r : array_like
        Abstände |r_a - r_b|
    h : float
        smoothing length

    Rückgabe
    --------
    W : ndarray
        Kernelwerte gleicher Form wie r
    """
    r = np.asarray(r)
    q = r / h
    W = np.zeros_like(q)

    alpha = 21.0 / (16.0 * np.pi * h**3)

    mask = (q >= 0.0) & (q <= 2.0)
    qm = q[mask]

    W[mask] = alpha * (1.0 - qm / 2.0)**4 * (2.0 * qm + 1.0)

    # für q > 2 bereits 0
    return W


def sph_smoothed_velocity(pts, vel_mag, h):
    """
    Berechnet für jedes Partikel im Clip eine SPH-geglättete Geschwindigkeit:

        V_a = sum_b V_b W_ab / sum_b W_ab

    Hinweis: Hier werden nur Partikel innerhalb des Clips als Nachbarn b
    verwendet. Wenn du streng physikalisch alle Nachbarn (auch außerhalb
    des Clips) nehmen willst, müsstest du pts/vel_mag aus dem gesamten
    Fluid einsetzen.

    Parameter
    ---------
    pts : (N,3) ndarray
        Positionen der Partikel (hier: im Clip)
    vel_mag : (N,) ndarray
        Geschwindigkeitsbeträge der Partikel (im Clip)
    h : float
        smoothing length

    Rückgabe
    --------
    V_smooth : (N,) ndarray
        SPH-geglättete Geschwindigkeit je Partikel
    """
    N = pts.shape[0]
    V_smooth = np.zeros(N)

    # Brute-force O(N^2). Für sehr große N kann das langsam werden.
    for a in range(N):
        ra = pts[a]
        # Abstände zu allen Partikeln (einschließlich sich selbst)
        r_ab = np.linalg.norm(pts - ra, axis=1)
        W_ab = wendland_quintic_kernel(r_ab, h)

        denom = np.sum(W_ab)
        if denom > 0.0:
            V_smooth[a] = np.sum(vel_mag * W_ab) / denom
        else:
            # Fallback: keine sinnvollen Nachbarn
            V_smooth[a] = vel_mag[a]

    return V_smooth


# ---------------------------------------------------------------------------
# HAUPTFUNKTION PRO FILE
# ---------------------------------------------------------------------------

def compute_between_planes(mesh, zmin, zmax, step, fname, h_sph=None):
    """
    Wählt Partikel im gewünschten Z-Bereich und berechnet Kennwerte.
    """
    pts = mesh.points
    mask = (pts[:, 2] >= zmin) & (pts[:, 2] <= zmax)

    N = int(np.count_nonzero(mask))

    avg_vel     = float("nan")  # einfacher Mittelwert
    avg_vel_sph = float("nan")  # SPH-geglätteter Mittelwert
    avg_rhop    = float("nan")

    if N > 0:
        # --- Geschwindigkeit / Vel ---
        if VEL_ARRAY_NAME not in mesh.point_data:
            raise KeyError(
                f"Feld '{VEL_ARRAY_NAME}' nicht gefunden. "
                f"Verfügbare Felder: {list(mesh.point_data.keys())}"
            )
        vel = np.asarray(mesh.point_data[VEL_ARRAY_NAME])
        if vel.ndim == 2 and vel.shape[1] >= 3:
            vel_mag_all = np.linalg.norm(vel[:, :3], axis=1)
        else:
            vel_mag_all = vel

        pts_clip = pts[mask]
        vel_clip = vel_mag_all[mask]

        # einfacher Mittelwert im Clip
        avg_vel = float(np.mean(vel_clip))

        # SPH-geglättete Geschwindigkeit im Clip (falls h_sph gesetzt)
        if h_sph is not None:
            V_smooth = sph_smoothed_velocity(pts_clip, vel_clip, h_sph)
            avg_vel_sph = float(np.mean(V_smooth))

        # --- Rhop ---
        if RHOP_ARRAY_NAME not in mesh.point_data:
            raise KeyError(
                f"Feld '{RHOP_ARRAY_NAME}' nicht gefunden. "
                f"Verfügbare Felder: {list(mesh.point_data.keys())}"
            )
        rhop = np.asarray(mesh.point_data[RHOP_ARRAY_NAME])
        avg_rhop = float(np.mean(rhop[mask]))

    # Time aus field_data holen (falls vorhanden)
    time_val = None
    if "TimeValue" in mesh.field_data:
        arr = np.asarray(mesh.field_data["TimeValue"]).ravel()
        if arr.size:
            time_val = float(arr[0])

    return dict(
        step=step,
        time=time_val,
        file=os.path.basename(fname),
        N=N,
        avg_vel=avg_vel,
        avg_vel_sph=avg_vel_sph,
        avg_Rhop=avg_rhop,
    )


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    files = sorted(glob.glob(os.path.join(DATA_DIR, FILE_PATTERN)))
    if not files:
        raise FileNotFoundError(f"Keine VTK-Dateien für Pattern {FILE_PATTERN} gefunden.")

    results = []
    for i, f in enumerate(files):
        print(f"Processing {f}")
        mesh = pv.read(f)
        res = compute_between_planes(mesh, Z_MIN, Z_MAX, i, f, h_sph=H_SMOOTH)
        results.append(res)

    fieldnames = ["step", "time", "file", "N", "avg_vel", "avg_vel_sph", "avg_Rhop"]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Fertig. Ergebnisse in '{OUTPUT_CSV}' gespeichert.")
    print(f"Verwendeter smoothing length h = {H_SMOOTH:.6f}")


if __name__ == "__main__":
    main()
