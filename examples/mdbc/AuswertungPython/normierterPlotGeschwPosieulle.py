import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# --------------------------------------------------------
# Liste an CSV-Dateien
# --------------------------------------------------------
CSV_FILES = [
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.005/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Programms/DualSPHysicsbeta/DualSPHysics_v6.0_BETA/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
]

#3D Pipe big - changed db
CSV_FILES = [
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.008/measuretool/_PointsVelocity_Vel.z.csv",    
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.004_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_4_FreeCadPosieulleBigExample/Posiuelle/Posiuelle_out_dp_0.002/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_0_25.csv",
]

CSV_FILES = [
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
    #"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.01/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_0_25.csv",
]

CSV_FILES = [
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesRe<</_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesRe<</AnalyticalTransientProfile_t_All.csv",
]

CSV_FILES = [
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesDpsmallMeasurementRe<</_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesDpsmallMeasurementRe<</AnalyticalTransientProfile_t_All.csv",
]

CSV_FILES = [
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesRe</_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesRe</AnalyticalTransientProfile_t_All.csv",
]

CSV_FILES = [
   "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesNewmeasurmentRe</_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesNewMeasurmentRe</AnalyticalTransientProfile_t_All.csv"
]

CSV_FILES = [
  #  "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesDpsmallMeasurementRe<</_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesDpsmallMeasurementRe<</AnalyticalTransientProfile_t_All.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/setDRWMode/smallPipe_FreeCAD/_PointsVelocity_Vel.z.csv"
]

CSV_FILES = [
   # "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.0025/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.0025/measuretool/_PointsVelocity_Vel.z.csv",
   "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.0025/measuretool_newDP/_PointsVelocity_Vel.z.csv",
   # "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesNewMeasurmentRe</AnalyticalTransientProfile_t_All.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesDpsmallMeasurementRe<</AnalyticalTransientProfile_t_All.csv",


]
#
#CSV_FILES = [
#    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesDpsmallMeasurementRe<</_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesDpsmallMeasurementRe<</AnalyticalTransientProfile_t_All.csv",
#]
#

CSV_FILES = [
   # "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.0025/measuretool/_PointsVelocity_Vel.z.csv",
       "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesNewMeasurmentRe</AnalyticalTransientProfile_t_All.csv",
       "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.0025/measuretoolnewDP/_PointsVelocity_Vel.z.csv",
   # "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/Analytical_t_0_25/Analytical/AnalyticalTransientProfile_t_50sekundeFinalRe<.csv",

]

# --------------------------------------------------------
# Part IDs
# --------------------------------------------------------
PARTS = [10, 20, 25, 30, 300]  # z.B. [12, 25, 50, 100 ,150, 500]
PARTS = [10,25,50,100,200,250,300]
# --------------------------------------------------------
# Helper: dp aus Pfad extrahieren
# --------------------------------------------------------
def extract_dp(path):
    m = re.search(r"dp[_=]([0-9.]+)", path)
    return m.group(1) if m else "analytical"


# --------------------------------------------------------
# Farben pro dp vorbereiten (stabil, pro dp gleich)
# --------------------------------------------------------
dp_list = sorted({extract_dp(f) for f in CSV_FILES})
colors = plt.cm.viridis(np.linspace(0, 1, len(dp_list)))
dp_color = dict(zip(dp_list, colors))

# --------------------------------------------------------
# Eine gemeinsame Figure
# --------------------------------------------------------

plt.figure(figsize=(12, 7))
plt.title("Normalized profile: $u_z/u_{max}$ über $x/D$ — Comparison of analytical and numerical solution")

for CSV_FILE in CSV_FILES:
    dp = extract_dp(CSV_FILE)
    color = dp_color[dp]
    is_analytical = ("Analytical" in CSV_FILE) or ("clean_3D_Analytical" in CSV_FILE)

    # --- Header lesen (PosX sitzt in Zeile 0 ab Spalte 2) ---
    raw = pd.read_csv(CSV_FILE, sep=";", header=None)
    x_values = raw.iloc[0, 2:].astype(float).values

    # --- x Normierung auf [-1,1] über Radius ---
    R = 0.5 * (x_values.max() - x_values.min())
    if R == 0:
        raise ValueError(f"R ist 0 (x_values constant) in Datei: {CSV_FILE}")
    x_center = 0.5 * (x_values.max() + x_values.min())
    x_norm = (x_values - x_center) / R  # -> [-1,1]

    # --- Daten ab Zeile 4 lesen ---
    data = pd.read_csv(CSV_FILE, sep=";", skiprows=3)

    # Velocity columns unterschiedlich je Datei? -> robust einsammeln
    vel_cols = [c for c in data.columns if str(c).startswith("Vel.z_")]
    if len(vel_cols) == 0:
        raise ValueError(f"Keine Vel.z_ Spalten gefunden in: {CSV_FILE}")

    # Label aus Ordnername
    file_label = CSV_FILE.split("/")[-3]

    # --- Referenzgeschwindigkeit Uref (pro Datei) ---
    # Für Simulation: Maximum über ausgewählte Parts
    # Für Analytical: Maximum über die erste vorhandene Zeile (oder ebenfalls über PARTS, falls vorhanden)
    Uref = 0.0
    if "Part" in data.columns:
        # wenn Part existiert: wie bisher über PARTS
        for part_id in PARTS:
            row = data.loc[data["Part"] == part_id]
            if not row.empty:
                vel_values = row.iloc[0][vel_cols].values.astype(float)
                Uref = max(Uref, np.max(vel_values))
    else:
        # falls Analytical keine Part-Spalte hat: nimm max aus erster Zeile
        vel_values0 = data.iloc[0][vel_cols].values.astype(float)
        Uref = float(np.max(vel_values0))

    if Uref == 0:
        print(f"⚠️ Uref=0 in {CSV_FILE} -> übersprungen")
        continue

    # --------------------------------------------------------
    # Plot pro Part (Simulation) oder einmal (Analytical)
    # --------------------------------------------------------
    if "Part" in data.columns:
        parts_to_plot = PARTS
    else:
        parts_to_plot = [None]  # einmal plotten

    for part_id in parts_to_plot:
        if part_id is not None:
            row = data.loc[data["Part"] == part_id]
            if row.empty:
                print(f"⚠️ Part {part_id} nicht gefunden in {CSV_FILE}")
                continue
            row0 = row.iloc[0]
        else:
            row0 = data.iloc[0]

        vel_values = row0[vel_cols].values.astype(float)
        vel_norm = vel_values / Uref  # gemeinsame Normierung pro Datei

        # Zeit bestimmen
        if "Time [s]" in data.columns and part_id is not None:
            time = float(row0["Time [s]"])
        elif part_id is not None:
            time = part_id * 0.01
        else:
            time = None

        # --- Style: Analytical = Linie, Simulation = Punkte ---
        if is_analytical:
            linestyle = "None"
            marker = "o"
            linewidth = 1.0
            zorder = 5
            color = "black"
            label = f"SPH (dp={dp}, t={time:.3f}s)" if time is not None else f"SPH (dp={dp})"            
        else:
            linestyle = "-"
            marker = None
            linewidth = 2.8
            zorder = 3
            color = "red"
            label = f"Analytical (dp={dp})"

        plt.plot(
            x_norm,
            vel_norm,
            linestyle=linestyle,
            marker=marker,
            markersize=5,
            linewidth=linewidth,
            color=color,
            label=label,
            zorder=zorder
        )

# --------------------------------------------------------
# Styling + Legend dedup
# --------------------------------------------------------
plt.xlabel(r"$x/R$")
plt.ylabel(r"$u_z/u_{ref}$")
plt.grid(True)

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), fontsize=10)

plt.tight_layout()
plt.savefig("test.png", dpi=200)
plt.show()
