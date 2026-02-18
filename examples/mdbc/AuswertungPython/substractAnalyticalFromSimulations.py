#!/usr/bin/env python3
"""
Plot differences between Analytical and two Default lines.

- Parses semicolon-separated float strings
- Computes diff = Analytical - Default
- Plots both diffs over index
- Prints a few basic error metrics

Run:
  python3 plot_analytical_minus_default.py
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt


def parse_semicolon_floats(s: str) -> np.ndarray:
    s = s.strip().strip('"').strip()
    return np.array([float(x) for x in s.split(";")], dtype=float)


def metrics(diff: np.ndarray) -> dict:
    return {
        "max_abs": float(np.max(np.abs(diff))),
        "l2": float(np.sqrt(np.mean(diff**2))),
        "area_trapz_dx1": float(np.trapz(diff, dx=1.0)),
        "area_abs_trapz_dx1": float(np.trapz(np.abs(diff), dx=1.0)),
    }


def main() -> None:
    # --- Analytical (same for both) ---
    TEST_ANALYTICAL = (
        "8.1185641420633473e-28;3.1236694100044945e-04;5.9508594794524018e-04;"
        "8.4794974886972130e-04;1.0710674338095662e-03;1.2644390028009390e-03;"
        "1.4281190018783842e-03;1.5619874310747999e-03;1.6661097444181177e-03;"
        "1.7404859419315934e-03;1.7851269336324560e-03;1.7999999915315910e-03;"
        "1.7851269336324558e-03;1.7404859419315932e-03;1.6661097444181170e-03;"
        "1.5619874310747993e-03;1.4281190018783833e-03;1.2644390028009379e-03;"
        "1.0710674338095653e-03;8.4794974886972011e-04;5.9508594794523888e-04;"
        "3.1236694100044804e-04;8.1185641420633473e-28"
    )

    # --- Defaults ---
    DEFAULT_DRWTRUE = (
        "0;0.000272934;0.000562853;0.000821457;0.00104822;0.00124369;0.00140931;"
        "0.00154453;0.00164969;0.00172538;0.00177061;0.00178586;0.00177087;"
        "0.00172591;0.00165045;0.00154545;0.00141026;0.00124448;0.00104862;"
        "0.000821115;0.000561368;0.000271455;0"
    )

    DEFAULT_SMALLONEV2 = (
        "0;0.000267182;0.000558914;0.000820576;0.00105038;0.00124884;0.0014163;"
        "0.00155298;0.00165914;0.00173485;0.00178027;0.00179539;0.00178026;"
        "0.00173487;0.00165913;0.001553;0.00141624;0.00124869;0.00105019;"
        "0.000820237;0.000558751;0.000267715;0"
    )

    analytical = parse_semicolon_floats(TEST_ANALYTICAL)
    d1 = parse_semicolon_floats(DEFAULT_DRWTRUE)
    d2 = parse_semicolon_floats(DEFAULT_SMALLONEV2)

    if not (len(analytical) == len(d1) == len(d2)):
        raise ValueError(
            f"Length mismatch: analytical={len(analytical)}, d1={len(d1)}, d2={len(d2)}"
        )

    diff1 = analytical - d1
    diff2 = analytical - d2
    x = np.arange(len(analytical), dtype=float)

    # --- Plot ---
    plt.figure()
    plt.plot(x, diff1, label="smallOneonV2setDRWTrue")
    plt.plot(x, diff2, label="smallOneV2")
    plt.xlabel("Index")
    plt.ylabel("Analytical - Default")
    plt.title("Difference Comparison")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --- Print metrics ---
    print("Metrics (dx=1 integration over index):")
    print("smallOneonV2setDRWTrue:", metrics(diff1))
    print("smallOneV2:", metrics(diff2))


if __name__ == "__main__":
    main()
