#!/usr/bin/env python3
"""Bootstrap mean/SD/95% CI for savings_pct from compression_corpus_v4.csv (EXP-04)."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
CSV_PATH = OUT / "compression_corpus_v4.csv"


def bootstrap_ci(values: np.ndarray, n_boot: int = 10_000, seed: int = 42) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    if len(values) == 0:
        return float("nan"), float("nan")
    means = np.empty(n_boot)
    for b in range(n_boot):
        sample = rng.choice(values, size=len(values), replace=True)
        means[b] = sample.mean()
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def main() -> None:
    if not CSV_PATH.is_file():
        print("No", CSV_PATH, file=sys.stderr)
        sys.exit(1)
    vals = []
    by_domain: dict[str, list[float]] = {}
    with CSV_PATH.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            v = float(row["savings_pct"])
            vals.append(v)
            by_domain.setdefault(row["domain"], []).append(v)
    arr = np.array(vals)
    lo, hi = bootstrap_ci(arr)
    report = {
        "n": len(arr),
        "mean": float(arr.mean()),
        "std": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
        "median": float(np.median(arr)),
        "ci95_bootstrap": [lo, hi],
        "by_domain": {
            d: {"n": len(vs), "mean": float(np.mean(vs)), "std": float(np.std(vs, ddof=1)) if len(vs) > 1 else 0.0}
            for d, vs in sorted(by_domain.items())
        },
    }
    p = OUT / "compression_stats_v4.json"
    p.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(p.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
