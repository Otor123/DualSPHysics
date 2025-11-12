import pandas as pd
import matplotlib.pyplot as plt

# --- Dateien laden ---
df_in = pd.read_csv("plotSamplingIncrease/MassFlow_dp_0.003_in_SamplingIncrease.csv")
df_out = pd.read_csv("plotSamplingIncrease/MassFlow_dp_0.003_out_SamplingIncrease.csv")

# --- Berechnung ---
df_in["N_times_avg_vel"] = df_in["N"] * df_in["avg_vel"] * df_in["avg_Rhop"]
df_out["N_times_avg_vel"] = df_out["N"] * df_out["avg_vel"] * df_out["avg_Rhop"] 

# --- Startindizes definieren ---
start_in = 1
start_out = 120

# --- Ab Startzeile zuschneiden ---
df_in = df_in.iloc[start_in:].reset_index(drop=True)
df_out = df_out.iloc[start_out:].reset_index(drop=True)

# --- Plot ---
plt.figure(figsize=(10, 6))
plt.plot(df_in.index, df_in["N_times_avg_vel"], label="IN (ab Zeile 1)")
plt.plot(df_out.index, df_out["N_times_avg_vel"], label="OUT (ab Zeile 40)")
plt.xlabel("Index (neu beginnend bei 0)")
plt.ylabel("N * avg_vel")
plt.title("Vergleich IN / OUT (gleicher Startpunkt)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
