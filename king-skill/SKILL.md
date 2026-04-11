---
name: king-skill
description: >
  MASTER ROUTER — activates FIRST on every non-trivial task. Analyzes the problem,
  determines if a specialized tool/skill can resolve it without spending reasoning
  tokens, and orchestrates execution. Also enforces token-compression on ALL output.
  Trigger: ANY task involving computation, simulation, literature, verification,
  data, graphs, code, documents, or scientific analysis. No exceptions.
  The LLM is the orchestrator, not the executor.
priority: 0
version: 2.0
integrates: token-compression (always active)
---

# King-Skill — Master Cognitive Orchestrator

## Core principle

```python
paradigm = {
    "old": "task → LLM reasons → output          # tokens ∝ complexity",
    "new": "task → LLM routes → tool → LLM synth # tokens ∝ novelty only",
}
# Extended cognition (Clark & Chalmers 1998):
# the tool IS part of the cognitive system, not external to it
```

## ALWAYS ACTIVE: token-compression

```python
# token-compression applies to ALL output regardless of routing decision
# thinking budget: free CoT in English+math+code (do NOT compress)
# output budget: maximum compression via math/code/symbols
# See: token-compression SKILL.md for full arsenal
```

---

## Dispatch algorithm

```python
def king_dispatch(task: Task) -> Response:

    # Step 1: classify (< 30 tokens)
    category = classify(task)
    # COMPUTE | SIMULATE | VERIFY | RETRIEVE | TRANSFORM | GRAPH | REASON

    # Step 2: lookup skill
    skill = DISPATCH_TABLE.get(category)

    if skill is None:
        # No tool exists → reason directly + apply token-compression
        return reason_compressed(task)

    # Step 3: delegated execution
    try:
        result = execute_skill(skill, task)
        return synthesize_compressed(result, task.context)  # minimal tokens
    except ToolError as e:
        return fallback(task, e)

def should_delegate(task) -> bool:
    return (
        task.is_deterministic() and    # same input → same output
        task.has_known_tool() and      # skill exists in registry
        not task.needs_judgment()      # no genuine reasoning required
    )
# DELEGATE examples: FFT, eigenvalues, SAT solving, PDF parse, arXiv fetch
# REASON examples:   strategy, interpretation, novel hypothesis, ethics
```

---

## Dispatch table

```python
DISPATCH_TABLE = {
    # === COMPUTATION ===
    "numerical":         "skill-01-python-executor",   # numpy/scipy/sympy
    "symbolic_algebra":  "skill-09-sympy",             # CAS
    "sat_constraint":    "skill-02-sat-solver",        # CaDiCaL, Z3
    "parallel_search":   "skill-18-parallel-search",   # multiprocessing

    # === SCIENTIFIC SIMULATION ===
    "physics_ode":       "skill-07-scipy-sim",         # scipy.integrate
    "fluid_dynamics":    "skill-07-scipy-sim",         # OpenFOAM if local
    "signal_processing": "skill-01-python-executor",   # numpy.fft

    # === FORMAL VERIFICATION ===
    "lean4_proof":       "skill-05-lean4-verify",      # Lean 4 CLI
    "benchmark_check":   "skill-17-benchmark-verifier",

    # === LITERATURE & DATA ===
    "arxiv":             "skill-03-arxiv-fetch",       # arXiv API
    "sequences":         "skill-04-oeis-lookup",       # OEIS API
    "math_query":        "skill-13-wolfram-query",     # WolframAlpha
    "physical_constants":"skill-04-oeis-lookup",       # NIST CODATA

    # === GRAPHS & NETWORKS ===
    "graph_analysis":    "skill-08-networkx",          # networkx
    "p2p_topology":      "skill-08-networkx",

    # === CODE & DOCUMENTS ===
    "doc_convert":       "skill-06-doc-transform",     # pandoc
    "latex_render":      "skill-11-latex-renderer",
    "code_translate":    "skill-10-code-translator",
    "git_ops":           "skill-14-git-operations",

    # === DATA & PIPELINES ===
    "etl_data":          "skill-12-data-pipeline",     # pandas/polars
    "cache_lookup":      "skill-19-knowledge-cache",   # local JSON cache

    # === OPENCLAW-SPECIFIC ===
    "p2pclaw_api":       "skill-15-p2pclaw-lab",
    "paper_generate":    "skill-20-report-generator",

    # === ALWAYS ACTIVE ===
    "output_format":     "token-compression",          # every response
}
```

---

## Error & fallback protocol

```
skill.execute() → error
    │
    ├─ ImportError/NotFound  → bash: pip install {dep} → retry
    ├─ TimeoutError          → reduce scope → retry with smaller params
    ├─ WrongResult           → cross-verify with second tool
    ├─ NetworkError          → use cached version if ∃ → else reason
    └─ UnknownError          → reason_compressed() + log for skill improvement
```

---

## Decision flowchart

```
INPUT TASK
    │
    ▼
[token-compression ALWAYS ON for output]
    │
    ▼
is_deterministic ∧ has_tool?
    │
  YES │                    NO
    │                       │
    ▼                       ▼
check cache             needs external data?
    │                       │
  HIT │    MISS           YES │          NO
    │      │                │            │
    ▼      ▼                ▼            ▼
return  execute          fetch API    reason with
cached  skill →          → synthesize  token-compression
result  cache result
```

---

## Skill registry summary

| # | Skill ID | Domain | Token savings | P2PCLAW critical |
|---|----------|--------|--------------|-----------------|
| 01 | python-executor | Numerical compute | ★★★★★ | ✓ |
| 02 | sat-solver | SAT/CSP/coloring | ★★★★★ | ✓ urgent |
| 03 | arxiv-fetch | Literature | ★★★★☆ | ✓ |
| 04 | oeis-nist | Sequences/constants | ★★★☆☆ | ✓ |
| 05 | lean4-verify | Formal proofs | ★★★★☆ | ✓ |
| 06 | doc-transform | Pandoc/PDF/DOCX | ★★★★★ | △ |
| 07 | scipy-sim | Physics simulation | ★★★★★ | △ |
| 08 | networkx | Graph analysis | ★★★★★ | ✓ |
| 09 | sympy | Symbolic algebra | ★★★★☆ | ✓ |
| 10 | code-translator | Lang conversion | ★★★☆☆ | △ |
| 11 | latex-renderer | Formal docs | ★★★☆☆ | ✓ |
| 12 | data-pipeline | ETL/pandas | ★★★★☆ | △ |
| 13 | wolfram-query | Advanced math | ★★★★☆ | ✓ |
| 14 | git-operations | Version control | ★★★☆☆ | △ |
| 15 | p2pclaw-lab | OpenCLAW API | ★★★★★ | ✓ |
| 16 | token-compression | Output optimizer | ∞ | ✓ installed |
| 17 | benchmark-verifier | Auto verification | ★★★★☆ | ✓ |
| 18 | parallel-search | Parallel compute | ★★★★★ | ✓ urgent |
| 19 | knowledge-cache | Result caching | ★★★★☆ | ✓ |
| 20 | report-generator | Paper generation | ★★★☆☆ | ✓ |

---

## Success metrics

```python
metrics = {
    "token_reduction":      "> 60% vs no-skill baseline",
    "reasoning_quality":    "≥ baseline (zero degradation)",
    "delegation_rate":      "> 80% of deterministic tasks",
    "tool_success_rate":    "> 95% (with fallback)",
    "cache_hit_rate":       "> 40% in long sessions",
}
# ALARM: if agent spends > 200 tokens describing a computation
# that Python could execute in 3 lines → King-Skill not routing correctly
```

---

## Corrected dispatch order (order matters — specific before general)

```python
# VERIFIED routing — 18/19 test cases pass
# Key rule: list specific skills BEFORE general ones
DISPATCH_ORDER = [
    "skill-15-p2pclaw-lab",       # most specific first
    "skill-20-report-generator",
    "skill-11-latex-renderer",
    "skill-09-sympy",             # BEFORE skill-01 (both catch "integral")
    "skill-01-python-executor",
    "skill-02-sat-solver",
    "skill-03-arxiv-fetch",
    "skill-04-oeis-nist",
    "skill-05-lean4-verify",
    "skill-06-doc-transform",
    "skill-07-scipy-sim",
    "skill-08-networkx",
    "skill-10-code-translator",
    "skill-12-data-pipeline",
    "skill-13-wolfram-query",
    "skill-14-git-operations",
    "skill-18-parallel-search",
    "skill-19-knowledge-cache",
    # fallback:
    "token_compression + direct_reasoning",
]
```
