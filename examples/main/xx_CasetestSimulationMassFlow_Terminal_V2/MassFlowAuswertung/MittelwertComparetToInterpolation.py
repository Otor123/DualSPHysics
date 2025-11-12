#!/usr/bin/env python3
"""
Plot der mittleren Geschwindigkeiten aus der CSV-Datei:
    - avg_vel (einfacher Mittelwert)
    - avg_vel_sph (SPH-geglätteter Mittelwert)
    
Die CSV-Datei stammt aus dem SPH-Postprocessing-Skript.

Voraussetzungen:
    pip install pandas matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------------------------
# KONFIGURATION
# ---------------------------------------------------------------------------

CSV_FILE = "MassFlow_dp_0.0015_out_sphvel.csv"  # Pfad zur CSV-Datei
X_AXIS = "step"  # "time" oder "step" (je nachdem, was in deiner CSV steht)

# ---------------------------------------------------------------------------
# EINLESEN
# ---------------------------------------------------------------------------

if not os.path.exists(CSV_FILE):
    raise FileNotFoundError(f"CSV-Datei '{CSV_FILE}' nicht gefunden!")

df = pd.read_csv(CSV_FILE)

print(f"Datei '{CSV_FILE}' erfolgreich geladen:")
print(df.head())

# Prüfen, welche Spalten vorhanden sind
required_cols = {"avg_vel", "avg_vel_sph"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Fehlende Spalten in CSV: {missing}")

# ---------------------------------------------------------------------------
# PLOTTEN
# ---------------------------------------------------------------------------

plt.figure(figsize=(10, 6))
x = df[X_AXIS]

plt.plot(x, df["avg_vel"], label="avg_vel (roh)", lw=2, color="tab:blue")
plt.plot(x, df["avg_vel_sph"], label="avg_vel_sph (SPH-geglättet)", lw=2, color="tab:orange")

plt.xlabel("Time" if X_AXIS == "time" else "Step", fontsize=12)
plt.ylabel("Mean Velocity [m/s]", fontsize=12)
plt.title("Vergleich: avg_vel vs. SPH-geglättete avg_vel_sph", fontsize=13)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# ---------------------------------------------------------------------------
# SPEICHERN & ANZEIGEN
# ---------------------------------------------------------------------------

output_png = os.path.splitext(CSV_FILE)[0] + "_plot.png"
plt.savefig(output_png, dpi=200)
print(f"Plot gespeichert als: {output_png}")

plt.show()
