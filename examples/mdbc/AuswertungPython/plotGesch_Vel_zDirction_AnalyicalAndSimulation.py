#!/usr/bin/env python3
"""
Plot Vel.z (or any velocity column) of a specific Part ID
against X-position for multiple DualSPHysics MeasureTool CSV files.

Works with CSV structure:
 - Row 0: PosX
 - Row 1: PosY
 - Row 2: PosZ
 - Row 3+: Time-dependent values (Part rows)
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# --------------------------------------------------------
# USER SETTINGS
# --------------------------------------------------------

CSV_FILES = [
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Analytical/_PointsVelocity_Vel.z_clean.csv",
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Poisuelle_mDBC_out_dp_0.001_activated_aoutofill_and_advanced_Draw_mode/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Poisuelle_mDBC_out_dp_0.001_activated_aoutofill_and_advanced_Draw_mode_coefh_0.95/measuretool/_PointsVelocity_Vel.z.csv",
]

PART_ID = 500          # <-- choose your particle
VEL_COLUMN = "Vel.z"   # can also be "Vel.x" or "Vel.y"
SEP = ";"              # your CSV uses semicolon


# --------------------------------------------------------
# FUNCTION TO LOAD ONE CSV
# --------------------------------------------------------

def load_measuretool_csv(csv_path):
    """Loads MeasureTool CSV and returns:
        x_values: numpy array of X coordinates
        df: dataframe with velocity/time rows (with header)
    """
    raw = pd.read_csv(csv_path, sep=SEP, header=None)

    # row 0 = PosX
    x_values = raw.iloc[0, 2:].astype(float).values

    # clean data rows starting from row 3
    df = pd.read_csv(csv_path, sep=SEP, skiprows=3)

    return x_values, df


# --------------------------------------------------------
# PLOT FOR MULTIPLE FILES
# --------------------------------------------------------

plt.figure(figsize=(10, 5))

for csv in CSV_FILES:
    print(f"Loading: {csv}")

    x_values, df = load_measuretool_csv(csv)

    if "Part" not in df.columns:
        raise KeyError(f"'Part' column not found in: {csv}")

    # Filter the row of the selected particle
    row = df.loc[df["Part"] == PART_ID]

    if row.empty:
        print(f"⚠ Part {PART_ID} not found in {csv}, skipping.")
        continue

    # extract velocity array (columns from index 2 onward)
    vel = row.iloc[0, 2:].values.astype(float)

    # label based on folder name or file name
    label = os.path.basename(os.path.dirname(csv))

    plt.plot(x_values, vel, label=label)

# --------------------------------------------------------
# FINAL PLOT STYLING
# --------------------------------------------------------

plt.title(f"Velocity ({VEL_COLUMN}) over X for Part {PART_ID}")
plt.xlabel("X position [m]")
plt.ylabel(f"{VEL_COLUMN} [m/s]")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
