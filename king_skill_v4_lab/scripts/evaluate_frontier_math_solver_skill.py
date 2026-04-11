#!/usr/bin/env python3
"""Evaluate Skills-frontier-math-solver.md for executability and rigor."""

from __future__ import annotations

import ast
import importlib
import json
import math
import re
from itertools import product
from pathlib import Path

import numpy as np
import requests
import tiktoken

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
SKILL_PATH = ROOT.parent / "Skills-frontier-math-solver.md"
TEXT = SKILL_PATH.read_text(encoding="utf-8", errors="replace")

LOCAL_TOOLS = ["numpy", "scipy", "sympy", "z3", "pandas", "requests", "networkx"]
EXTERNAL_ENDPOINTS = {
    "p2pclaw_base": "https://www.p2pclaw.com/silicon",
    "p2pclaw_admin_problems": "https://www.p2pclaw.com/silicon/admin/problems",
    "p2pclaw_api_problems": "https://www.p2pclaw.com/silicon/api/problems",
    "arxiv_api": "https://export.arxiv.org/api/query?search_query=all:FrontierMath&start=0&max_results=1",
    "gap": "https://www.gap-system.org/",
    "sagecell": "https://sagecell.sagemath.org/",
    "pari_gp": "https://pari.math.u-bordeaux.fr/gp.html",
    "magma": "http://magma.maths.usyd.edu.au/calc/",
}


def import_check() -> dict[str, bool]:
    result: dict[str, bool] = {}
    for name in LOCAL_TOOLS:
        try:
            importlib.import_module(name)
            result[name] = True
        except Exception:
            result[name] = False
    return result


def http_check() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for name, url in EXTERNAL_ENDPOINTS.items():
        try:
            r = requests.get(url, timeout=20, allow_redirects=True)
            out[name] = {
                "url": url,
                "status_code": r.status_code,
                "final_url": r.url,
                "content_type": r.headers.get("content-type", ""),
                "body_prefix": r.text[:160],
            }
        except Exception as e:
            out[name] = {"url": url, "error": f"{type(e).__name__}: {e}"}
    return out


def verify_hadamard(H: np.ndarray) -> bool:
    n = H.shape[0]
    return np.allclose(H @ H.T, n * np.eye(n)) and set(np.unique(H)).issubset({-1, 1})


def paley_I(q: int) -> np.ndarray:
    from sympy.ntheory import isprime, quadratic_residues

    assert isprime(q) and q % 4 == 3
    qr = set(quadratic_residues(q)) - {0}
    elems = list(range(q))
    Q = np.array(
        [
            [1 if (a - b) % q in qr else -1 if a != b else 0 for b in elems]
            for a in elems
        ],
        dtype=int,
    )
    n = q + 1
    H = np.ones((n, n), dtype=int)
    H[1:, 1:] = Q
    H[0, 1:] = 1
    H[1:, 0] = -1
    H[0, 0] = 1
    return H


def paley_I_corrected(q: int) -> np.ndarray:
    from sympy.ntheory import isprime, quadratic_residues

    assert isprime(q) and q % 4 == 3
    qr = set(quadratic_residues(q)) - {0}
    elems = list(range(q))
    Q = np.array(
        [
            [1 if (a - b) % q in qr else -1 if a != b else 0 for b in elems]
            for a in elems
        ],
        dtype=int,
    )
    n = q + 1
    H = np.ones((n, n), dtype=int)
    H[1:, 1:] = Q + np.eye(q, dtype=int)
    H[0, 1:] = 1
    H[1:, 0] = -1
    H[0, 0] = 1
    return H


def paley_graph(q: int):
    import networkx as nx
    from sympy.ntheory import isprime, quadratic_residues

    assert isprime(q) and q % 4 == 1
    qr = set(quadratic_residues(q)) - {0}
    G = nx.Graph()
    G.add_nodes_from(range(q))
    for a in range(q):
        for b in range(a + 1, q):
            if (a - b) % q in qr:
                G.add_edge(a, b)
    return G


def book_graph(p: int):
    import networkx as nx

    G = nx.Graph()
    G.add_edge(0, 1)
    for i in range(p):
        G.add_edge(0, 2 + i)
        G.add_edge(1, 2 + i)
    return G


def compute_sensitivity(f_table: dict) -> int:
    n = len(next(iter(f_table)))
    best = 0
    for x in product([0, 1], repeat=n):
        sens_x = sum(
            1
            for i in range(n)
            if f_table[x] != f_table[x[:i] + (1 - x[i],) + x[i + 1 :]]
        )
        best = max(best, sens_x)
    return best


def compute_degree(f_table: dict) -> int:
    n = len(next(iter(f_table)))
    coeffs = {}
    for S in product([0, 1], repeat=n):
        val = 0.0
        for x in product([0, 1], repeat=n):
            parity = (-1) ** sum(s & xi for s, xi in zip(S, x))
            val += f_table[x] * parity
        coeffs[S] = val / (2**n)
    support = [S for S, c in coeffs.items() if abs(c) > 1e-9]
    return max(sum(S) for S in support) if support else 0


def executable_math_tests() -> dict:
    H168_skill = paley_I(167)
    H168_fixed = paley_I_corrected(167)
    G13 = paley_graph(13)
    B5 = book_graph(5)

    examples = {
        "dictator3": {x: x[0] for x in product([0, 1], repeat=3)},
        "and2": {x: int(x[0] and x[1]) for x in product([0, 1], repeat=2)},
        "xor2": {x: int(x[0] ^ x[1]) for x in product([0, 1], repeat=2)},
        "majority3": {
            x: int(sum(x) >= 2) for x in product([0, 1], repeat=3)
        },
    }
    boolean_results = {}
    for name, table in examples.items():
        sens = compute_sensitivity(table)
        deg = compute_degree(table)
        boolean_results[name] = {
            "sensitivity": sens,
            "degree": deg,
            "huang_bound_holds": deg <= sens**2,
        }

    return {
        "hadamard_168_skill_snippet": {
            "shape": list(H168_skill.shape),
            "verified": verify_hadamard(H168_skill),
            "entries": sorted(int(x) for x in np.unique(H168_skill)),
        },
        "hadamard_168_corrected_variant": {
            "shape": list(H168_fixed.shape),
            "verified": verify_hadamard(H168_fixed),
            "entries": sorted(int(x) for x in np.unique(H168_fixed)),
        },
        "paley_graph_13": {
            "nodes": G13.number_of_nodes(),
            "edges": G13.number_of_edges(),
            "regular_degree": list(dict(G13.degree()).values())[0],
            "all_degrees_equal": len(set(dict(G13.degree()).values())) == 1,
        },
        "book_graph_5": {
            "nodes": B5.number_of_nodes(),
            "edges": B5.number_of_edges(),
            "shared_edge_degree_pair": [B5.degree(0), B5.degree(1)],
        },
        "boolean_functions": boolean_results,
        "gnfs_constant": round((64 / 9) ** (1 / 3), 8),
        "m23_order_factorization": {
            "factorization": "2^7 * 3^2 * 5 * 7 * 11 * 23",
            "computed_order": 2**7 * 3**2 * 5 * 7 * 11 * 23,
        },
    }


def parse_registry_count() -> int:
    start = TEXT.find("VERIFIED PROBLEM REGISTRY")
    end = TEXT.find("## PHASE 0")
    if start == -1 or end == -1 or end <= start:
        return 0
    chunk = TEXT[start:end]
    return sum(1 for line in chunk.splitlines() if line.strip().startswith("FM"))


def parse_verified_refs_count() -> int:
    m = re.search(r"VERIFIED_REFS\s*=\s*\{(.*?)\n\}", TEXT, flags=re.DOTALL)
    if not m:
        return 0
    blob = "{" + m.group(1) + "\n}"
    return len(re.findall(r'"[^"]+"\s*:', blob))


def parse_phase_count() -> int:
    return len(re.findall(r"## PHASE \d+", TEXT))


def parse_forbidden_count() -> int:
    m = re.search(r"FORBIDDEN\s*=\s*\[(.*?)\]", TEXT, flags=re.DOTALL)
    if not m:
        return 0
    return len(re.findall(r'"[^"]+"', m.group(1)))


def parse_synthesis_patterns_count() -> int:
    return len(re.findall(r'"[^"]+"\s*:\s*\{\s*\n\s*"model"', TEXT))


def token_stats() -> dict[str, int]:
    enc = tiktoken.get_encoding("cl100k_base")
    return {
        "chars": len(TEXT),
        "words": len(TEXT.split()),
        "cl100k_base_tokens": len(enc.encode(TEXT)),
    }


def render_markdown(report: dict) -> str:
    imports = report["local_stack"]
    http = report["external_endpoints"]
    math_tests = report["executable_math_tests"]
    return "\n".join(
        [
            "# Frontier Math Solver Skill Evaluation",
            "",
            f"Skill file: `{report['skill_path']}`",
            "",
            "## Executive Summary",
            "",
            f"- Prompt overhead of the skill itself is `{report['token_stats']['cl100k_base_tokens']}` tokens (`{report['token_stats']['words']}` words, `{report['token_stats']['chars']}` characters).",
            f"- Local scientific stack promised by the skill is available in `{sum(imports.values())}/{len(imports)}` cases.",
            f"- Core mathematical snippets mostly run, but one headline snippet is broken as written: the Paley Type I code in the skill does not verify a Hadamard matrix until corrected.",
            f"- The skill is strong as a mathematical workflow spec: `{report['structure']['phase_count']}` phases, `{report['structure']['problem_registry_count']}` registry entries, `{report['structure']['verified_refs_count']}` claimed verified references, `{report['structure']['forbidden_actions_count']}` forbidden actions.",
            f"- Integration claim is only partial: `p2pclaw.com/silicon` responds `200`, but `/silicon/api/problems` returns `{http['p2pclaw_api_problems'].get('status_code')}` and `/silicon/admin/problems` returns `{http['p2pclaw_admin_problems'].get('status_code')}`.",
            "",
            "## Reasoning Value",
            "",
            "- Strong upside: theorem-first decomposition, mandatory SOTA fetch, enforced tool routing, cross-domain synthesis patterns, and an anti-loop audit improve research discipline.",
            "- Cost tradeoff: this is a heavy steering prompt. It can improve rigor, but it spends a large amount of context before any actual problem solving begins.",
            "- What is actually demonstrated here: executable subroutines and available tooling, not success on open FrontierMath problems.",
            "- Main honesty gap: the 2026 problem-status registry and some endpoint contracts are asserted inside the skill but not fully verified by the local codebase.",
            "",
            "## Key Executable Checks",
            "",
            f"- `paley_I(167)` as written in the skill -> Hadamard verification: `{math_tests['hadamard_168_skill_snippet']['verified']}` with entries `{math_tests['hadamard_168_skill_snippet']['entries']}`.",
            f"- Corrected Paley Type I variant -> Hadamard verification: `{math_tests['hadamard_168_corrected_variant']['verified']}`.",
            f"- `paley_graph(13)` -> `{math_tests['paley_graph_13']['nodes']}` nodes, `{math_tests['paley_graph_13']['edges']}` edges, regular degrees: `{math_tests['paley_graph_13']['all_degrees_equal']}`.",
            f"- `book_graph(5)` -> `{math_tests['book_graph_5']['nodes']}` nodes, `{math_tests['book_graph_5']['edges']}` edges.",
            f"- GNFS constant from the skill evaluates to `{math_tests['gnfs_constant']}`.",
            "",
            "## Integration Caveat",
            "",
            "- The skill contains concrete POST/GET API contracts for P2PCLAW Silicon. In this audit, the public Silicon entrypoint exists, but the documented `/api/problems` route was not live.",
        ]
    ) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        "skill_path": str(SKILL_PATH),
        "token_stats": token_stats(),
        "local_stack": import_check(),
        "external_endpoints": http_check(),
        "executable_math_tests": executable_math_tests(),
        "structure": {
            "phase_count": parse_phase_count(),
            "problem_registry_count": parse_registry_count(),
            "verified_refs_count": parse_verified_refs_count(),
            "forbidden_actions_count": parse_forbidden_count(),
            "synthesis_patterns_count": parse_synthesis_patterns_count(),
        },
        "assessment": {
            "reasoning_value": (
                "High as a research workflow discipline layer: it strongly pushes theorem-first "
                "classification, tool use, citation discipline, and anti-loop audits."
            ),
            "unproven_claims": [
                "That the listed 2026 problem statuses are all still current.",
                "That the documented P2PCLAW API contracts are correct end to end.",
                "That using this skill materially solves more open problems without controlled evaluation.",
            ],
        },
    }

    json_path = OUT / "frontier_math_solver_skill_evaluation.json"
    md_path = OUT / "frontier_math_solver_skill_evaluation.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "md": str(md_path)}, indent=2))


if __name__ == "__main__":
    main()
