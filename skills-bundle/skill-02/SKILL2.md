---
name: skill-02-sat-solver
description: >
  Solve Boolean satisfiability, constraint satisfaction, graph coloring,
  scheduling, and combinatorial optimization problems via CaDiCaL/Z3/OR-Tools.
  NEVER reason through SAT problems manually — delegate immediately.
  Triggers: "SAT", "satisfiability", "graph coloring", "constraint", "CSP",
  "combinatorial", "Ramsey", "scheduling", "assignment problem", "clique".
token_savings: ★★★★★
dependencies: python-sat, z3-solver, ortools
---

## When to use
Any combinatorial problem with explicit constraints:
graph coloring, Ramsey numbers, scheduling, packing, covering, clique finding.

## Install

```bash
pip install python-sat z3-solver --break-system-packages
# OR-Tools for scheduling:
pip install ortools --break-system-packages
```

## Pattern: PySAT (CaDiCaL)

```python
from pysat.solvers import Cadical153
from pysat.formula import CNF

formula = CNF()
# Add clauses: each clause = list of literals (positive=True, negative=negate)
formula.append([1, 2])       # x1 OR x2
formula.append([-1, 3])      # NOT x1 OR x3

with Cadical153(bootstrap_with=formula) as solver:
    sat = solver.solve()
    model = solver.get_model() if sat else None
print(f"SAT: {sat}, model: {model}")
```

## Pattern: Z3 (SMT, more expressive)

```python
from z3 import *
x, y = Ints('x y')
s = Solver()
s.add(x + y == 10, x > 0, y > 0, x != y)
result = s.check()
if result == sat:
    m = s.model()
    print(f"x={m[x]}, y={m[y]}")
```

## Graph coloring (k-colorability)

```python
def k_colorable(G: dict, k: int) -> dict | None:
    """G = {node: [neighbors]}. Returns coloring dict or None."""
    from pysat.solvers import Cadical153
    nodes = list(G.keys())
    n = len(nodes)
    # Variable x[i][c] = node i has color c → var_id = i*k + c + 1
    var = lambda i, c: i * k + c + 1
    clauses = []
    for i in range(n):
        clauses.append([var(i, c) for c in range(k)])          # at least 1 color
        for c1 in range(k):
            for c2 in range(c1+1, k):
                clauses.append([-var(i,c1), -var(i,c2)])       # at most 1 color
    for i, nbrs in enumerate(G.values()):
        for j in [nodes.index(nb) for nb in nbrs if nb > nodes[i]]:
            for c in range(k):
                clauses.append([-var(i,c), -var(j,c)])         # no same color
    with Cadical153(bootstrap_with=clauses) as s:
        if s.solve():
            m = s.get_model()
            return {nodes[i]: next(c for c in range(k) if m[var(i,c)-1]>0)
                    for i in range(n)}
    return None
```

## Verification
```python
# Verify coloring
assert all(coloring[u] != coloring[v] for u,nbrs in G.items() for v in nbrs)
```
