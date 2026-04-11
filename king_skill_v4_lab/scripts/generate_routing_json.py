#!/usr/bin/env python3
"""EXP-02 / EXP-08 — emit routing task JSON files (reproducible, version-controlled)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

# 19 canonical tasks (v1 disclosure) — ground truth aligned with keyword_router reference.
TASKS_V1: list[dict] = [
    {"id": "T001", "input": "Call the P2PCLAW lab API to list active agents on the gateway host.", "expected_skill": "skill-15-p2pclaw-lab", "notes": "p2pclaw-specific", "difficulty": "easy"},
    {"id": "T002", "input": "Generate the full paper in publication-ready Markdown with figures.", "expected_skill": "skill-20-report-generator", "notes": "", "difficulty": "easy"},
    {"id": "T003", "input": "Render this LaTeX table with booktabs and compile to PDF.", "expected_skill": "skill-11-latex-renderer", "notes": "", "difficulty": "easy"},
    {"id": "T004", "input": "Simplify the integral ∫ x^3 e^x dx symbolically and give a closed form.", "expected_skill": "skill-09-sympy", "notes": "boundary: integral vs numerical", "difficulty": "boundary"},
    {"id": "T005", "input": "Compute eigenvalues of a 500x500 random matrix in float64 with NumPy.", "expected_skill": "skill-01-python-executor", "notes": "", "difficulty": "easy"},
    {"id": "T006", "input": "Encode graph 3-coloring as CNF and run a SAT solver (CaDiCaL).", "expected_skill": "skill-02-sat-solver", "notes": "graph vs SAT: SAT wording wins", "difficulty": "boundary"},
    {"id": "T007", "input": "Fetch arXiv:2401.00001 abstract and BibTeX via arxiv.org API.", "expected_skill": "skill-03-arxiv-fetch", "notes": "", "difficulty": "easy"},
    {"id": "T008", "input": "Look up Fibonacci numbers n=1..20 in OEIS and cite A000045.", "expected_skill": "skill-04-oeis-nist", "notes": "", "difficulty": "easy"},
    {"id": "T009", "input": "Verify this Lean 4 snippet compiles: def f := 2 + 2", "expected_skill": "skill-05-lean4-verify", "notes": "", "difficulty": "easy"},
    {"id": "T010", "input": "Convert README.md to DOCX using pandoc templates.", "expected_skill": "skill-06-doc-transform", "notes": "", "difficulty": "easy"},
    {"id": "T011", "input": "Simulate Lorenz ODE with scipy solve_ivp for t=0..30.", "expected_skill": "skill-07-scipy-sim", "notes": "simulate → scipy", "difficulty": "medium"},
    {"id": "T012", "input": "Compute PageRank on a 1k-node NetworkX DiGraph from edge list.", "expected_skill": "skill-08-networkx", "notes": "", "difficulty": "easy"},
    {"id": "T013", "input": "Translate this Rust function to idiomatic Python.", "expected_skill": "skill-10-code-translator", "notes": "", "difficulty": "easy"},
    {"id": "T014", "input": "Build an ETL: read CSV, clean nulls, write Parquet with Polars.", "expected_skill": "skill-12-data-pipeline", "notes": "", "difficulty": "easy"},
    {"id": "T015", "input": "Query WolframAlpha for roots of z^5 + 1 in the complex plane.", "expected_skill": "skill-13-wolfram-query", "notes": "", "difficulty": "easy"},
    {"id": "T016", "input": "Explain how to recover from a bad git rebase interactively.", "expected_skill": "skill-14-git-operations", "notes": "", "difficulty": "easy"},
    {"id": "T017", "input": "Run the microbenchmark suite and flag performance regression >5%.", "expected_skill": "skill-17-benchmark-verifier", "notes": "", "difficulty": "easy"},
    {"id": "T018", "input": "Parallel search over seeds 0..10^6 using multiprocessing Pool.", "expected_skill": "skill-18-parallel-search", "notes": "", "difficulty": "easy"},
    {"id": "T019", "input": "Lookup a prior tool result from the knowledge cache JSON store.", "expected_skill": "skill-19-knowledge-cache", "notes": "v1 set ends here (19 disclosed)", "difficulty": "easy"},
]

# Extended: + skill-16 + 5 ambiguous + 5 fallback + duplicates per skill to reach 70
EXTRA: list[dict] = [
    {"id": "T020", "input": "Compress scientific notation in this paragraph to minimize tokens.", "expected_skill": "skill-16-token-compression", "notes": "token-compression path", "difficulty": "easy"},
    {"id": "T021", "input": "simplify the integral ∫x²dx symbolically", "expected_skill": "skill-09-sympy", "notes": "guide boundary wording", "difficulty": "boundary"},
    {"id": "T022", "input": "Simulate a damped harmonic oscillator numerically with scipy ODE.", "expected_skill": "skill-07-scipy-sim", "notes": "simulate + scipy", "difficulty": "boundary"},
    {"id": "T023", "input": "Prove Fermat's Last Theorem in one page.", "expected_skill": "fallback", "notes": "provable overreach → fallback", "difficulty": "fallback"},
    {"id": "T024", "input": "Graph the social network metrics but only as prose essay.", "expected_skill": "fallback", "notes": "ambiguous: no tool keywords", "difficulty": "ambiguous"},
    {"id": "T025", "input": "Graph coloring encoded as CNF clauses for n=50 graph.", "expected_skill": "skill-02-sat-solver", "notes": "SAT dominates graph word", "difficulty": "boundary"},
    {"id": "T026", "input": "Compute FFT of a 2^20 signal using NumPy vectorized.", "expected_skill": "skill-01-python-executor", "notes": "", "difficulty": "easy"},
    {"id": "T027", "input": "Gun.js relay node health check for decentralized sync.", "expected_skill": "skill-15-p2pclaw-lab", "notes": "", "difficulty": "medium"},
    {"id": "T028", "input": "P2P overlay shortest path experiment with NetworkX.", "expected_skill": "skill-08-networkx", "notes": "p2p topology routing", "difficulty": "boundary"},
    {"id": "T029", "input": "Hive queen spawner logs show crash — diagnose OpenCLAW gateway.", "expected_skill": "skill-15-p2pclaw-lab", "notes": "", "difficulty": "medium"},
    {"id": "T030", "input": "What is the meaning of life?", "expected_skill": "fallback", "notes": "no skill", "difficulty": "fallback"},
]

# Per-skill filler to reach 70 (3 per skill × 20 = 60 from v1+extra we need more)
# We attach 40 more systematic tasks: 2 per skill for skills 01..20 not already tripled
SKILL_SEEDS: dict[str, tuple[str, ...]] = {
    "skill-01-python-executor": ("NumPy batched matmul timing float32", "SciPy sparse eigen solver ARPACK"),
    "skill-02-sat-solver": ("SAT solver on random 3-SAT CNF 200 vars", "Z3 python-sat cardinality constraints"),
    "skill-03-arxiv-fetch": ("Download metadata for arXiv:2309.00012", "arxiv.org search API for 'quantum error correction'"),
    "skill-04-oeis-nist": ("OEIS lookup for Catalan numbers", "NIST CODATA speed of light 2022"),
    "skill-05-lean4-verify": ("Typecheck this Lean 4 structure field", "Lean4 proof of commutativity of Nat.add"),
    "skill-06-doc-transform": ("pandoc md to pdf via weasyprint", "DOCX template merge with pandoc"),
    "skill-07-scipy-sim": ("solve_ivp stiff Robertson chemical kinetics", "ODE simulation of SIR model scipy"),
    "skill-08-networkx": ("NetworkX betweenness on Zachary karate", "graph diameter random geometric graph"),
    "skill-09-sympy": ("closed form of sum 1/k^2 sympy", "symbolic derivative of matrix expression"),
    "skill-10-code-translator": ("convert Java to Python asyncio", "translate this Rust enum to Python"),
    "skill-11-latex-renderer": ("pdflatex beamer slides compile", "Tikz diagram compile latex"),
    "skill-12-data-pipeline": ("pandas groupby aggregation pipeline", "polars lazy scan parquet"),
    "skill-13-wolfram-query": ("WolframAlpha integrate sin(x)/x", "wolfram query Lambert W"),
    "skill-14-git-operations": ("git bisect start binary search", "git cherry-pick onto main"),
    "skill-15-p2pclaw-lab": ("openclaw gateway pairing code", "p2pclaw lab integration harness"),
    "skill-16-token-compression": ("token compress equations in prose", "notation compress for P2PCLAW output"),
    "skill-17-benchmark-verifier": ("benchmark suite CI gate", "microbenchmark regression detector"),
    "skill-18-parallel-search": ("multiprocessing brute force keyspace", "parallel search over combinatorial seeds"),
    "skill-19-knowledge-cache": ("knowledge cache json lookup key", "memoize tool result in cache store"),
    "skill-20-report-generator": ("write the entire paper section Methods", "publication-ready figure captions generator"),
}


def build_extended_70() -> list[dict]:
    out: list[dict] = []
    out.extend(TASKS_V1)
    out.extend(EXTRA)
    nxt = 100
    # Ensure ≥3 tasks per skill (guide: 3×20 + boundaries + fallbacks ≈ 70)
    for skill, phrases in SKILL_SEEDS.items():
        need = 3 - sum(1 for x in out if x["expected_skill"] == skill)
        for j in range(max(0, need)):
            ph = phrases[j % len(phrases)]
            out.append(
                {
                    "id": f"T{nxt}",
                    "input": f"{ph} (coverage {j}).",
                    "expected_skill": skill,
                    "notes": "coverage to ≥3/skill",
                    "difficulty": "medium",
                },
            )
            nxt += 1
    out.sort(key=lambda x: x["id"])
    if len(out) > 70:
        return out[:70]
    while len(out) < 70:
        out.append(
            {
                "id": f"TX{len(out):03d}",
                "input": "Discuss epistemology of models without invoking tools.",
                "expected_skill": "fallback",
                "notes": "pad to 70",
                "difficulty": "fallback",
            },
        )
    return out


def build_500() -> list[dict]:
    """EXP-08: 25 variants × 20 skills = 500 stratified synthetic prompts (protocol-disclosed)."""
    rows: list[dict] = []
    i = 0
    for skill, phrases in SKILL_SEEDS.items():
        for k in range(25):
            base = phrases[k % len(phrases)]
            rows.append(
                {
                    "id": f"S{i:04d}",
                    "input": f"[v{k}] {base}: add technical detail for a controlled trial.",
                    "expected_skill": skill,
                    "notes": "synthetic stratified template",
                    "difficulty": ["easy", "medium", "hard", "boundary"][k % 4],
                }
            )
            i += 1
    return rows


def main() -> None:
    ext = build_extended_70()
    (DATA / "routing_tasks_v1.json").write_text(json.dumps(TASKS_V1, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "routing_tasks_v4_extended.json").write_text(json.dumps(ext, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    big = build_500()
    (DATA / "routing_tasks_v4_500.json").write_text(json.dumps(big, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Wrote", DATA / "routing_tasks_v1.json", len(TASKS_V1))
    print("Wrote", DATA / "routing_tasks_v4_extended.json", len(ext))
    print("Wrote", DATA / "routing_tasks_v4_500.json", len(big))


if __name__ == "__main__":
    main()
    sys.exit(0)
