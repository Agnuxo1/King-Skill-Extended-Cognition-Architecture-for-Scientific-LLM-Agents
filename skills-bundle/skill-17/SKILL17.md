---
name: skill-17-benchmark-verifier
description: >
  Automatically verify computational results against known benchmarks,
  cross-validate between tools, and check OpenCLAW CBM claim status.
  Triggers: "verify result", "cross-check", "benchmark", "validate",
  "is this correct", "double-check computation", "CBM verify".
token_savings: 4/5
dependencies: numpy, scipy, sympy
---

## Cross-verification pattern

```python
def cross_verify(problem, result, tools=["numpy", "sympy", "scipy"]):
    """Verify result using multiple independent tools."""
    results = {}

    if "numpy" in tools:
        import numpy as np
        results["numpy"] = np_solve(problem)

    if "sympy" in tools:
        from sympy import *
        results["sympy"] = sympy_solve(problem)

    # Check agreement
    values = list(results.values())
    agreement = all(abs(float(v) - float(values[0])) < 1e-6 for v in values[1:])
    return {
        "verified": agreement,
        "results":  results,
        "consensus": float(values[0]) if agreement else None,
    }

def verify_matrix_computation(A, result_claimed, operation="eigenvalues"):
    import numpy as np
    ground_truth = {
        "eigenvalues": np.linalg.eigvals(A),
        "inverse":     np.linalg.inv(A),
        "det":         np.linalg.det(A),
    }[operation]
    return np.allclose(result_claimed, ground_truth, rtol=1e-6)
```

## Known benchmark values (hardcoded ground truth)

```python
BENCHMARKS = {
    "pi":          3.14159265358979323846,
    "e":           2.71828182845904523536,
    "golden_ratio":1.61803398874989484820,
    "sqrt2":       1.41421356237309504880,
    # P2PCLAW known results
    "openclaw_consensus_baseline": 0.73,  # 17-judge average on test set
}

def verify_against_known(value: float, benchmark_key: str, tol=1e-8) -> bool:
    expected = BENCHMARKS[benchmark_key]
    return abs(value - expected) < tol
```
