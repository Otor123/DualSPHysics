import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------------
# Pfade
# --------------------------------------------------------
SIM_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001/measuretool/_PointsVelocity_Vel.z.csv"

#8s - .../mdbc/02_4_FreeCadPosieulleBigExample/ - NVIDIA GeForce RTX 2080 Ti
SIM_FILE = "/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_8s_GPU/measuretool/_PointsVelocity_Vel.z.csv"
#16s - mdbc/02_4_FreeCadPosieulleBigExample/ - NVIDIA GeForce RTX 3080
SIM_FILE = "/nishome/PaulS/Desktop/ParameterStudie/FirstResultsSimulation/Posieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv"

ANA_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_1_0.csv"


SIM_FILE =    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesRe<</_PointsVelocity_Vel.z.csv"
SIM_FILE =    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/setDRWMode/smallPipe_FreeCAD/_PointsVelocity_Vel.z.csv"
ANA_FILE =    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesRe<</AnalyticalTransientProfile_t_All.csv"


PARTS = [ 10, 25, 300]
X_TARGET = 0.1  # Zielposition

# --------------------------------------------------------
# X-Positionen aus Kopfzeile lesen
# --------------------------------------------------------
raw_sim = pd.read_csv(SIM_FILE, sep=";", header=None)
x_values = raw_sim.iloc[0, 2:].astype(float).values

# Index der Position 0.1 m
idx = int(np.argmin(np.abs(x_values - X_TARGET)))
x_nearest = x_values[idx]
vel_col = f"Vel.z_{idx}"

print(f"Using index {idx} -> X ≈ {x_nearest:.6f} m (target = {X_TARGET})")
print(f"Velocity column: {vel_col}\n")

# --------------------------------------------------------
# Daten einlesen
# --------------------------------------------------------
sim = pd.read_csv(SIM_FILE, sep=";", skiprows=3)
ana = pd.read_csv(ANA_FILE, sep=";", skiprows=3)

time_col = [c for c in sim.columns if "Time" in c][0]  # z.B. "Time [s]"

# --------------------------------------------------------
# Fehler sammeln
# --------------------------------------------------------
times = []
errors = []

for part in PARTS:
    row_sim = sim.loc[sim["Part"] == part]
    row_ana = ana.loc[ana["Part"] == part]

    if row_sim.empty or row_ana.empty:
        print(f"⚠️ Part {part} fehlt in einer Datei.")
        continue

    t = float(row_sim[time_col].iloc[0])
    v_sim = float(row_sim[vel_col].iloc[0])
    v_ana = float(row_ana[vel_col].iloc[0])
    err = v_sim - v_ana

    times.append(t)
    errors.append(err)

    print(f"Part {part}: t = {t:.4f} s,  err = {err:+.4e}")

# --------------------------------------------------------
# Plot
# --------------------------------------------------------
plt.figure(figsize=(10,6))
plt.plot(times, errors, marker="o", linewidth=2, markersize=8)

plt.title(f"Error at x ≈ {x_nearest:.3f} m  (sim − analytical)")
plt.xlabel("Time [s]")
plt.ylabel("Error in Vel.z [m/s]")
plt.grid(True, alpha=0.4)

for t, e in zip(times, errors):
    plt.text(t, e, f"{e:.2e}", fontsize=9, ha="left", va="bottom")

plt.tight_layout()
plt.show()
