# Frontier-Math-Solver Skill Evaluation

**Skill**: `frontier-math-solver` (v6.0)  
**Date**: 2026-04-11  
**Evaluation Type**: Independent external audit following scientific methodology

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total tokens** | 11,349 (cl100k_base) |
| **Cost overhead vs simple solver** | +8,849 tokens (354% more) |
| **Problems in registry** | 15 |
| **Local tools available** | 6/6 |
| **External APIs accessible** | 0/5 |

**Verdict**: This skill MAXIMIZES rigor at the cost of context. It does NOT save tokens; it SPENDS tokens to buy disciplinary structure. The value proposition is methodological rigor, not efficiency.

---

## Detailed Findings

### 1. Token Budget Analysis

```
Total tokens (cl100k_base):     11,349
Total tokens (o200k_base):      11,336
Thinking phases (estimated):   2,143 (18.9%)
Output phases (estimated):  5,953 (52.5%)
```

The skill uses ~11k tokens every time it activates. This is **4.5× more** than a simple math solver (~2,500 tokens).

### 2. Problem Registry

The skill includes a registry of 15 FrontierMath problems:

| Difficulty | Count |
|-----------|-------|
| MODERATE | 3 |
| SOLID | 5 |
| MAJOR | 3 |
| BREAKTHROUGH | 4 |

| Domain | Count |
|--------|-------|
| Combinatorics | 6 |
| Number Theory | 6 |
| Algebraic Geometry | 1 |
| Topology/Geometry | 2 |

### 3. External API Verification

| API | URL | Status |
|-----|-----|-------|
| p2pclaw.com/silicon | /silicon | ❌ HTTP 403 |
| WolframAlpha | wolframalpha.com | ❌ Encoding error |
| PARI/GP | pari.math.u-bordeaux.fr | ❌ SSL cert |
| SageMath Cloud | sagecell.sagemath.org | ❌ HTTP 403 |
| GAP Online | gap-system.org | ❌ Encoding error |

**Finding**: None of the external mathematical services referenced in the skill are accessible from this environment.

### 4. Local Tools Verification

| Tool | Available | Version |
|------|-----------|---------|
| numpy | ✅ | 2.2.2 |
| scipy | ✅ | 1.15.1 |
| sympy | ✅ | 1.13.3 |
| z3 | ✅ | unknown |
| pandas | ✅ | 2.2.3 |
| networkx | ✅ | 3.4.2 |

**Finding**: All local Python tools requested by the skill are available.

### 5. Mathematical Verification

Code snippets are present for:
- Paley I construction (Hadamard matrices) - present but not executed
- Paley graph construction - present but not executed  
- Williamson matrix search - executed, verified for n=1

### 6. Methodological rigor

**FORBIDDEN ACTIONS** (9 defined):
1. Compute eigenvalues of 668×668 matrix mentally
2. State a bound without citation
3. Claim to solve Diophantine undecidable instance
4. Ignore the 20-minute audit
5. Implement own number-theoretic library when sympy/PARI exists
6. Hallucinate author names or theorem statements
7. Skip Phase 1 taxonomy
8. Submit VERIFIED status without proof
9. (additional items in code)

**CITATIONS**: 71 references verified in VERIFIED_REFS dict, including:
- Turyn_1974 (Hadamard matrices)
- Williamson_1944 (determinant theorem)
- Paley_1933 (orthogonal matrices)
- Huang_2019 (sensitivity conjecture)
- Faltings_1983 (finiteness theorems)

---

## Cost Comparison

| Solver Type | Tokens | Use Case |
|------------|--------|----------|
| Simple Math | 2,500 | Basic calculations |
| **This Skill** | **11,349** | **Frontier problems** |
| Overhead | +8,849 | +354% |

---

## Honest Conclusion

This skill is **NOT** designed to save tokens. It is designed to:

1. **Enforce rigor**: No computing mentally, all deterministic logic routed to verified tools
2. **Prevent hallucinations**: 71 verified citations, forbidden actions list
3. **Enable systematic attack**: 7-phase methodology with 20-minute epistemic audit
4. **Track progress**: Integration with p2pclaw.com/silicon (currently inaccessible)

**Where it adds value**:
- When attacking genuinely hard math problems (FrontierMath class)
- When methodological discipline matters more than speed
- When avoiding hallucinations is critical

**Where it fails**:
- For routine math problems (wastes ~9k tokens)
- When external APIs are down
- When context budget is limited

**What remains untested**:
- Actual problem-solving success rate
- Quality of solutions vs baseline
- 17-judge panel evaluation

---

## Files Produced

- `outputs/frontier_math_solver_evaluation.json` - Full metrics
- `outputs/frontier_math_solver_evaluation.md` - This summary