#!/usr/bin/env python3
"""
Postprocessing für DualSPHysics / ParaView:
- liest eine Serie von PartFluid_*.vtk Dateien ein
- wendet zwei Clip-Ebenen (wie Clip5 und Clip6 in ParaView) an
- berechnet im jeweiligen Clip:
    * Anzahl der Partikel (N)
    * mittlere Geschwindigkeit (Betrag von 'Vel')
- schreibt die Ergebnisse in eine CSV-Datei

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

# Ordner mit den VTK-Dateien
DATA_DIR = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/xx_CasetestSimulationMassFlow_Terminal_V3Simple/SimplaeTest_Aufangbehälter_V4_dp_0.0015/SimplaeTest_Aufangbehälter_V2_out/particles/"  # <- hier ggf. Pfad anpassen
DATA_DIR = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/xx_CasetestSimulationMassFlow_Terminal_V3Simple/SimplaeTest_Aufangbehälter_V2/SimplaeTest_Aufangbehälter_V2_out/particles/"  # <- hier ggf. Pfad anpassen


# Dateimuster für deine Partikel-Dateien
FILE_PATTERN = "PartFluid_*.vtk"
VEL_ARRAY_NAME = "Vel"
RHOP_ARRAY_NAME = "Rhop"

# Bereich zwischen den beiden Clip-Planes (Z-Koordinaten)
#In
#Z_MIN = 1.05
#Z_MAX = 1.10

#
#Out
Z_MIN = 0.75
Z_MAX = 0.8

OUTPUT_CSV = "MassFlow_dp_0.003_out_SamplingIncrease.csv"
# ------------------------------------------------------------

def compute_between_planes(mesh, zmin, zmax, step, fname):
    pts = mesh.points
    mask = (pts[:, 2] >= zmin) & (pts[:, 2] <= zmax)

    N = int(np.count_nonzero(mask))

    # Default-Werte
    avg_vel  = float("nan")
    avg_rhop = float("nan")

    if N > 0:
        # --- Geschwindigkeit ---
        if VEL_ARRAY_NAME not in mesh.point_data:
            raise KeyError(
                f"Feld '{VEL_ARRAY_NAME}' nicht gefunden. "
                f"Verfügbare Felder: {list(mesh.point_data.keys())}"
            )
        vel = np.asarray(mesh.point_data[VEL_ARRAY_NAME])
        if vel.ndim == 2 and vel.shape[1] >= 3:
            vel_mag = np.linalg.norm(vel[:, :3], axis=1)
        else:
            vel_mag = vel
        avg_vel = float(np.mean(vel_mag[mask]))

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
        avg_Rhop=avg_rhop,
    )

def main():
    files = sorted(glob.glob(os.path.join(DATA_DIR, FILE_PATTERN)))
    if not files:
        raise FileNotFoundError(f"Keine VTK-Dateien für Pattern {FILE_PATTERN} gefunden.")

    results = []
    for i, f in enumerate(files):
        print(f"Processing {f}")
        mesh = pv.read(f)
        results.append(compute_between_planes(mesh, Z_MIN, Z_MAX, i, f))

    fieldnames = ["step", "time", "file", "N", "avg_vel", "avg_Rhop"]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Fertig. Ergebnisse in '{OUTPUT_CSV}' gespeichert.")

if __name__ == "__main__":
    main()
