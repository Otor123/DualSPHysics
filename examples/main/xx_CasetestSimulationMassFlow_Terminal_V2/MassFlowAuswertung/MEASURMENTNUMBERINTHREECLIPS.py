#!/usr/bin/env python3
"""
DualSPHysics-Postprocessing:

- liest eine Serie von PartFluid_*.vtk Dateien ein
- schneidet jede Datei mit zwei Clip-Ebenen in drei Teile (unten/mitte/oben)
- zählt die Partikel in allen drei Bereichen
- speichert die Ergebnisse in einer CSV-Datei

Voraussetzungen:
    pip install pyvista numpy
"""

import os
import glob
import re
import csv

import pyvista as pv
from typing import Optional

# ---------------------------------------------------------------------------
# KONFIGURATION
# ---------------------------------------------------------------------------

# Ordner mit den VTK-Dateien
DATA_DIR = (
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/"
    "DualSPHysics/examples/main/periodicity/periodicity_out/particles/"
)

# Dateimuster für DualSPHysics-Partikel
PATTERN = "PartFluid_*.vtk"

# Zwei Clip-Planen wie in ParaView:
#  - Clip unten/mitte-Grenze (z1)
#  - Clip mitte/oben-Grenze (z2)
# Werte aus deinen Screenshots:
#   Origin1 = (0.03, 0.03, 0.075)
#   Origin2 = (0.03, 0.03, 0.15)
CLIP1_ORIGIN = (0.03, 0.03, 0.075)   # untere Grenze
CLIP2_ORIGIN = (0.03, 0.03, 0.15)    # obere Grenze
CLIP_NORMAL  = (0.0, 0.0, 1.0)       # Normal in +z-Richtung

# Name der Ergebnis-CSV
OUTPUT_CSV = "ParticleCount_3Regions.csv"

# ---------------------------------------------------------------------------
# HILFSFUNKTION: Schritt aus Dateinamen extrahieren
# ---------------------------------------------------------------------------

step_regex = re.compile(r"PartFluid_(\d+)\.vtk")


def extract_step(filename: str) -> Optional[int]:
    """
    Versucht, aus 'PartFluid_0000.vtk' die Zahl 0 zu extrahieren.
    Gibt None zurück, falls es nicht klappt.
    """
    base = os.path.basename(filename)
    m = step_regex.match(base)
    if m:
        return int(m.group(1))
    return None


# ---------------------------------------------------------------------------
# HAUPTLOGIK
# ---------------------------------------------------------------------------

def main():
    # Alle passenden Dateien holen und sortieren
    files = sorted(glob.glob(os.path.join(DATA_DIR, PATTERN)))
    if not files:
        print(f"Keine Dateien nach Muster {PATTERN} in {DATA_DIR} gefunden.")
        return

    print(f"{len(files)} VTK-Dateien gefunden.")

    # CSV vorbereiten
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        # Kopfzeile
        writer.writerow([
            "step",
            "filename",
            "N_total",
            "N_lower",   # z < z1
            "N_middle",  # z1 <= z <= z2
            "N_upper"    # z > z2
        ])

        # Dateien durchgehen
        for vtk_path in files:
            print(f"Bearbeite {vtk_path} ...")

            # Schrittzahl aus Dateinamen
            step = extract_step(vtk_path)

            # VTK einlesen
            dataset = pv.read(vtk_path)

            # Falls es ein MultiBlock ist, alles zusammenführen
            if isinstance(dataset, pv.MultiBlock):
                mesh = dataset.combine()
            else:
                mesh = dataset

            # Gesamtanzahl Partikel
            n_total = mesh.n_points

            # -----------------------------
            # UNTERER BEREICH: z < z1
            # -----------------------------
            lower_region = mesh.clip(origin=CLIP1_ORIGIN,
                                     normal=CLIP_NORMAL,
                                     invert=True)
            n_lower = lower_region.n_points

            # -----------------------------
            # OBERER BEREICH: z > z2
            # -----------------------------
            upper_region = mesh.clip(origin=CLIP2_ORIGIN,
                                     normal=CLIP_NORMAL,
                                     invert=False)
            n_upper = upper_region.n_points

            # -----------------------------
            # MITTLERER BEREICH: z1 <= z <= z2
            # erst z >= z1 clippen, dann z <= z2
            # -----------------------------
            tmp = mesh.clip(origin=CLIP1_ORIGIN,
                            normal=CLIP_NORMAL,
                            invert=False)  # z >= z1
            middle_region = tmp.clip(origin=CLIP2_ORIGIN,
                                     normal=CLIP_NORMAL,
                                     invert=True)  # z <= z2
            n_middle = middle_region.n_points

            # In CSV schreiben
            writer.writerow([
                step if step is not None else "",
                os.path.basename(vtk_path),
                n_total,
                n_lower,
                n_middle,
                n_upper,
            ])

    print(f"Fertig. Ergebnisse in '{OUTPUT_CSV}' gespeichert.")


if __name__ == "__main__":
    main()
