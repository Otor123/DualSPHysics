#!/usr/bin/env python3
"""
Berechnet den Massestrom über die beiden Clip-Ebenen aus ParticleCount_3Regions.csv

Voraussetzungen:
    pip install pandas numpy
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# USER-EINSTELLUNGEN  -> HIER ANPASSEN
# ---------------------------------------------------------------------------

# Eingabe-/Ausgabedateien
INPUT_CSV  = "ParticleCount_3Regions.csv"          # ggf. Dateinamen anpassen
OUTPUT_CSV = "MassFlow_FromParticles_3Regions.csv"

# Fluiddichte [kg/m^3]
rho0 = 1000.0       # z.B. Wasser

# Partikelabstand dp [m]
dp = 0.003          # HIER deinen dp eintragen

# Dimension der Simulation: 3D oder 2D
dimension = 3       # 3 für 3D, 2 für 2D

# Falls 2D: angenommene "Dicke" in z-Richtung [m]
thickness_2d = 1.0  # nur relevant bei dimension == 2

# Zeitschritt pro "step" [s]
dt_per_step = 1e-4  # HIER dein Delta t pro PartFluid_XXXX angeben


# ---------------------------------------------------------------------------
# MASSEN PRO PARTIKEL
# ---------------------------------------------------------------------------

if dimension == 3:
    particle_volume = dp**3
elif dimension == 2:
    particle_volume = dp**2 * thickness_2d
else:
    raise ValueError("dimension muss 2 oder 3 sein.")

m_particle = rho0 * particle_volume     # kg pro Partikel

print(f"Teilchenmasse m_p = {m_particle:.6e} kg")


# ---------------------------------------------------------------------------
# CSV EINLESEN
# ---------------------------------------------------------------------------

df = pd.read_csv(INPUT_CSV, sep=";")

# Zeitspalte hinzufügen
df["time"] = df["step"] * dt_per_step


# ---------------------------------------------------------------------------
# ÄNDERUNG DER PARTIKELZAHL PRO STEP
# ---------------------------------------------------------------------------
# N_lower  : Bereich z < z1
# N_middle : Bereich z1 <= z <= z2
# N_upper  : Bereich z > z2

df["dN_lower"]  = df["N_lower"].diff().fillna(0)
df["dN_middle"] = df["N_middle"].diff().fillna(0)
df["dN_upper"]  = df["N_upper"].diff().fillna(0)

# ---------------------------------------------------------------------------
# SPEICHERN
# ---------------------------------------------------------------------------

df.to_csv(OUTPUT_CSV, sep=";", index=False)
print(f"fertig. Ergebnisse in '{OUTPUT_CSV}' gespeichert.")
