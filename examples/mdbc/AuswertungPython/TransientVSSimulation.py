import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------
# Dateien
# --------------------------------------------------------
SPH_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv"

# Falls du die Version mit Transient+Steady hast, ggf. diesen Pfad nehmen:
# ANA_FILE = "/nishome/PaulS/Programms/.../_PointsVelocity_Vel.z_clean_3D_AnalyticalTransientAndSteady.csv"
ANA_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_0_25.csv"

PART_ID = 25  # gewünschter "Part" (wie in deinem Vergleichsscript)


# --------------------------------------------------------
# 1) SPH-Datei einlesen: PosX-Linie + Vel.z-Profil für PART_ID
# --------------------------------------------------------

# Roh-Header laden, um die X-Positionen zu bekommen
raw = pd.read_csv(SPH_FILE, sep=";", header=None)

# In deinen Files sieht Zeile 0 ungefähr so aus:
# ;PosX [m]:;0.0085;0.00875;0.009;...
# => X-Koordinaten stehen ab Spalte 2
posx = raw.iloc[0, 2:].astype(float).values

# Ab Zeile 3 stehen die eigentlichen Daten (mit Spaltennamen)
data = pd.read_csv(SPH_FILE, sep=";", skiprows=3)

print("Spalten in SPH-Daten:", data.columns)

# Versuch, die 'Part'-Spalte robust zu finden
part_col_candidates = [c for c in data.columns if c.strip().lower() == "part"]
if not part_col_candidates:
    raise ValueError("Keine 'Part'-Spalte in SPH-Datei gefunden. Bitte columns checken.")
part_col = part_col_candidates[0]

row = data.loc[data[part_col] == PART_ID]
if row.empty:
    raise ValueError(f"Part {PART_ID} nicht in SPH-Datei gefunden.")

# Alle Vel.z-Spalten (wie in deinem Vergleichsscript)
vel_cols = [c for c in data.columns if str(c).startswith("Vel.z_")]
if not vel_cols:
    raise ValueError("Keine 'Vel.z_*'-Spalten gefunden. Bitte Struktur prüfen.")

vel_sph = row.iloc[0][vel_cols].astype(float).values


# --------------------------------------------------------
# 2) Analytische Datei einlesen: transienten Zustand
# --------------------------------------------------------

# Auto-Separator, falls du mal Komma mal Semikolon hast
df_ana = pd.read_csv(ANA_FILE, sep=None, engine="python")
print("Spalten in analytischer Datei:", df_ana.columns)

# Versuche, passende Spalten zu finden
# - X- oder z-Koordinate
x_cols = [c for c in df_ana.columns if c.lower() in ("x", "z", "posx", "z_pos", "z_coord")]
if not x_cols:
    raise ValueError("Keine x/z-Spalte in analytischer Datei gefunden.")
x_col = x_cols[0]

# - transienter Anteil
vtrans_candidates = [c for c in df_ana.columns if "trans" in c.lower()]
if not vtrans_candidates:
    # fallback: falls die Datei nur 'v' hat
    vtrans_candidates = [c for c in df_ana.columns if c.lower().startswith("v")]
if not vtrans_candidates:
    raise ValueError("Keine Spalte für transienten Anteil in analytischer Datei gefunden.")
vtrans_col = vtrans_candidates[0]

x_ana = df_ana[x_col].values
v_trans = df_ana[vtrans_col].values


# --------------------------------------------------------
# 3) Plot: SPH Part 25 vs. analytisch transient
# --------------------------------------------------------

plt.figure(figsize=(10, 6))
plt.plot(posx, vel_sph, label=f"SPH: Part {PART_ID} (Vel.z über PosX)", linewidth=2)
plt.plot(x_ana, v_trans, "--", label="Analytisch transient", linewidth=2)

plt.xlabel("PosX [m]")
plt.ylabel("Velocity in z-Richtung [m/s]")
plt.title(f"Vergleich: SPH (Part {PART_ID}) vs. analytisch transient")
plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()
