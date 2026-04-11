#!/usr/bin/env python3
"""
EXP-01 acceptance driver: dependency import checks + routing JSON validation +
reference-router accuracy (EXP-08/09) with Wilson 95% CI.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    phat = successes / n
    denom = 1 + z**2 / n
    centre = phat + z**2 / (2 * n)
    rad = z * math.sqrt((phat * (1 - phat) + z**2 / (4 * n)) / n)
    return ((centre - rad) / denom, (centre + rad) / denom)


def load_tasks(name: str) -> list[dict]:
    p = DATA / name
    if not p.is_file():
        raise FileNotFoundError(p)
    return json.loads(p.read_text(encoding="utf-8"))


def test_imports() -> None:
    import numpy  # noqa: F401
    import scipy  # noqa: F401
    import sympy  # noqa: F401
    import pandas  # noqa: F401
    import polars  # noqa: F401
    import z3  # noqa: F401
    import feedparser  # noqa: F401
    import requests  # noqa: F401
    import joblib  # noqa: F401
    import matplotlib  # noqa: F401
    import pdfminer  # noqa: F401
    import tiktoken  # noqa: F401


def eval_routing(path: Path) -> dict:
    from keyword_router import route_task

    tasks = json.loads(path.read_text(encoding="utf-8"))
    ok = 0
    matrix: dict[tuple[str, str], int] = {}
    for t in tasks:
        exp = t["expected_skill"]
        pred = route_task(t["input"])
        if pred == exp:
            ok += 1
        matrix[(exp, pred)] = matrix.get((exp, pred), 0) + 1
    n = len(tasks)
    lo, hi = wilson_ci(ok, n)
    return {
        "file": str(path.name),
        "n": n,
        "correct": ok,
        "accuracy": ok / n,
        "wilson95": [lo, hi],
        "confusion_pairs_nonzero": sum(1 for v in matrix.values() if v),
    }


def main() -> int:
    gen = ROOT / "scripts" / "generate_routing_json.py"
    subprocess.run([sys.executable, str(gen)], check=True, cwd=str(ROOT))

    v1 = DATA / "routing_tasks_v1.json"
    assert len(load_tasks(v1.name)) == 19, "v1 must have 19 tasks"
    ext = DATA / "routing_tasks_v4_extended.json"
    big = DATA / "routing_tasks_v4_500.json"
    assert len(load_tasks(ext.name)) == 70
    assert len(load_tasks(big.name)) == 500

    if os.environ.get("SKIP_HEAVY_DEPS") == "1":
        print("SKIP_HEAVY_DEPS=1 — skipping optional pinned imports (use Docker for full EXP-01).")
    else:
        test_imports()
    r70 = eval_routing(ext)
    r500 = eval_routing(big)
    report = {
        "routing_extended_70": r70,
        "routing_500": r500,
        "note": "Accuracy is for keyword_router reference implementation vs disclosed labels.",
        "methodology_warning": (
            "The 500-task stratified file is self-consistent with this router by construction (EXP-08). "
            "For the v4 paper, replace labels after Carbon review and measure the production LLM router separately."
        ),
    }
    outp = ROOT / "outputs" / "run_all_tests_report.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if r70["accuracy"] < 0.85:
        print("WARN: extended set accuracy < 0.85 — tune router or labels.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
