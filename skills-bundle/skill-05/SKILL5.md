---
name: skill-05-lean4-verify
description: >
  Verify formal proofs and check mathematical claims using Lean 4 via bash_tool.
  Critical for OpenCLAW Claims-Boundary Matrix (CBM) verification.
  Triggers: "verify proof", "Lean 4", "formal verification", "CBM", "theorem",
  "prove that", "check formally", "FORMAL_PENDING", "type-check".
token_savings: 4/5
dependencies: lean4 (elan), mathlib4
---

## Install

```bash
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
source ~/.elan/env
elan install leanprover/lean4:stable
```

## Pattern: inline verification

```lean4
-- Save to /tmp/verify.lean then: lean /tmp/verify.lean
import Mathlib.Tactic

-- CBM status markers:
-- ✓ VERIFIED | ⚠ PARTIAL | ✗ PENDING | sorry = FORMAL_PENDING

theorem example_claim (n : ℕ) (h : n > 0) : n * 2 > n := by
  omega

-- For OpenCLAW peer review claims:
structure Claim where
  statement  : Prop
  cbm_status : String  -- "VERIFIED" | "PARTIAL" | "PENDING"
  lean4_proof: Option String
```

## CBM integration (OpenCLAW)

```python
# Classify claim before writing paper section:
CBM = {
    "VERIFIED":  "∃ Lean4 proof | empirically reproduced",
    "PARTIAL":   "strong evidence, no formal proof",
    "PENDING":   "hypothesis, needs verification",
    "REFUTED":   "∃ counterexample",
}
```

## Quick check via bash_tool

```bash
echo 'theorem t : 2 + 2 = 4 := by norm_num' > /tmp/t.lean
lean /tmp/t.lean && echo "VERIFIED" || echo "FAILED"
```
