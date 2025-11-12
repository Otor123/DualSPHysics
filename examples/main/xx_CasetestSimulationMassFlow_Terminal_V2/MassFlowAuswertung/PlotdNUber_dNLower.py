#!/usr/bin/env python3
"""
Überprüft, ob dN_upper und dN_lower gleich sind.
Wenn nicht, gibt es den Step und die Differenz ΔN aus.
Wenn alle gleich sind, wird ΔN über step geplottet.
"""

import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# EINSTELLUNGEN
# ----------------------------------------------------------
CSV_FILE = "MassFlow_FromParticles_V2.csv"
DELIMITER = ";"  # dein CSV nutzt Semikolon

TimeOut = 0.001;

# ----------------------------------------------------------
# LADEN
# ----------------------------------------------------------
df = pd.read_csv(CSV_FILE, delimiter=DELIMITER)

# Differenz berechnen
df["dN_diff"] = df["dN_upper"] + df["dN_lower"]

df["time"] = df["step"]*TimeOut

# Ungleichheiten finden
diff_rows = df[df["dN_diff"] != 0]

if not diff_rows.empty:
    print("❗ Unterschiede gefunden:")
    for _, row in diff_rows.iterrows():
        print(f"Step {int(row['step'])}: dN = {row['dN_diff']:.3f}  "
              f"(upper={row['dN_upper']:.3f}, lower={row['dN_lower']:.3f})")
else:
    print("✅ Alle Werte sind gleich. Erstelle Plot...")


#plt.figure(figsize=(10, 5))
#plt.plot(df["step"], df["dN_diff"], label="ΔN = dN_upper - dN_lower", lw=1.5)
#plt.xlabel("Step")
#plt.ylabel("ΔN (Partikel)")
#plt.title("Differenz dN_upper - dN_lower über Step")
#plt.grid(True)
#plt.legend()
#plt.tight_layout()
#plt.show()
#
#plt.figure(figsize=(10, 5))
#plt.plot(df["step"], df["N_total"], label="ΔN = dN_upper - dN_lower", lw=1.5)
#plt.xlabel("Step")
#plt.ylabel("ΔN (Partikel)")
#plt.title("Differenz dN_upper - dN_lower über Step")
#plt.grid(True)
#plt.legend()
#plt.tight_layout()
#plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))

# --- Linke Achse (ΔN_diff)
ax1.plot(df["time"], df["dN_diff"], color="tab:blue", label="ΔN = dN_upper + dN_lower", lw=1.5)

# --- Nur Linien für Werte >= 1
mask = df["dN_diff"] <= -1     # oder np.abs(df["dN_diff"]) >= 1 für beides

ax1.vlines(
    x=df.loc[mask, "time"],
    ymin=0,
    ymax=-15,
    color="tab:blue",
    alpha=0.3,
    linestyle="--",
    lw=0.8
)

ax1.set_xlabel("Time")
ax1.set_ylabel("ΔN (Partikel)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

# --- Zweite Achse (N_total)
ax2 = ax1.twinx()
ax2.plot(df["time"], df["N_total"], color="tab:orange", label="N_total", lw=1.5, linestyle="--")
ax2.set_ylabel("N_total (Partikel)", color="tab:orange")
ax2.tick_params(axis="y", labelcolor="tab:orange")

# --- Titel & Legende
fig.suptitle("Vergleich: ΔN und N_total über Time")
ax1.grid(True, which="both", alpha=0.3)

# Legenden kombinieren
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right")

fig.tight_layout()
plt.show()
