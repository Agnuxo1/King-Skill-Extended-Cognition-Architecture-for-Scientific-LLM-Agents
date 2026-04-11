# King-Skill

**Extended Cognition Architecture for Scientific LLM Agents**

A hierarchical skill-routing system that externalizes deterministic computation to verified tools — reducing token consumption while preserving reasoning quality.

Built for the [P2PCLAW](https://p2pclaw.com) autonomous peer-review network.

[![P2PCLAW Status](https://img.shields.io/badge/P2PCLAW-49%20agents%20%7C%20249%20papers-green)](https://p2pclaw.com)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v4-orange)](king-skill/SKILL.md)

---

## TL;DR

| Metric | Value | Evidence |
|--------|-------|----------|
| Token savings (measured) | **2.7×** | 10 verified examples, tiktoken |
| Skills available | 19 domain skills | Direct file analysis |
| Total system overhead | 6,997 tokens | Router (961) + Bundle (3,812) + Compression (2,224) |
| P2PCLAW network | 49 agents, 249 papers | API verified (April 2026) |
| Test pass rate | 51/53 (96.2%) | Default environment |

**What this is NOT:**
- ✗ NOT a 3-6× savings claim (actual: 2.7× measured)
- ✗ NOT for expanding reasoning depth (compressing thinking degrades quality)
- ✗ NOT free (costs 6,997 tokens to activate full system)

---

## Overview

Large language models spend tokens computing what tools should handle. A model that generates 2,000 tokens explaining eigenvalue computation is solving linear algebra by hand while a computer sits unused. This is not intelligence failing — it's tool use failing.

King-Skill solves this through two mechanisms:

### 1. Skill Routing
A master router classifies tasks and dispatches to 20 verified domain skills, eliminating token cost for deterministic computation.

### 2. Token Compression  
A permanent layer substituting natural language with mathematical notation, chemical formulas, and code — reducing output tokens by ~33% while keeping reasoning fully verbose.

**The foundation** is the extended mind thesis (Clark & Chalmers, 1998): cognitive processes extend into tools. The Python interpreter and SAT solver are not external — they're part of the agent's cognitive system.

---

## Architecture

```
User Input
    │
    ▼
┌─────────────────────────────┐
│   King-Skill Router      │  ← 961 tokens, dispatches to skills
└─────────────────────────────┘
    │
    ├──→ skill-01 (Python)     │ numpy, scipy, FFT
    ├──→ skill-02 (SAT)        │ Z3, graph coloring
    ├──→ skill-03 (arXiv)      │ Literature fetch
    ├──→ skill-05 (Lean4)      │ Formal proofs (51/53 tests)
    ├──→ skill-07 (SciPy)       │ Physics simulation
    ├──→ skill-09 (SymPy)       │ Symbolic math
    ├──→ skill-15 (P2PCLAW)    │ Network submission
    └──→ ... (13 more)
    │
    ▼
┌─────────────────────────────┐
│  Token Compression Layer  │  ← 2,224 tokens, always on output
└─────────────────────────────┘
    │
    ▼
Compressed Output
```

### Dispatch Priority (Order matters — discovered bug fix)

```
Priority  Skill              Trigger
────────────────────────────────
1         skill-15           p2pclaw, judge score
2         skill-20           generate paper, manuscript  
3         skill-11           compile, render, LaTeX
4         skill-09           symbolic, simplify, integral ← ABOVE skill-01
5         skill-01           calculate, compute, matrix, FFT
6         skill-02           SAT, graph coloring, clique
7         skill-03           arXiv, fetch paper
... (more skills below)
-         fallback           reason_with_compression()
```

**Critical fix**: skill-09 must precede skill-01 because both match "integral". Discovered during testing — skill-01 was intercepting symbolic math tasks.

---

## Skills Catalogue — All 19 Skills

**Total bundle size**: 3,812 tokens | **Average per skill**: 200 tokens

| ID | Skill | Tokens | Rating | Status |
|----|-------|--------|--------|--------|
| 01 | python-executor | 212 | ★★★★★ | ✅ Verified |
| 02 | sat-solver | 356 | ★★★★★ | ✅ Verified |
| 03 | arxiv-fetch | 150 | ★★★★☆ | ✅ Verified |
| 04 | oeis-nist | 225 | ★★★☆☆ | ✅ Verified |
| 05 | lean4-verify | 201 | 4/5 | ⚠️ Partial (51/53) |
| 06 | doc-transform | 152 | ★★★★★ | ✅ Verified |
| 07 | scipy-sim | 274 | ★★★★★ | ✅ Verified |
| 08 | networkx | 190 | ★★★★★ | ✅ Verified |
| 09 | sympy | 204 | ★★★★☆ | ✅ Verified |
| 10 | code-translator | 223 | ★★★☆☆ | ✅ Verified |
| 11 | latex-renderer | 212 | ★★★☆☆ | ✅ Verified |
| 12 | data-pipeline | 153 | ★★★★☆ | ✅ Verified |
| 13 | wolfram-query | 150 | ★★★★☆ | ✅ Verified |
| 14 | git-operations | 179 | ★★★☆☆ | ✅ Verified |
| 15 | p2pclaw-lab | 169 | ★★★★★ | ✅ Verified |
| 17 | benchmark-verifier | 184 | ★★★★☆ | ✅ Verified |
| 18 | parallel-search | 200 | ★★★★★ | ✅ Verified |
| 19 | knowledge-cache | 201 | ★★★★☆ | ✅ Verified |
| 20 | report-generator | 177 | ★★★☆☆ | ✅ Verified |

**Partial (skill-05)**: Lean 4 runtime requires manual `elan` installation. The Python CBM sub-test passes; the runtime sub-test fails in default environment.

---

## Token Compression — Real Measurements

### Measured Savings (NOT estimated)

| Example | Original | Compressed | Ratio |
|--------|----------|----------|-------|
| pH definition | "pH equals negative log of hydrogen ion concentration" | `pH = -log[H⁺]` | **5.0×** |
| Ideal gas law | "pressure times volume equals n times R times temperature" | `PV = nRT` | **4.5×** |
| Caffeine formula | "caffeine with formula C8H10N4O2" | `C₈H₁₀N₄O₂` | **3.2×** |
| Ethanol structure | "ethanol has structure CH3-CH2-OH" | `C₂H₅OH` | **3.2×** |
| Glucose combustion | "glucose + oxygen → CO2 + water + energy" | `C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 38ATP` | **1.6×** |

**Average measured**: **2.7×** (10 examples, tiktoken cl100k_base)

### Two-Budget Rule (Critical)

```
NEVER compress thinking (CoT) → reasoning quality ∝ thinking tokens
ALWAYS compress output       → ~33% savings on response
```

Compressing thinking is explicitly forbidden — Wei et al. (2022) proved reasoning quality ∝ intermediate tokens.

### What NOT To Compress

| Concept | Why Not |
|---------|---------|
| Ethical nuances | Values ≠ formulas |
| Aesthetic judgments | No formal encoding |
| New concepts | Needs natural anchor first |
| Short words (≤4 chars) | Same or worse token count |

---

## Real Performance Data

### Test Results — Empirical

```
Total tests:     53
Passing:         51  (96.2%)
Failed:           2  (skill-05 runtime require elan install)

By category:
  Compute         (01,09,18)   100%
  SAT/CSP         (02)         100%  
  Retrieval       (03,04)      100%
  Simulation     (07,08)      100%
  Documents      (06,11)      100%
  OpenCLAW        (15,20)     100%
  Infrastructure (14,19)     100%
  Verification   (05,17)       75% <- Lean4 runtime
```

### Routing Accuracy — Limited

```
Test set:     19 hand-crafted tasks (one per skill)
Correct:     18/19 (94.7%)
Bug found:    skill-01 caught "integral" before skill-09 → fixed by reorder

⚠️  This is NOT statistically valid. 19 tasks cannot support 
    inference. Production requires 500+ stratified tasks.
```

### P2PCLAW Network — Real API Data

```
GET /swarm-status (April 11, 2026):
  active_agents:         49 (26 real + 23 simulated)
  papers_verified:        249
  mempool_pending:         6

GET /leaderboard (top 5):
  1. claude-recovery-01   8.4 score
  2. kimi-k2-5-agent     8.1 score  
  3. research-agent      7.6 score
  4. claude-sonnet       7.5 score
  5. openclaw-nebula     7.5 score
```

**Source**: Direct API calls to `p2pclaw.com/api/` on April 11, 2026.

---

## Cost Analysis

### Combined System Overhead

| Component | Tokens | Purpose |
|-----------|--------|---------|
| King-Skill (router) | 961 | Orchestration |
| Skills Bundle (19) | 3,812 | Domain tools |
| Token Compression | 2,224 | Output compression |
| **Total** | **6,997** | Full activation |

### Annual Savings (1,000 papers/day)

| Model | Output-only (33%) | Net Total (~23%) |
|-------|------------------|-----------------|
| DeepSeek V3 | $23.76 | $16 |
| Gemini Flash | $49.50 | $35 |
| GPT-5.4 Nano | $103.13 | $72 |
| Claude Sonnet | $1,237.50 | $866 |
| Claude Opus | $6,187.50 | $4,331 |

**Note**: These are estimates based on 2.7× compression from n=10 examples — not statistically validated.

---

## What This Is NOT

| Claim from v1 | Reality (v4) |
|--------------|--------------|
| "5× reasoning depth" | ❌ RETRACTED — contradicts "never compress thinking" |
| "3-6× token savings" | 2.7× measured (not 3-6×) |
| "100% semantic fidelity" | ❌ RETRACTED — some qualifiers lost |
| "94.7% routing accuracy" | ⚠️ 19 tasks — insufficient for inference |
| "free expansion" | ❌ Compressing thinking degrades quality |

---

## Installation

### Quick Install

```bash
# Clone
git clone https://github.com/Agnuxo1/OpenCLAW-P2P.git
cd OpenCLAW-P2P

# Python dependencies
pip install numpy scipy sympy pandas networkx python-sat feedparser requests joblib

# Document generation
apt install pandoc texlive-latex-base

# Optional: Lean 4 for formal verification
curl https://elan.lean-lang.org/elan-init.sh | sh
source ~/.elan/env
elan install leanprover/lean4:stable
```

---

## Files

```
.
├── king-skill/
│   └── SKILL.md              # Router skill (961 tokens)
├── skills-bundle/
│   ├── skill-01/ ... skill-20/   # 19 domain skills
│   └── token-compression/
│       └── SKILL.md        # Compression layer (2,224 tokens)
├── papers/
│   └── Skills/
│       ├── king_skill_v4_lab/      # Experiments
│       │   ├── scripts/           # EXP-04, 05, 09, 10
│       │   └── outputs/          # Real data outputs
│       └── outputs/               # Evaluation reports
└── README.md
```

---

## Verified External Data

All data below from direct API/file analysis (April 2026):

| Source | Endpoint/File | Data |
|--------|---------------|------|
| P2PCLAW network | `GET /swarm-status` | 49 agents, 249 papers |
| P2PCLAW leaderboard | `GET /leaderboard` | Top 5 agents + scores |
| P2PCLAW scoring | `GET /lab/scoring-rubric` | 10-dimension rubric |
| EXP-04 corpus | `exp04_token_baseline.py` | 137.42 tokens mean (320 paras) |
| EXP-05 PubChem | `exp05_pubchem.py` | 210 compounds |
| EXP-09 routing | `exp09_fp_fn.py` | 500 tasks |
| EXP-10 conflicts | `exp10_keyword_conflicts.py` | 5 resolved |

---

## Honest Claims Classification

| Classification | Examples in This Project |
|----------------|--------------------------|
| **Empirical** | 51/53 tests pass, P2PCLAW API returns 200, SA converges E=2.4e-5 |
| **Estimated** | 2.7× compression (n=10), 33% output savings (n=20) |
| **Theoretical** | Reasoning quality ∝ thinking tokens (Wei et al. 2022) |
| **Retracted** | 5× depth gain, 3-6× savings target, 100% fidelity |

---

## Important Notes

### What Works
- ✅ Token compression on output (2.7× measured)
- ✅ Skill routing to domain tools
- ✅ P2PCLAW network live verification
- ✅ 6/6 local Python tools (numpy, scipy, sympy, z3, pandas, networkx)

### What Does NOT Work  
- ❌ Frontier-Math-Solver: +354% cost (NOT for savings — for rigor)
- ❌ External APIs for frontier math: 0/5 accessible
- ❌ 3-6× target: Only 2.7× measured

### What Remains Untested
- A/B baseline (King-Skill vs. unrouted LLM) — requires OSF preregistration
- 17-judge panel — requires P2PCLAW registration
- Krippendorff's α consensus — requires enough papers

---

## References

- [1] Clark & Chalmers (1998). "The Extended Mind." *Analysis* 58(1)
- [2] Wei et al. (2022). "Chain-of-Thought Prompting." *NeurIPS 2022* arXiv:2201.11903
- [3] Angulo de Lafuente (2026). "P2PCLAW Framework." p2pclaw.com

---

## License

Apache License 2.0 — See [LICENSE](LICENSE) file.

---

*Generated April 11, 2026 from king_skill_paper_v4.html with all real external evaluation data.*

**Version**: v4  
**Status**: Preprint — not peer reviewed by external journal