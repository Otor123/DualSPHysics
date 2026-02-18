import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------
# CSV-Datei einlesen
# --------------------------------------------------------
#CSV_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_Poiseuille/CasePoiseuille_NS_LR_3D_mDBC_out_WORKS/measuretool/_PointsVelocity_Vel.x.csv"   # <-- anpassen falls nötig
#CSV_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_Poiseuille/CasePoiseuille_NS_LR_3D_mDBC_out/measuretool/_PointsVelocity_Vel.x.csv"   # <-- anpassen falls nötig

CSV_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Poisuelle_mDBC_out/measuretool/_PointsVelocity_Vel.x.csv" 



PARTS = [10, 20, 30, 40, 50]                          # gewünschter Part

# ---------------------------------------------------------
# 1) Gesamte CSV einmal roh einlesen, um PosZ zu bekommen
# ---------------------------------------------------------
raw = pd.read_csv(CSV_FILE, sep=";", header=None)

# Zeile mit PosZ ist die dritte Zeile (Index 2)
# Spalten ab Index 2 sind die Zahlenwerte
z_values = raw.iloc[2, 2:].astype(float).values

## ---------------------------------------------------------
# 2) Datenbereich einlesen (mit Header)
# ---------------------------------------------------------
data = pd.read_csv(CSV_FILE, sep=";", skiprows=3)

# ---------------------------------------------------------
# Plot vorbereiten
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

for part_id in PARTS:

    # Zeile für gewünschten Part finden
    row = data.loc[data["Part"] == part_id]
    if row.empty:
        print(f"⚠️  Part {part_id} nicht gefunden, wird übersprungen…")
        continue

    row = row.iloc[0]

    vel_cols = [c for c in data.columns if c.startswith("Vel.x_")]
    vel_values = row[vel_cols].values.astype(float)

    # Plotten
    plt.plot(z_values, vel_values, marker="o", linewidth=1.5, label=f"Part {part_id}")

# ---------------------------------------------------------
# Plot finalisieren
# ---------------------------------------------------------
plt.xlabel("Z-Koordinate [m]")
plt.ylabel("Vel.x [m/s]")
plt.title("Vel.x über Z für mehrere Parts")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
