#!/usr/bin/env python3
"""EXP-10 — static registry of known keyword collisions for the reference router."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Documented overlaps (DISPATCH_ORDER resolution + ambiguous natural language)
CONFLICTS = [
    {
        "keywords": ["integral", "∫"],
        "skills": ["skill-09-sympy", "skill-01-python-executor"],
        "resolution": "If 'numerically' or 'numpy' or 'finite difference' → 01 else → 09",
    },
    {
        "keywords": ["simulate", "ode", "differential"],
        "skills": ["skill-07-scipy-sim", "skill-09-sympy", "skill-01-python-executor"],
        "resolution": "If closed-form/symbolic → 09; if scipy/solve_ivp/Lorenz → 07; numpy fft → 01",
    },
    {
        "keywords": ["graph", "coloring", "CNF", "SAT"],
        "skills": ["skill-02-sat-solver", "skill-08-networkx"],
        "resolution": "CNF/SAT wording → 02 before graph metrics → 08",
    },
    {
        "keywords": ["p2p", "topology", "p2pclaw"],
        "skills": ["skill-15-p2pclaw-lab", "skill-08-networkx"],
        "resolution": "p2pclaw/gun.js/openclaw gateway → 15; p2p overlay + PageRank/path → 08",
    },
    {
        "keywords": ["prove", "lean"],
        "skills": ["skill-05-lean4-verify", "fallback"],
        "resolution": "Lean4 explicit → 05; vague 'prove theorem' without Lean → fallback",
    },
]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    p = DATA / "routing_keyword_conflicts_v4.json"
    p.write_text(json.dumps(CONFLICTS, indent=2) + "\n", encoding="utf-8")
    print(p.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
