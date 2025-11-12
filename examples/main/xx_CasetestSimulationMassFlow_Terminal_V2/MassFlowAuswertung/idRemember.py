#!/usr/bin/env python3
"""
Liest alle PartFluid_*.vtk in DATA_DIR ein und schreibt die Partikel-IDs
in eine CSV-Datei.

Ausgabe-CSV: particle_ids_allsteps.csv
Spalten:
    step        -> Zeitschritt (aus Dateinamen)
    file        -> Dateiname
    particle_ix -> laufender Index des Partikels im VTK (0..N-1)
    id          -> Partikel-ID (aus dem VTK-Array)
"""

import os
import glob
import csv
import re

import pyvista as pv


# ---------------------------------------------------------------------------
# KONFIGURATION
# ---------------------------------------------------------------------------

DATA_DIR = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/xx_CasetestSimulationMassFlow_Terminal_V3Simple/SimplaeTest_Aufangbehälter_V2/SimplaeTest_Aufangbehälter_V2_out_T_6s/particles/"
OUTPUT_CSV = os.path.join(DATA_DIR, "particle_ids_allsteps.csv")

# Kandidatennamen für das ID-Array im VTK
ID_CANDIDATES = ["Idp", "idp", "Id", "id", "ParticleId", "ParticleID"]


# ---------------------------------------------------------------------------
# HILFSFUNKTIONEN
# ---------------------------------------------------------------------------

def extract_step_from_filename(fname: str) -> int:
    """
    Holt die Schrittzahl aus 'PartFluid_0003.vtk' -> 3
    Falls nichts gefunden wird, wird -1 zurückgegeben.
    """
    m = re.search(r"PartFluid_(\d+)\.vtk$", os.path.basename(fname))
    if m:
        return int(m.group(1))
    return -1


def find_id_array(mesh: pv.DataSet):
    """
    Versucht, ein passendes ID-Array im point_data zu finden.
    Gibt (name, array) oder (None, None) zurück.
    """
    for name in ID_CANDIDATES:
        if name in mesh.point_data:
            return name, mesh.point_data[name]
    return None, None


# ---------------------------------------------------------------------------
# HAUPTLOGIK
# ---------------------------------------------------------------------------

def main():
    vtk_files = sorted(glob.glob(os.path.join(DATA_DIR, "PartFluid_*.vtk")))
    if not vtk_files:
        print("Keine PartFluid_*.vtk in", DATA_DIR)
        return

    print(f"Gefundene Dateien: {len(vtk_files)}")

    with open(OUTPUT_CSV, "w", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["step", "file", "particle_ix", "id"])

        for vtk_path in vtk_files:
            step = extract_step_from_filename(vtk_path)
            print(f"Verarbeite {os.path.basename(vtk_path)} (step={step}) ...")

            mesh = pv.read(vtk_path)

            id_name, id_array = find_id_array(mesh)
            if id_name is None:
                print(f"  -> KEIN ID-Array gefunden in {vtk_path}. "
                      f"Vorhandene point_data: {list(mesh.point_data.keys())}")
                continue

            print(f"  -> benutze ID-Array: '{id_name}', N={len(id_array)}")

            for i, pid in enumerate(id_array):
                writer.writerow([step, os.path.basename(vtk_path), i, int(pid)])

    print("Fertig. CSV geschrieben nach:", OUTPUT_CSV)


if __name__ == "__main__":
    main()
