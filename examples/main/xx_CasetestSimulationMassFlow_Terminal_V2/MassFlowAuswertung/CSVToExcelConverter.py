import pandas as pd
import glob
import os

# --- Ordner mit CSVs ---
FOLDER = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/main/xx_CasetestSimulationMassFlow_Terminal_V2/MassFlowAuswertung/plot"

# Alle CSVs suchen
csv_files = sorted(glob.glob(os.path.join(FOLDER, "MassFlow_*.csv")))

# Ziel-Excel-Datei
excel_path = os.path.join(FOLDER, "MassFlow_Auswertung.xlsx")

# ExcelWriter öffnen
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    for f in csv_files:
        # Dateiname ohne Endung = Tabellenname
        sheetname = os.path.basename(f).replace(".csv", "")
        
        # CSV lesen
        df = pd.read_csv(f)
        
        # In Excel schreiben
        df.to_excel(writer, index=False, sheet_name=sheetname)

print(f"✅ Alle {len(csv_files)} CSV-Dateien wurden in '{excel_path}' gespeichert.")
