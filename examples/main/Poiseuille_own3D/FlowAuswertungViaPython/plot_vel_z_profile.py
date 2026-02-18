#!/usr/bin/env python3
"""
Liest die spezielles DualSPHysics-CSV (low_ruler_plane_Vel.csv) ein
und plottet Vel_z in Abhängigkeit von y für alle Partikel an der
Position x ≈ X_TARGET und z ≈ Z_TARGET.

Annahmen über Dateiformat (wie in low_ruler_plane_Vel.csv):
- Trennzeichen: Semikolon ;
- Zeile 0: "Pos X/Y/Z [m]:", dann (x0,y0,z0,x1,y1,z1,...) für alle Partikel
- Zeile 1: "Part", "Time [s]", dann für jeden Partikel (Vel_i.x, Vel_i.y, Vel_i.z)
- Zeilen 2..N: Datenzeilen mit Part-Index, Zeit und Geschwindigkeiten
"""

import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------------------------
# USER-EINSTELLUNGEN
# --------------------------------------------------------------------
CSV_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/Poiseuille_own3D/periodicity_out_dp_0.001/Measurment/low_ruler_plane_Vel.csv"  # Pfad zur Datei
CSV_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/Poiseuille_own3D/periodicity_out_0.0005/Measurment/low_ruler_plane_Vel.csv"  # Pfad zur Datei
X_TARGET = 0.03                       # gewünschtes x
Z_TARGET = 0.079                      # gewünschtes z
TOL      = 1e-4#1e-3                       # Toleranz für Vergleich von x und z

# Datenzeile wählen:
#   Zeilenindex in der CSV (0-basiert):
#   0: Positionszeile, 1: Header für Vel,
#   2: erste Datenzeile, 3: zweite Datenzeile, ...
DATA_ROW_INDEX = 3 # <-- hier kannst du z.B. 3,4,... setzen für andere Zeiten


def main():
    # ----------------------------------------------------------------
    # CSV einlesen (ohne Header, Semikolon als Separator)
    # ----------------------------------------------------------------
    df = pd.read_csv(CSV_FILE, sep=";", header=None)

    ncols = df.shape[1]
    pos_row = df.iloc[0]  # Zeile mit Positionen (x,y,z,...)

    # ----------------------------------------------------------------
    # Partikel finden, die bei x≈X_TARGET und z≈Z_TARGET liegen
    # ----------------------------------------------------------------
    particle_indices = []
    ys = []

    i = 0
    while True:
        base = 2 + 3 * i  # Spalte von x(i)
        if base + 2 >= ncols:
            break  # keine weiteren Partikel-Spalten

        try:
            x = float(pos_row[base])
            y = float(pos_row[base + 1])
            z = float(pos_row[base + 2])
        except ValueError:
            # falls irgendwas kein float ist -> abbrechen
            break

        if abs(x - X_TARGET) < TOL and abs(z - Z_TARGET) < TOL:
            particle_indices.append(i)
            ys.append(y)

        i += 1

    if not particle_indices:
        print("❗ Keine Partikel mit x≈{} und z≈{} gefunden.".format(X_TARGET, Z_TARGET))
        return

    # ----------------------------------------------------------------
    # Vel_z für die ausgewählte Datenzeile auslesen
    # ----------------------------------------------------------------
    if DATA_ROW_INDEX >= len(df):
        print(f"❗ DATA_ROW_INDEX={DATA_ROW_INDEX} existiert nicht in der Datei.")
        return

    data_row = df.iloc[DATA_ROW_INDEX]

    vel_z_values = []
    for i in particle_indices:
        base_vel = 2 + 3 * i      # Vel_i.x Spalte
        col_vel_z = base_vel + 2  # Vel_i.z Spalte
        try:
            vz = float(data_row[col_vel_z])
        except ValueError:
            vz = float("nan")
        vel_z_values.append(vz)

    # Nach y sortieren, damit der Plot „sauber“ aussieht
    pairs = sorted(zip(ys, vel_z_values), key=lambda p: p[0])
    ys_sorted, vz_sorted = zip(*pairs)

    # ----------------------------------------------------------------
    # Plot
    # ----------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    plt.plot(ys_sorted, vz_sorted, marker="o")
    plt.xlabel("y [m]")
    plt.ylabel("Vel_z [m/s]")
    plt.title(f"Vel_z an x={X_TARGET}, z={Z_TARGET} (Datenzeile {DATA_ROW_INDEX})")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
