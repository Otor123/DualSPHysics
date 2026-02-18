#!/usr/bin/env python3
"""
Symmetry check + plotting for a 1D profile.

- Reads values from a semicolon-separated line (default embedded below)
- Computes symmetry errors w.r.t. mirror around the center
- Plots:
    1) profile y[i]
    2) pairwise symmetry error |y_left - y_right|

python ./SymmetrieCheck.py \
  --csv-out symmetry_smallOneV2__setDRWTrue_full.csv \
  --csv-pairs-out symmetry_smallOneV2_setDRWTrue_pairs.csv


Requires: numpy, matplotlib
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import csv
from typing import Optional



## dp 0.0025
DEFAULT_LINE = (
"0;0;0.00012627;0.000221063;0.000313959;0.000395105;0.000463709;0.000520003;0.000563658;0.000594823;0.000613705;0.000620133;0.000613979;0.000595186;0.000564159;0.000520504;0.000464544;0.000396302;0.000315824;0.000223519;0.000127706;0;0"
)
res = 0.0025
#
## dp 0.005
#DEFAULT_LINE = (
#"0;0;0.000200325;0.000254839;0.000324977;0.000396055;0.000458922;0.000511261;0.000552209;0.000581602;0.000599217;0.000605088;0.000599234;0.000581536;0.000551921;0.000510742;0.000458324;0.000395644;0.000324538;0.000254432;0.000200835;0;0"
#)
#res = 0.005

### dp 0.01
#DEFAULT_LINE = (
#"0;0;0;0.000276697;0.00031113;0.000352233;0.000397604;0.000443197;0.000483661;0.00051444;0.000533103;0.000539208;0.000532473;0.000512709;0.000480427;0.000438958;0.000393733;0.0003505;0.000312905;0.000282492;0;0;0"
#)
#res = 0.01
#
#### dp 0.01
#DEFAULT_LINE = (
#"0;0;0;0.000486323;0.000520033;0.000560631;0.000606154;0.000652729;0.00069486;0.000727522;0.000747609;0.000754406;0.000747742;0.000728269;0.000696953;0.000656211;0.000610119;0.000563337;0.000519789;0.000482119;0.000452099;0;0"
#)
#res = 0.0123
#
#### 2D_check
#DEFAULT_LINE = (
#"0.180385;0.352753;0.507818;0.643815;0.758025;0.850971;0.922107;0.97489;1.00545;1.01472;1.00546;0.974901;0.922133;0.851035;0.758149;0.644054;0.507989;0.352903;0.181459"
#)
#res = "2D_check"

##### Wendeland
#DEFAULT_LINE = (
#"0;0;0;0.000513589;0.000547269;0.000587723;0.000632997;0.000679302;0.000721336;0.000754116;0.000774429;0.000781435;0.000774928;0.000755651;0.000724612;0.000684262;0.000638747;0.000593037;0.000551331;0.000516141;0.000488784;0;0"
#)
#res = "Wendeland_check"

TestAnalytical = (
"-1.3099872942236217e-04;-2.0440906830458376e-22;1.1847223335361116e-04;2.2442866323444421e-04;3.1788096789552863e-04;3.9884127419109917e-04;4.6732159287191696e-04;5.2333325416736691e-04;5.6688637173078066e-04;5.9798936172286905e-04;6.1664854112724872e-04;6.2286782546742308e-04;6.1664854112724872e-04;5.9798936172286905e-04;5.6688637173078066e-04;5.2333325416736691e-04;4.6732159287191696e-04;3.9884127419109917e-04;3.1788096789552863e-04;2.2442866323444421e-04;1.1847223335361116e-04;-2.0440906830458376e-22;-1.3099872942236217e-04"
)

### dp 0.0025
#DEFAULT_LINE = (
#"0.00012627;0.000221063;0.000313959;0.000395105;0.000463709;0.000520003;0.000563658;0.000594823;0.000613705;0.000620133;0.000613979;0.000595186;0.000564159;0.000520504;0.000464544;0.000396302;0.000315824;0.000223519;0.000127706"
#)
#res = 0.0025
#

#### dp 0.01
#DEFAULT_LINE = (
#"0;0.000276697;0.00031113;0.000352233;0.000397604;0.000443197;0.000483661;0.00051444;0.000533103;0.000539208;0.000532473;0.000512709;0.000480427;0.000438958;0.000393733;0.0003505;0.000312905;0.000282492;0"
#)
#res = 0.01

#TestAnalytical = (
#"1.1847223335361116e-04;2.2442866323444421e-04;3.1788096789552863e-04;3.9884127419109917e-04;4.6732159287191696e-04;5.2333325416736691e-04;5.6688637173078066e-04;5.9798936172286905e-04;6.1664854112724872e-04;6.2286782546742308e-04;6.1664854112724872e-04;5.9798936172286905e-04;5.6688637173078066e-04;5.2333325416736691e-04;4.6732159287191696e-04;3.9884127419109917e-04;3.1788096789552863e-04;2.2442866323444421e-04;1.1847223335361116e-04"
#)

## Test 5S big Zentral Check

TestAnalytical = ("-1.0554646198016004e-04;-2.0885859039237564e-20;9.0336066264112778e-05;1.6656493517197595e-04;2.2988958912949385e-04;2.8155519131973291e-04;3.2278949537620135e-04;3.5474466164928993e-04;3.7844353256148022e-04;3.9473287389577667e-04;4.0424545646214555e-04;4.0737224502575590e-04;4.0424545646214555e-04;3.9473287389577667e-04;3.7844353256148022e-04;3.5474466164928993e-04;3.2278949537620135e-04;2.8155519131973291e-04;2.2988958912949385e-04;1.6656493517197595e-04;9.0336066264112778e-05;-2.0885859039237564e-20;-1.0554646198016004e-04")

DEFAULT_LINE = (
"0;0;0.00012627;0.000221063;0.000313959;0.000395105;0.000463709;0.000520003;0.000563658;0.000594823;0.000613705;0.000620133;0.000613979;0.000595186;0.000564159;0.000520504;0.000464544;0.000396302;0.000315824;0.000223519;0.000127706;0;0"
)
res = 0.01


## small on

TestAnalytical = (
"-8.1185641420633473e-28;5.4999999812363725e-04;9.9999999615899894e-04;1.3499999943267611e-03;1.5999999928383213e-03;1.7499999918682916e-03;1.7999999915315910e-03;1.7499999918682914e-03;1.5999999928383206e-03;1.3499999943267611e-03;9.9999999615899785e-04;5.4999999812363584e-04;-8.1185641420633473e-28"
)

DEFAULT_LINE = ("0;0.000511985;0.000977287;0.00133642;0.00159175;0.00174453;0.00179539;0.00174455;0.00159177;0.00133634;0.000977067;0.000511888;0")


res = "smallOne"

## small onV2

TestAnalytical = (
"8.1185641420633473e-28;3.1236694100044945e-04;5.9508594794524018e-04;8.4794974886972130e-04;1.0710674338095662e-03;1.2644390028009390e-03;1.4281190018783842e-03;1.5619874310747999e-03;1.6661097444181177e-03;1.7404859419315934e-03;1.7851269336324560e-03;1.7999999915315910e-03;1.7851269336324558e-03;1.7404859419315932e-03;1.6661097444181170e-03;1.5619874310747993e-03;1.4281190018783833e-03;1.2644390028009379e-03;1.0710674338095653e-03;8.4794974886972011e-04;5.9508594794523888e-04;3.1236694100044804e-04;8.1185641420633473e-28"
)

DEFAULT_LINE = ("0;0.000267182;0.000558914;0.000820576;0.00105038;0.00124884;0.0014163;0.00155298;0.00165914;0.00173485;0.00178027;0.00179539;0.00178026;0.00173487;0.00165913;0.001553;0.00141624;0.00124869;0.00105019;0.000820237;0.000558751;0.000267715;0")


res = "smallOneV2"

## BIG ONE

TestAnalytical = (
"-6.4295267629495673e-23;1.0839293862066630e-04;2.0644867113644557e-04;2.9417425011650809e-04;3.7156867182822881e-04;4.3863820634446819e-04;4.9538266461879711e-04;5.4180709507901091e-04;5.7791169610371077e-04;6.0369989858286596e-04;6.1917193845242640e-04;6.2432934124037533e-04;6.1917193845242640e-04;6.0369989858286596e-04;5.7791169610371077e-04;5.4180709507901091e-04;4.9538266461879711e-04;4.3863820634446819e-04;3.7156867182822881e-04;2.9417425011650809e-04;2.0644867113644557e-04;1.0839293862066630e-04;-6.4295267629495673e-23"
)

DEFAULT_LINE = ("0;0.00012349;0.00020581;0.000290974;0.000367453;0.000434242;0.000491062;0.000537366;0.000573254;0.000598967;0.000614201;0.000619367;0.000614198;0.000598741;0.000572888;0.000536811;0.000490613;0.000434075;0.000367108;0.000289969;0.000202949;0.000116882;0")


res = "BigOneCSVExport"


## small onV2setDRWTrue

TestAnalytical = (
"8.1185641420633473e-28;3.1236694100044945e-04;5.9508594794524018e-04;8.4794974886972130e-04;1.0710674338095662e-03;1.2644390028009390e-03;1.4281190018783842e-03;1.5619874310747999e-03;1.6661097444181177e-03;1.7404859419315934e-03;1.7851269336324560e-03;1.7999999915315910e-03;1.7851269336324558e-03;1.7404859419315932e-03;1.6661097444181170e-03;1.5619874310747993e-03;1.4281190018783833e-03;1.2644390028009379e-03;1.0710674338095653e-03;8.4794974886972011e-04;5.9508594794523888e-04;3.1236694100044804e-04;8.1185641420633473e-28"
)

DEFAULT_LINE = ("0;0.000272934;0.000562853;0.000821457;0.00104822;0.00124369;0.00140931;0.00154453;0.00164969;0.00172538;0.00177061;0.00178586;0.00177087;0.00172591;0.00165045;0.00154545;0.00141026;0.00124448;0.00104862;0.000821115;0.000561368;0.000271455;0")


res = "smallOneonV2setDRWTrue"

## BIG onV2setDRWTrue

TestAnalytical = (
"-6.4295267629495673e-23;1.0839293862066630e-04;2.0644867113644557e-04;2.9417425011650809e-04;3.7156867182822881e-04;4.3863820634446819e-04;4.9538266461879711e-04;5.4180709507901091e-04;5.7791169610371077e-04;6.0369989858286596e-04;6.1917193845242640e-04;6.2432934124037533e-04;6.1917193845242640e-04;6.0369989858286596e-04;5.7791169610371077e-04;5.4180709507901091e-04;4.9538266461879711e-04;4.3863820634446819e-04;3.7156867182822881e-04;2.9417425011650809e-04;2.0644867113644557e-04;1.0839293862066630e-04;-6.4295267629495673e-23"
)

DEFAULT_LINE = ("0;0.000127878;0.000215911;0.000304126;0.00038171;0.00044844;0.000504702;0.000550343;0.000585766;0.000611104;0.000626177;0.000631241;0.000626375;0.000611387;0.000585971;0.000550489;0.000504904;0.000448823;0.000382522;0.0003056;0.000217893;0.000131162;0")


res = "BIGOneonV2setDRWTrue"

def parse_values_from_line(line: str, sep: str = ";") -> np.ndarray:
    parts = [p.strip() for p in line.strip().split(sep)]
    # allow empty parts (just skip)
    parts = [p for p in parts if p != ""]
    try:
        vals = np.array([float(p) for p in parts], dtype=float)
    except ValueError as e:
        raise ValueError(f"Failed to parse floats from line: {e}") from e
    return vals


def parse_values_from_file(path: Path, sep: str = ";") -> np.ndarray:
    txt = path.read_text(encoding="utf-8").strip()
    # if multiple lines, use the first non-empty one
    for line in txt.splitlines():
        if line.strip():
            return parse_values_from_line(line, sep=sep)
    raise ValueError(f"No non-empty line found in file: {path}")


def symmetry_metrics(y: np.ndarray, analytical: np.ndarray, eps: float = 1e-15):
    n = len(y)
    pairs = n // 2  # number of mirror pairs
    left = y[:pairs]
    right = y[::-1][:pairs]  # mirrored

    abs_err = left - right
    abs_err_mag = np.abs(abs_err)

    # relative error per pair (normalized by max(|left|, |right|))
    denom = np.maximum(np.maximum(np.abs(left), np.abs(right)), eps)
    rel_err = abs_err_mag / denom

    rel_err_pct = 100.0 * rel_err



    umax = max(np.max(np.abs(left)), np.max(np.abs(right)), eps)
    rel_err_pct_umax = 100.0 * abs_err_mag / umax

    #erroNew
    err = np.abs(y - analytical) / np.abs(analytical) * 100

    #err = np.where(err > 99.9, 0.0, err)


    print(err)


    max_abs = float(abs_err_mag.max()) if pairs > 0 else 0.0
    max_rel = float(rel_err.max()) if pairs > 0 else 0.0
    rms_abs = float(np.sqrt(np.mean(abs_err_mag**2))) if pairs > 0 else 0.0
    mean_abs = float(np.mean(abs_err_mag)) if pairs > 0 else 0.0

    # index of worst pair in left-side indexing
    worst_i = int(np.argmax(abs_err_mag)) if pairs > 0 else -1
    # corresponding indices in original array
    worst_left_idx = worst_i
    worst_right_idx = n - 1 - worst_i

    center_idx = n // 2  # for odd n, this is the center element; for even, right-of-center
    center_val = float(y[center_idx]) if n > 0 else float("nan")

    return {
        "n": n,
        "pairs": pairs,
        "center_idx": center_idx,
        "center_val": center_val,
        "max_abs": max_abs,
        "max_rel": max_rel,
        "rms_abs": rms_abs,
        "mean_abs": mean_abs,
        "worst_i": worst_i,
        "worst_left_idx": worst_left_idx,
        "worst_right_idx": worst_right_idx,
        "worst_left_val": float(y[worst_left_idx]) if worst_i >= 0 else float("nan"),
        "worst_right_val": float(y[worst_right_idx]) if worst_i >= 0 else float("nan"),
        "abs_err_mag": abs_err_mag,
        "rel_err": rel_err,
        "left": left,
        "right": right,
        "rel_err_pct": rel_err_pct,
        "rel_err_pct_umax": rel_err_pct_umax,
        "umax": float(umax),
        "errorAll" : err,

    }


def export_symmetry_csv(
    out_path: Path,
    y: np.ndarray,
    m: dict,
    analytical: Optional[np.ndarray] = None,
    sep: str = ";",
) -> None:
    """
    Exports a per-index table:
      i, y[i], analytical[i], mirror_j, y[mirror_j], |diff|, rel_sym[%], rel_sym_umax[%], err_vs_analytical[%]
    """
    n = len(y)
    pairs = m["pairs"]
    abs_err_mag = m["abs_err_mag"]
    rel_err_pct = m["rel_err_pct"]
    rel_err_pct_umax = m["rel_err_pct_umax"]
    error_all = m.get("errorAll", None)

    # If analytical provided but length differs, align to min length (avoid crash)
    if analytical is not None and len(analytical) != n:
        n_min = min(n, len(analytical))
        # truncate both consistently for export
        y = y[:n_min]
        n = n_min
        analytical = analytical[:n_min]

        # recompute mirror-dependent arrays safely (best effort)
        pairs = n // 2
        # re-slice the metric arrays if they exist
        abs_err_mag = abs_err_mag[:pairs]
        rel_err_pct = rel_err_pct[:pairs]
        rel_err_pct_umax = rel_err_pct_umax[:pairs]
        if error_all is not None:
            error_all = error_all[:n]

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=sep)

        w.writerow([
            "i",
            "y",
            "analytical",
            "mirror_j",
            "y_mirror",
            "abs_diff_mirror",
            "rel_sym_err_pct",
            "rel_sym_err_pct_umax",
            "err_vs_analytical_pct",
        ])

        for i in range(n):
            j = n - 1 - i
            y_i = float(y[i])
            y_j = float(y[j])

            # symmetry pair metrics only defined for left half pairs (i < pairs)
            if i < pairs:
                abs_diff = float(abs_err_mag[i])
                rel_sym = float(rel_err_pct[i])
                rel_sym_umax = float(rel_err_pct_umax[i])
            else:
                abs_diff = ""
                rel_sym = ""
                rel_sym_umax = ""

            a_i = ""
            err_a = ""
            if analytical is not None:
                a_i = float(analytical[i])
                if error_all is not None and i < len(error_all):
                    err_a = float(error_all[i])

            w.writerow([i, y_i, a_i, j, y_j, abs_diff, rel_sym, rel_sym_umax, err_a])


def export_pairwise_csv(out_path: Path, m: dict, sep: str = ";") -> None:
    """
    Exports a per-pair table:
      pair_i, left_idx, right_idx, left_val, right_val, abs_diff, rel_sym[%], rel_sym_umax[%]
    """
    pairs = m["pairs"]
    n = m["n"]
    left = m["left"]
    right = m["right"]
    abs_err_mag = m["abs_err_mag"]
    rel_err_pct = m["rel_err_pct"]
    rel_err_pct_umax = m["rel_err_pct_umax"]

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=sep)
        w.writerow([
            "pair_i",
            "left_idx",
            "right_idx",
            "left_val",
            "right_val",
            "abs_diff",
            "rel_sym_err_pct",
            "rel_sym_err_pct_umax",
        ])
        for i in range(pairs):
            li = i
            ri = n - 1 - i
            w.writerow([
                i,
                li,
                ri,
                float(left[i]),
                float(right[i]),
                float(abs_err_mag[i]),
                float(rel_err_pct[i]),
                float(rel_err_pct_umax[i]),
            ])

def export_pairwise_csv(out_path: Path, m: dict, sep: str = ";") -> None:
    """
    Exports a per-pair table:
      pair_i, left_idx, right_idx, left_val, right_val, abs_diff, rel_sym[%], rel_sym_umax[%]
    """
    pairs = m["pairs"]
    n = m["n"]
    left = m["left"]
    right = m["right"]
    abs_err_mag = m["abs_err_mag"]
    rel_err_pct = m["rel_err_pct"]
    rel_err_pct_umax = m["rel_err_pct_umax"]

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=sep)
        w.writerow([
            "pair_i",
            "left_idx",
            "right_idx",
            "left_val",
            "right_val",
            "abs_diff",
            "rel_sym_err_pct",
            "rel_sym_err_pct_umax",
        ])
        for i in range(pairs):
            li = i
            ri = n - 1 - i
            w.writerow([
                i,
                li,
                ri,
                float(left[i]),
                float(right[i]),
                float(abs_err_mag[i]),
                float(rel_err_pct[i]),
                float(rel_err_pct_umax[i]),
            ])

def main():
    ap = argparse.ArgumentParser(description="Check symmetry of a semicolon-separated 1D profile and plot it.")
    ap.add_argument("--file", type=str, default="", help="Path to text/CSV file containing one semicolon-separated line.")
    ap.add_argument("--sep", type=str, default=";", help="Separator (default ';').")
    ap.add_argument("--show", action="store_true", help="Show plot window instead of saving.")
    ap.add_argument("--out", type=str, default=f"symmetry {res}_.png", help="Output image filename when not using --show.")
    ap.add_argument("--csv-out", type=str, default="", help="Export a per-index CSV table to this path.")
    ap.add_argument("--csv-pairs-out", type=str, default="", help="Export a per-pair CSV table to this path.")
    args = ap.parse_args()



    analytical = None
    if args.file:
        y = parse_values_from_file(Path(args.file), sep=args.sep)
        src = f"file: {args.file}"
    else:
        y = parse_values_from_line(DEFAULT_LINE, sep=args.sep)
        analytical = parse_values_from_line(TestAnalytical, sep=args.sep)
        src = "embedded DEFAULT_LINE"

    m = symmetry_metrics(y, analytical)           

    if args.csv_out:
        export_symmetry_csv(Path(args.csv_out), y=y, m=m, analytical=analytical, sep=args.sep)
        print(f"CSV exported: {args.csv_out}")

    if args.csv_pairs_out:
        export_pairwise_csv(Path(args.csv_pairs_out), m=m, sep=args.sep)
        print(f"Pairwise CSV exported: {args.csv_pairs_out}")        



    print(f"Source: {src}")
    print(f"n = {m['n']}  | pairs = {m['pairs']}")
    print(f"center_idx = {m['center_idx']}  | center_val = {m['center_val']:.9g}")
    print(f"max |L-R|  = {m['max_abs']:.6e}")
    print(f"RMS |L-R|  = {m['rms_abs']:.6e}")
    print(f"mean|L-R|  = {m['mean_abs']:.6e}")
    print(f"max rel err= {m['max_rel']:.6e}")
    if m["worst_i"] >= 0:
        print(
            "worst pair: "
            f"idx {m['worst_left_idx']} (val {m['worst_left_val']:.9g})  <->  "
            f"idx {m['worst_right_idx']} (val {m['worst_right_val']:.9g})"
        )
    print(f"max rel err= {m['max_rel']:.6e}")



    # --- plotting ---
    x = np.arange(len(y))

    fig1 = plt.figure()
    plt.plot(x, y, marker="o", color="black")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Profile (values over index)")
    plt.grid(True)


    # Pairwise symmetry error
    pairs = m["pairs"]
    if pairs > 0:
        fig2 = plt.figure()
        pair_x = np.arange(pairs)  # pair index from left side
        plt.plot(pair_x, m["abs_err_mag"], marker="o", color="black")
        plt.xlabel("Pair index (left side i)")
        plt.ylabel("|y[i] - y[n-1-i]|")
        plt.title(f"Symmetry error per mirrored pair - dp = {res}")
        plt.grid(True)

    if pairs > 0:
        fig3 = plt.figure()
        pair_x = np.arange(pairs)
        plt.plot(pair_x, m["rel_err_pct"], marker="o", color="black")
        plt.xlabel("Pair index (left side i)")
        plt.ylabel("Relative error [%]")
        plt.title(f"Relative symmetry error per mirrored pair - dp = {res}")
        plt.grid(True)      

    if pairs > 0:
        fig4= plt.figure()
        pair_x = np.arange(pairs)
        plt.xlabel("Pair index (left side i)")
        plt.title(f"Relative symmetry error per mirrored pair - dp = {res}")
        plt.plot(pair_x, m["rel_err_pct_umax"], marker="o", color="black")
        plt.ylabel("Relative error vs umax [%]")
        plt.grid(True)   

    if pairs > 0:
        fig5= plt.figure()
        plt.xlabel("Pair index (left side i)")
        plt.title(f"error not mirrored - dp = {res}")
        plt.plot(m["errorAll"], marker="o", color="black")
        plt.ylabel("error [%]")
        plt.grid(True)                     

    if args.show:
        plt.show()
    else:
        # save both figures into one file? simplest: save first, then second with suffix
        out1 = Path(args.out)
        fig1.savefig(out1, dpi=200, bbox_inches="tight")
        if pairs > 0:
            out2 = out1.with_name(out1.stem + "_error_FINAL" + out1.suffix)
            fig2.savefig(out2, dpi=200, bbox_inches="tight")
            print(f"Saved: {out1} and {out2}")
            out3 = out1.with_name(out1.stem + "_rel_error_pct_FINAL" + out1.suffix)
            fig3.savefig(out3, dpi=200, bbox_inches="tight")
            print(f"Saved: {out3}")
            out4 = out1.with_name(out1.stem + "_rel_error_pct_umax_FINAL" + out1.suffix)
            fig4.savefig(out4, dpi=200, bbox_inches="tight")
            print(f"Saved: {out4}")        
            out5 = out1.with_name(out1.stem + "_ErrorAll_FINAL" + out1.suffix)
            fig5.savefig(out5, dpi=200, bbox_inches="tight")
            print(f"Saved: {out5}")                 
        else:
            print(f"Saved: {out1}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
