"""
Reference keyword router mirroring King-Skill DISPATCH_ORDER (king-skill/SKILL.md).
Used for EXP-02/08/09 reproducible routing metrics — not an LLM substitute.
Order: most specific patterns first.
"""

from __future__ import annotations

import re
from typing import Optional

# Canonical IDs aligned with king-skill/SKILL.md DISPATCH_ORDER
FALLBACK = "fallback"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def route_task(user_input: str) -> str:
    t = _norm(user_input)

    def has(*words: str) -> bool:
        return all(w in t for w in words)

    def anyw(*words: str) -> bool:
        return any(w in t for w in words)

    # skill-15 p2pclaw — require infra cues (avoid "P2PCLAW" in generic compression prompts)
    if (
        ("p2pclaw" in t and anyw("lab", "api", "gateway", "harness", "spawner"))
        or anyw("hive queen", "gun.js", "gunjs", "openclaw gateway")
        or ("relay" in t and "node" in t)
    ):
        return "skill-15-p2pclaw-lab"

    # P2P graph analysis (DISPATCH_TABLE p2p_topology → networkx)
    if "p2p" in t and anyw("topology", "overlay", "betweenness", "pagerank", "shortest path"):
        return "skill-08-networkx"

    # skill-20 report
    if anyw("generate the full paper", "publication-ready", "report generator", "write the entire paper"):
        return "skill-20-report-generator"

    # skill-11 latex
    if anyw("latex", "pdflatex", "tikz", "bibtex"):
        return "skill-11-latex-renderer"

    # skill-09 sympy BEFORE skill-01 — integrals / symbolic
    if "∫" in user_input or "integral" in t or "symbolic" in t or "closed form" in t:
        if "numerically" in t or "numpy" in t or "finite difference" in t:
            return "skill-01-python-executor"
        return "skill-09-sympy"

    # skill-07 scipy simulation / ODE — before generic "scipy" → python executor
    if anyw(
        "simulate",
        "simulation",
        "odeint",
        "solve_ivp",
        "lorenz",
        "runge-kutta",
        "differential equation",
        "sir model",
    ):
        if "closed form" in t or "symbolic" in t:
            return "skill-09-sympy"
        return "skill-07-scipy-sim"

    # skill-01 python numerical
    if anyw("numpy", "scipy", "eigenvalue", "fft", "matrix multiply", "float64"):
        return "skill-01-python-executor"

    # skill-02 SAT
    if anyw("sat solver", "cnf", "boolean satisfiability", "cadical", "z3 python-sat"):
        return "skill-02-sat-solver"

    # skill-03 arxiv
    if anyw("arxiv", "arxiv.org"):
        return "skill-03-arxiv-fetch"

    # skill-04 oeis / constants
    if anyw("oeis", "integer sequence", "fibonacci", "euler totient", "nist codata"):
        return "skill-04-oeis-nist"

    # skill-05 lean
    if anyw("lean 4", "lean4", "#check", "theorem prover lean"):
        return "skill-05-lean4-verify"

    # skill-06 pandoc / docs
    if anyw("pandoc", "docx", "markdown to pdf", "weasyprint"):
        return "skill-06-doc-transform"

    # skill-08 networkx
    if anyw("networkx", "betweenness", "pagerank", "graph diameter", "shortest path graph"):
        return "skill-08-networkx"

    # skill-10 translate code
    if anyw("translate this rust", "convert java to python", "port c++ to"):
        return "skill-10-code-translator"

    # skill-12 data pipeline
    if anyw("pandas", "polars", "etl", "csv to parquet"):
        return "skill-12-data-pipeline"

    # skill-13 wolfram
    if anyw("wolfram", "wolframalpha"):
        return "skill-13-wolfram-query"

    # skill-14 git
    if anyw("git rebase", "git bisect", "cherry-pick"):
        return "skill-14-git-operations"

    # skill-17 benchmark
    if anyw("benchmark suite", "performance regression", "microbenchmark"):
        return "skill-17-benchmark-verifier"

    # skill-18 parallel
    if anyw("multiprocessing", "parallel search", "brute force parallel"):
        return "skill-18-parallel-search"

    # skill-19 cache
    if anyw("knowledge cache", "cached json lookup", "memoize tool result"):
        return "skill-19-knowledge-cache"

    # skill-16 token compression only
    if has("compress", "notation") or ("token" in t and "compress" in t):
        return "skill-16-token-compression"

    return FALLBACK
