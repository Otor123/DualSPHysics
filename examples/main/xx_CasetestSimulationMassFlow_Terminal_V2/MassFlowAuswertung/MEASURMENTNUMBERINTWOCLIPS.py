#!/usr/bin/env python3
"""
DualSPHysics-Postprocessing:

- liest eine Serie von PartFluid_*.vtk Dateien ein
- schneidet jede Datei mit einer Clip-Ebene in zwei Teile (oben/unten)
- zählt die Partikel in beiden Clips
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
DATA_DIR = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/periodicity/periodicity_out/particles/"    # <--- HIER anpassen

DATA_DIR = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/xx_CasetestSimulationMassFlow_Terminal_V3Simple/SimplaeTest_Aufangbehälter_V2/SimplaeTest_Aufangbehälter_V2_out/particles/"

# Dateimuster für DualSPHysics-Partikel
PATTERN = "PartFluid_*.vtk"

# Clip-Plane (wie in ParaView eingestellt)
# Werte aus deinem Screenshot: Origin = (0.03, 0.02, 0.1), Normal = (0, 0, 1)
CLIP_ORIGIN = (0.03, 0.02, 0.1)
CLIP_ORIGIN = (0.125, 0.125, 1.05)
CLIP_NORMAL = (0.0, 0.0, 1.0)

# Name der Ergebnis-CSV
OUTPUT_CSV = "ParticleCount_Clips_V2.csv"

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
            "N_upper_clip",   # Seite der Normalen (nicht invertiert)
            "N_lower_clip"    # invertierte Seite (andere Hälfte)
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

            # Clip oben (Seite der Normalen)
            clip_upper = mesh.clip(origin=CLIP_ORIGIN,
                                   normal=CLIP_NORMAL,
                                   invert=False)
            n_upper = clip_upper.n_points

            # Clip unten (invertierte Seite)
            clip_lower = mesh.clip(origin=CLIP_ORIGIN,
                                   normal=CLIP_NORMAL,
                                   invert=True)
            n_lower = clip_lower.n_points

            # In CSV schreiben
            writer.writerow([
                step if step is not None else "",
                os.path.basename(vtk_path),
                n_total,
                n_upper,
                n_lower,
            ])

    print(f"Fertig. Ergebnisse in '{OUTPUT_CSV}' gespeichert.")


if __name__ == "__main__":
    main()
