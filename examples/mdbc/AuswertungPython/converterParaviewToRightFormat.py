#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract only the columns 'Temp' and 'Points:0' from a CSV file
and write them to a new CSV.

Usage:
  python converterParaviewToRightFormat.py lowlowlowlow.csv dp_0.0000125.csv
  python converterParaviewToRightFormat.py lowlowlow.csv dp_0.000025.csv
  python converterParaviewToRightFormat.py lowlow.csv dp_0.00005.csv
  python converterParaviewToRightFormat.py low.csv dp_0.0001.csv
"""

import sys
import pandas as pd
from pathlib import Path

def main(input_csv: str, output_csv: str):
    input_csv = Path(input_csv)
    output_csv = Path(output_csv)

    # Read CSV (auto-detect separator)
    df = pd.read_csv(input_csv, sep=None, engine="python")

    # Check required columns
    required_cols = ["Temp", "Points:0"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    # Keep only desired columns
    out_df = df[required_cols]

    # Write CSV
    out_df.to_csv(output_csv, index=False)

    print(f"Written: {output_csv}")
    print(f"Columns: {list(out_df.columns)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_temp_points0.py input.csv output.csv")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
