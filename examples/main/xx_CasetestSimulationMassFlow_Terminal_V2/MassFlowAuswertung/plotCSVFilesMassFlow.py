import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import re

# --- Ordner mit den CSVs ---
FOLDER = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/xx_CasetestSimulationMassFlow_Terminal_V2/MassFlowAuswertung/plotSamplingIncrease"

files = sorted(glob.glob(os.path.join(FOLDER, "MassFlow_dp_*.csv")))

plt.figure(figsize=(10, 6))
x_label = "step"  # Default-Wert, falls 'time' überall leer ist

for f in files:
    df = pd.read_csv(f)

    if not {"step", "N", "avg_vel"}.issubset(df.columns):
        print(f"Überspringe {f}, Spalten nicht gefunden:", df.columns)
        continue

    # Zeit oder Step als x-Achse
    if df["time"].notna().any():
        x = df["time"].fillna(method="ffill").fillna(0)
        x_label = "time"
    else:
        x = df["step"]

    # vel * N berechnen
    df["velN"] = df["avg_vel"].fillna(0) * df["N"].fillna(0) * df["avg_Rhop"].fillna(0)
    #df["velN"] = df["avg_vel"].fillna(0) * df["avg_Rhop"].fillna(0)
    # DP und in/out aus Dateiname extrahieren
    fname = os.path.basename(f)
    match = re.search(r"dp_(\d*\.?\d+)_?(in|out)?", fname)
    if match:
        dp = match.group(1)
        direction = match.group(2) if match.group(2) else "?"
        label = f"dp={dp} ({direction})"
    else:
        label = fname.replace(".csv", "")

    # Linienstil je nach Richtung
    linestyle = "--" if "out" in fname else "-"
    plt.plot(x, df["velN"], linestyle=linestyle, label=label)

plt.xlabel(x_label)
plt.ylabel("avg_vel * N * avg_Rhop")
plt.title("vel * N * rhop über Zeitschritte")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
