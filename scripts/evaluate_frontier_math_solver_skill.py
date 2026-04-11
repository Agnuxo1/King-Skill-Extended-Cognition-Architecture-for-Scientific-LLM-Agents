"""
Evaluation script for Skills-frontier-math-solver.md
Following same methodology as token_compression_skill_evaluation.py
"""

import json
import sys
import os
import re
import tiktoken
from pathlib import Path

SKILL_PATH = Path(__file__).parent.parent / "Skills-frontier-math-solver.md"
OUTPUT_DIR = Path(__file__).parent / "outputs"


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    enc = tiktoken.get_encoding(model)
    return len(enc.encode(text))


def main():
    print("=" * 70)
    print("FRONTIER-MATH-SOLVER SKILL EVALUATION")
    print("=" * 70)

    if not SKILL_PATH.exists():
        print(f"ERROR: Skill file not found: {SKILL_PATH}")
        return 1

    content = SKILL_PATH.read_text(encoding="utf-8")

    results = {
        "skill_file": str(SKILL_PATH),
        "file_size_bytes": len(content.encode("utf-8")),
        "lines": len(content.splitlines()),
    }

    # TOKEN BUDGET ANALYSIS
    print("\n[1] TOKEN BUDGET ANALYSIS")
    print("-" * 40)

    token_counts = {
        "cl100k_base": count_tokens(content, "cl100k_base"),
        "o200k_base": count_tokens(content, "o200k_base"),
    }

    print(f"  Total tokens (cl100k_base): {token_counts['cl100k_base']:,}")
    print(f"  Total tokens (o200k_base):  {token_counts['o200k_base']:,}")

    # Estimate thinking vs output regions
    thinking_pattern = re.compile(r"## PHASE \d+:.*?(?=\n## |\Z)", re.DOTALL)
    phases = thinking_pattern.findall(content)

    thinking_tokens = sum(count_tokens(p, "cl100k_base") for p in phases[:4])
    output_tokens = sum(count_tokens(p, "cl100k_base") for p in phases[4:])

    results["token_budget"] = {
        "total_cl100k": token_counts["cl100k_base"],
        "thinking_phase_tokens": thinking_tokens,
        "output_phase_tokens": output_tokens,
        "ratio_thinking": thinking_tokens / max(1, token_counts["cl100k_base"]),
    }

    print(f"  Estimated thinking phases: {thinking_tokens:,} tokens")
    print(f"  Estimated output phases:  {output_tokens:,} tokens")
    print(f"  Thinking ratio: {results['token_budget']['ratio_thinking']:.1%}")

    # PROBLEM REGISTRY ANALYSIS
    print("\n[2] PROBLEM REGISTRY ANALYSIS")
    print("-" * 40)

    problem_pattern = re.compile(r"FM\d+ ([A-Z]+)\s+([^\t]+)\t+([^\t]+)\t+([A-Z_]+)")
    problems = problem_pattern.findall(content)

    domains = {}
    for p in problems:
        domain = p[1].strip()
        domains[domain] = domains.get(domain, 0) + 1

    print(f"  Total problems in registry: {len(problems)}")
    print(f"  By domain: {domains}")

    results["registry"] = {
        "total_problems": len(problems),
        "by_domain": domains,
    }

    # EXTERNAL API VERIFICATION
    print("\n[3] EXTERNAL API VERIFICATION")
    print("-" * 40)

    apis = {
        "p2pclaw.com/silicon": "https://p2pclaw.com/silicon",
        "WolframAlpha": "https://www.wolframalpha.com",
        "PARI_GP": "https://pari.math.u-bordeaux.fr/gp.html",
        "SageMath_cloud": "https://sagecell.sagemath.org/",
        "GAP_online": "https://www.gap-system.org/",
    }

    api_status = {}
    for name, url in apis.items():
        try:
            from urllib.request import urlopen
            from urllib.error import URLError

            req = urlopen(url, timeout=5)
            api_status[name] = {"status": req.getcode(), "accessible": True}
            print(f"  {name}: HTTP {req.getcode()} ✓")
        except Exception as e:
            api_status[name] = {"error": str(e), "accessible": False}
            print(f"  {name}: FAILED ({type(e).__name__})")

    results["external_apis"] = api_status

    # VERIFIED PYTHON TOOLS CHECK
    print("\n[4] VERIFIED PYTHON TOOLS (local)")
    print("-" * 40)

    tools_to_check = [
        ("numpy", "np"),
        ("scipy", "scipy"),
        ("sympy", "sympy"),
        ("z3", "z3"),
        ("pandas", "pd"),
        ("networkx", "nx"),
    ]

    tool_status = {}
    for module, alias in tools_to_check:
        try:
            __import__(module)
            tool_status[module] = {
                "available": True,
                "version": getattr(__import__(module), "__version__", "unknown"),
            }
            print(f"  {alias}: {tool_status[module]['version']}")
        except ImportError as e:
            tool_status[module] = {"available": False, "error": str(e)}
            print(f"  {alias}: NOT AVAILABLE")

    results["local_tools"] = tool_status

    # MATHEMATICAL VERIFICATION (code execution)
    print("\n[5] MATHEMATICAL VERIFICATION")
    print("-" * 40)

    math_tests = {}

    # Test 1: Hadamard verification (from skill code)
    try:
        import numpy as np
        from sympy.ntheory import isprime, quadratic_residues

        def verify_hadamard(H):
            n = H.shape[0]
            return np.allclose(H @ H.T, n * np.eye(n)) and set(H.flatten()).issubset(
                {-1, 1}
            )

        def paley_I(q):
            assert isprime(q) and q % 4 == 3
            QR = set(quadratic_residues(q)) - {0}
            elems = list(range(q))
            Q = np.array(
                [
                    [1 if (a - b) % q in QR else -1 if a != b else 0 for b in elems]
                    for a in elems
                ]
            )
            n = q + 1
            H = np.ones((n, n), dtype=int)
            H[1:, 1:] = Q
            H[0, 1:] = 1
            H[1:, 0] = -1
            H[0, 0] = 1
            return H

        # Test Paley I construction
        test_q = 167
        if test_q % 4 == 3 and isprime(test_q):
            H168 = paley_I(test_q)
            verified = verify_hadamard(H168)
            math_tests["paley_I_167"] = {
                "verified": verified,
                "n": 168,
                "expected": "H_168 exists by Paley I (1933)",
            }
            print(f"  paley_I(167): {'PASS ✓' if verified else 'FAIL ✗'}")
        else:
            print(f"  paley_I(167): SKIPPED (q conditions not met)")
    except Exception as e:
        math_tests["paley_I_167"] = {"error": str(e)}
        print(f"  paley_I(167): ERROR ({e})")

    # Test 2: Paley graph construction
    try:
        import networkx as nx
        from sympy.ntheory import isprime, quadratic_residues

        def paley_graph(q):
            assert isprime(q) and q % 4 == 1
            QR = set(quadratic_residues(q)) - {0}
            G = nx.Graph()
            G.add_nodes_from(range(q))
            for a in range(q):
                for b in range(a + 1, q):
                    if (a - b) % q in QR:
                        G.add_edge(a, b)
            return G

        test_q = 13  # 13 ≡ 1 mod 4, prime
        if test_q % 4 == 1 and isprime(test_q):
            P = paley_graph(test_q)
            is_regular = all(d == (test_q - 1) // 2 for _, d in P.degree())
            math_tests["paley_graph_13"] = {
                "verified": is_regular,
                "nodes": P.number_of_nodes(),
                "edges": P.number_of_edges(),
            }
            print(f"  paley_graph(13): {'PASS ✓' if is_regular else 'FAIL ✗'}")
    except Exception as e:
        math_tests["paley_graph_13"] = {"error": str(e)}
        print(f"  paley_graph(13): ERROR ({e})")

    # Test 3: Williamson matrix search (small scale)
    try:
        from itertools import product

        def circ(row):
            return np.array([np.roll(row, i) for i in range(len(row))])

        def search_williamson_small(n, max_iter=1000):
            rng = np.random.default_rng(42)
            for _ in range(max_iter):
                rows = [rng.choice([-1, 1], n) for _ in range(4)]
                A, B, C, D = [circ(r) for r in rows]
                if np.allclose(A @ A + B @ B + C @ C + D @ D, 4 * n * np.eye(n)):
                    return True
            return False

        # Test n=1 (trivial)
        found = search_williamson_small(1, max_iter=10)
        math_tests["williamson_n1"] = {
            "search_iterations": 10,
            "found": found,
        }
        print(f"  williamson_search(1): {'FOUND' if found else 'NOT FOUND'}")
    except Exception as e:
        math_tests["williamson_n1"] = {"error": str(e)}
        print(f"  williamson_search(1): ERROR ({e})")

    results["math_verification"] = math_tests

    # FORBIDDEN ACTIONS CHECK
    print("\n[6] FORBIDDEN ACTIONS VERIFICATION")
    print("-" * 40)

    forbidden_pattern = re.compile(
        r"FORBIDDEN\s*=\s*\[(.*?)\]", re.DOTALL | re.IGNORECASE
    )
    forbidden_match = forbidden_pattern.search(content)

    if forbidden_match:
        forbidden_list = [
            f.strip().strip('"').strip("'") for f in forbidden_match.group(1).split(",")
        ]
        results["forbidden_actions"] = {
            "count": len(forbidden_list),
            "examples": forbidden_list[:5],
        }
        print(f"  Defined forbidden actions: {len(forbidden_list)}")
        for f in forbidden_list[:3]:
            print(f"    - {f}")
    else:
        print("  No FORBIDDEN list found")
        results["forbidden_actions"] = {"count": 0}

    # CITATION VERIFICATION
    print("\n[7] CITATION VERIFICATION")
    print("-" * 40)

    verified_refs = re.findall(r'"([^"]+)":\s*"([^"]+)"', content)
    print(f"  VERIFIED_REFS entries: {len(verified_refs)}")

    results["citations"] = {
        "count": len(verified_refs),
        "samples": [r[0] for r in verified_refs[:5]],
    }

    # COST ANALYSIS (compared to baseline)
    print("\n[8] COST COMPARISON (vs baseline)")
    print("-" * 40)

    baseline_simple_math = 2500

    skill_cost = token_counts["cl100k_base"]

    results["cost_comparison"] = {
        "baseline_simple_math": baseline_simple_math,
        "skill_total": skill_cost,
        "cost_overhead": skill_cost - baseline_simple_math,
        "overhead_percentage": (skill_cost - baseline_simple_math)
        / baseline_simple_math,
    }

    print(f"  Baseline (simple): {baseline_simple_math:,} tokens")
    print(f"  Skill cost: {skill_cost:,} tokens")
    print(
        f"  Overhead: +{results['cost_comparison']['cost_overhead']:,} tokens ({results['cost_comparison']['overhead_percentage']:.1%} more)"
    )

    # SAVE RESULTS
    OUTPUT_DIR.mkdir(exist_ok=True)

    evaluation_results = {
        "skill": "frontier-math-solver",
        "version": "6.0",
        "evaluation_date": "2026-04-11",
        "metrics": results,
    }

    json_path = OUTPUT_DIR / "frontier_math_solver_evaluation.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(evaluation_results, f, indent=2, ensure_ascii=False)

    md_path = OUTPUT_DIR / "frontier_math_solver_evaluation.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Frontier-Math-Solver Skill Evaluation\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Total tokens**: {token_counts['cl100k_base']:,} (cl100k_base)\n")
        f.write(f"- **Problems in registry**: {len(problems)}\n")
        f.write(
            f"- **Local tools available**: {sum(1 for t in tool_status.values() if t.get('available'))}/{len(tool_status)}\n"
        )
        f.write(
            f"- **External APIs accessible**: {sum(1 for a in api_status.values() if a.get('accessible'))}/{len(api_status)}\n\n"
        )
        f.write("## Findings\n\n")
        f.write("### Token Budget\n\n")
        f.write(f"- Thinking phases: {thinking_tokens:,} tokens\n")
        f.write(f"- Output phases: {output_tokens:,} tokens\n")
        f.write(
            f"- Thinking ratio: {results['token_budget']['ratio_thinking']:.1%}\n\n"
        )
        f.write("### Cost Analysis\n\n")
        f.write(
            f"- This skill ADDS {results['cost_comparison']['cost_overhead']:,} tokens overhead vs baseline\n"
        )
        f.write(
            f"- Token cost: ${results['cost_comparison']['overhead_percentage']:.1%} more than a simple solver\n\n"
        )
        f.write("### Mathematical Verification\n\n")
        for test_name, test_result in math_tests.items():
            status = (
                "✓" if test_result.get("verified") or test_result.get("found") else "✗"
            )
            f.write(f"- {test_name}: {status}\n")
        f.write("\n### Honest Conclusion\n\n")
        f.write(
            "This skill MAXIMIZES rigor at the cost of context. It does NOT save tokens;\n"
        )
        f.write(
            "it SPENDS tokens to buy disciplinary structure. The value proposition is\n"
        )
        f.write("methodological rigor, not efficiency.\n")

    print(f"\n[OUTPUT] Results saved to:")
    print(f"  - {json_path}")
    print(f"  - {md_path}")

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print(f"Token cost: {skill_cost:,} tokens (cl100k_base)")
    print(
        f"Cost vs baseline: +{results['cost_comparison']['cost_overhead']:,} tokens ({results['cost_comparison']['overhead_percentage']:.1%})"
    )
    print("This skill SPENDS tokens for rigor, not savings.")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
