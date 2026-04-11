# AGENT INSTRUCTIONS — Ramsey Book Graphs (FrontierMath Open Problems)
# EXCEPTIONAL CASE: attempt limit suspended. Work until complete solution.
# Active skill: token-compression — maximum semantic density, minimum token waste.

---

## CURRENT STATE (inherited from previous session)

```
SOLVED (algebraic, 2-block circulant): 29 values of n ≤ 100
  q=2n-1 prime ≡1(4): {3,7,9,15,19,21,27,31,37,45,49,51,55,57,69,75,79,87,91,97,99}
  q=p²  ≡1(4):        {5,13,25,61,85}     [GF(p²)]
  q=p³⁺ ≡1(4):        {41,63}             [GF(3⁴), GF(5³)]
  SA:                  {4}
  Total:               29/98

WARM-UP  n=25: ✓ (GF(7²), maxR=23, maxB=24, verified)
SINGLE   n=50: ✗ (q=99=9×11, not prime power)
FULL PROBLEM:  ~69 n uncovered

PROVEN BARRIER: 2-block vertex-transitivity → vertex removal cannot reduce books
P2PCLAW PAPER: published (ID paper-1775617067601, DISTINCTION 88%)
```

---

## FINAL OBJECTIVE

Produce `solution(n)` → valid adjacency string ∀n ∈ [2,100] in ≤10 min/n on a standard laptop.

Success condition: maxR(G) ≤ n−2 ∧ maxB(G) ≤ n−1 where G has exactly 4n−2 vertices.

---

## ATTACK PLAN — EXECUTE IN ORDER

### PHASE A — Cover remaining GF(p^k) with k≥4 (fast, algebraic)

```python
from sympy import factorint
covered = {3,4,5,7,9,13,15,19,21,25,27,31,37,41,45,49,51,55,57,61,63,69,75,79,85,87,91,97,99}
for n in range(2, 101):
    if n not in covered:
        q = 2*n - 1
        f = factorint(q)
        if len(f) == 1:          # prime power
            p, k = list(f.items())[0]
            if q % 4 == 1:
                print(f"n={n} q={q}=p^{k} ≡1(4) → GF({q}) FEASIBLE")
```

For each n found: implement GF(p^k) using `galois` library.

```python
import galois
GF  = galois.GF(p**k)
Q   = {int(x) for x in GF.elements if x != 0 and pow(int(x), (q-1)//2, q) == 1}
# Build 2-block construction → adjacency string
```

---

### PHASE B — SAT encoding for uncovered n (critical path)

This is the core method. Wesley's original paper used SAT/IP for non-algebraic cases.

#### Install: `pip install python-sat`

```python
from pysat.solvers import CaDiCal   # use CaDiCal, not Glucose4 (handles larger instances)
from pysat.card import CardEnc, EncType
from pysat.formula import CNF

def solve_ramsey_sat(n, timeout=300):
    N  = 4*n - 2
    RL = n - 2     # max allowed red book size
    BL = n - 1     # max allowed blue book size

    cnf = CNF()
    cnf.nv = 0

    # Edge variable: x_{ij} = 1 → red, 0 → blue (i < j, 0-indexed)
    def var(i, j):
        if i > j: i, j = j, i
        return i*N - i*(i+1)//2 + j - i   # 1-indexed

    cnf.nv = N*(N-1)//2   # reserve base variables

    for u in range(N):
        for v in range(u+1, N):
            W = [w for w in range(N) if w != u and w != v]

            # --- RED constraint ---
            # If edge (u,v) is red → ≤ RL common red neighbors
            # z_w = x_{uw} AND x_{vw}  (auxiliary AND gate)
            aux_r = []
            for w in W:
                z = cnf.nv + 1; cnf.nv += 1
                cnf.append([-z,  var(u,w)])
                cnf.append([-z,  var(v,w)])
                cnf.append([ z, -var(u,w), -var(v,w)])
                aux_r.append(z)

            am_r = CardEnc.atmost(aux_r, bound=RL,
                                   encoding=EncType.seqcounter,
                                   top_id=cnf.nv)
            cnf.nv = am_r.nv
            for clause in am_r.clauses:
                cnf.append([-var(u,v)] + clause)  # x_{uv}=1 → AtMost(RL)

            # --- BLUE constraint ---
            # If edge (u,v) is blue → ≤ BL common blue neighbors
            # z_w = (NOT x_{uw}) AND (NOT x_{vw})
            aux_b = []
            for w in W:
                z = cnf.nv + 1; cnf.nv += 1
                cnf.append([-z, -var(u,w)])
                cnf.append([-z, -var(v,w)])
                cnf.append([ z,  var(u,w),  var(v,w)])
                aux_b.append(z)

            am_b = CardEnc.atmost(aux_b, bound=BL,
                                   encoding=EncType.seqcounter,
                                   top_id=cnf.nv)
            cnf.nv = am_b.nv
            for clause in am_b.clauses:
                cnf.append([var(u,v)] + clause)   # x_{uv}=0 → AtMost(BL)

    # Symmetry breaking: fix first vertex's edge colors (eliminates N! permutation symmetries)
    for j in range(1, min(n, N)):
        cnf.append([ var(0, j)])   # x_{0,j} = red
    cnf.append([-var(0, n)])       # x_{0,n} = blue  (if n < N)

    with CaDiCal(bootstrap_with=cnf.clauses, use_timer=True) as solver:
        if solver.solve_limited(expect_interrupt=True, time=timeout):
            model = set(solver.get_model())
            bits  = []
            for i in range(N):
                for j in range(i+1, N):
                    bits.append('1' if var(i,j) in model else '0')
            return ''.join(bits)
    return None
```

**Note on scale**: n=50 → N=198 → ~19,500 base vars + auxiliaries (~200K total).
CaDiCal handles this. Glucose4 may not. Use CaDiCal or Kissat.

---

### PHASE C — Parallel SA with warm start (fallback)

For n where SAT is slow (large N with dense constraints):

```python
import multiprocessing as mp, random, math, time

def sa_worker(seed, n, adj_init, result_queue):
    random.seed(seed)
    N  = 4*n - 2
    RL = n - 2
    BL = n - 1

    # Decode initial adjacency
    adj = list(adj_init)

    def penalty(adj):
        """Count constraint violations. Target: 0."""
        # Build neighbor lists
        red  = [[] for _ in range(N)]
        blue = [[] for _ in range(N)]
        idx = 0
        for i in range(N):
            for j in range(i+1, N):
                if adj[idx] == '1': red[i].append(j); red[j].append(i)
                else:               blue[i].append(j); blue[j].append(i)
                idx += 1
        pen = 0
        for u in range(N):
            for v in red[u]:
                if v > u:
                    common = len(set(red[u]) & set(red[v]))
                    if common > RL: pen += common - RL
            for v in blue[u]:
                if v > u:
                    common = len(set(blue[u]) & set(blue[v]))
                    if common > BL: pen += common - BL
        return pen

    def edge_idx(i, j):
        if i > j: i, j = j, i
        return i*N - i*(i+1)//2 + j - i - 1

    T    = 1.0
    best = penalty(adj)
    T_min, alpha = 1e-4, 0.9999

    while T > T_min:
        # Flip a random edge
        i = random.randint(0, N-2)
        j = random.randint(i+1, N-1)
        k = edge_idx(i, j)
        adj[k] = '0' if adj[k] == '1' else '1'

        new_pen = penalty(adj)
        delta   = new_pen - best

        if delta <= 0 or random.random() < math.exp(-delta / T):
            best = new_pen
        else:
            adj[k] = '0' if adj[k] == '1' else '1'  # revert

        T *= alpha

        if best == 0:
            result_queue.put(''.join(adj))
            return

        # Reheat if stuck
        if T < 0.01: T = 0.5

def solve_parallel_sa(n, adj_init, num_workers=8, time_limit=300):
    result_queue = mp.Queue()
    procs = [mp.Process(target=sa_worker, args=(s, n, adj_init, result_queue))
             for s in range(num_workers)]
    for p in procs: p.start()

    start = time.time()
    while time.time() - start < time_limit:
        if not result_queue.empty():
            res = result_queue.get()
            for p in procs: p.terminate()
            return res
        time.sleep(0.3)

    for p in procs: p.terminate()
    return None
```

---

### PHASE D — ILP via SCIP (last resort for resistant cases)

```python
# pip install pyscipopt
from pyscipopt import Model

def solve_ramsey_scip(n, time_limit=300):
    N  = 4*n - 2
    RL = n - 2
    BL = n - 1
    m  = Model()
    m.setParam('limits/time', time_limit)
    m.setParam('display/verblevel', 0)

    # Binary vars: x[i,j] = 1 → red
    x = {}
    for i in range(N):
        for j in range(i+1, N):
            x[i,j] = m.addVar(vtype='B', name=f'x_{i}_{j}')

    # For each edge (u,v): auxiliary y[u,v,w] = x[u,w] * x[v,w]  (linearized AND)
    # Then sum_w y[u,v,w] ≤ RL * x[u,v]  (red book constraint)
    # Similarly for blue.
    # Due to scale, use lazy constraints or BigM formulation.

    for u in range(N):
        for v in range(u+1, N):
            W = [w for w in range(N) if w != u and w != v]

            # Linearize y[w] = x[u,w] AND x[v,w]
            yr = {w: m.addVar(vtype='B') for w in W}
            yb = {w: m.addVar(vtype='B') for w in W}

            for w in W:
                uw = (min(u,w), max(u,w))
                vw = (min(v,w), max(v,w))
                # yr[w] ≤ x[u,w], yr[w] ≤ x[v,w], yr[w] ≥ x[u,w]+x[v,w]-1
                m.addCons(yr[w] <= x[uw])
                m.addCons(yr[w] <= x[vw])
                m.addCons(yr[w] >= x[uw] + x[vw] - 1)
                # yb[w] ≤ 1-x[u,w], yb[w] ≤ 1-x[v,w], yb[w] ≥ (1-x[u,w])+(1-x[v,w])-1
                m.addCons(yb[w] <= 1 - x[uw])
                m.addCons(yb[w] <= 1 - x[vw])
                m.addCons(yb[w] >= 1 - x[uw] + 1 - x[vw] - 1)

            uv = (u,v)
            # Red: x[u,v]=1 → sum_w yr[w] ≤ RL
            m.addCons(sum(yr[w] for w in W) <= RL + (N-2)*(1 - x[uv]))
            # Blue: x[u,v]=0 → sum_w yb[w] ≤ BL
            m.addCons(sum(yb[w] for w in W) <= BL + (N-2)*x[uv])

    m.optimize()

    if m.getStatus() == 'optimal':
        bits = []
        for i in range(N):
            for j in range(i+1, N):
                bits.append('1' if m.getVal(x[i,j]) > 0.5 else '0')
        return ''.join(bits)
    return None
```

---

### PHASE E — Master solution(n) function

```python
def solution(n):
    """
    Returns adjacency string for K_{4n-2} 2-colored: no B_{n-1} red, no B_n blue.
    Time limit: ≤10 min per n on a standard laptop.
    """
    # 1. Algebraic: 2-block circulant over GF(q) [instantaneous]
    result = try_two_block_gf(n)
    if result: return result

    # 2. SAT solver [seconds to ~5 min]
    result = solve_ramsey_sat(n, timeout=180)
    if result: return result

    # 3. Parallel SA with warm start from nearest covered n [minutes]
    nearest_adj = get_nearest_covered_adj(n)
    result = solve_parallel_sa(n, nearest_adj, num_workers=8, time_limit=240)
    if result: return result

    # 4. ILP via SCIP [minutes, last resort]
    result = solve_ramsey_scip(n, time_limit=300)
    if result: return result

    raise TimeoutError(f"n={n}: no solution within time budget")
```

---

## MANDATORY VERIFICATION — BEFORE ANY PUBLIC CLAIM

```python
def verify(n, adj):
    N  = 4*n - 2
    RL = n - 2
    BL = n - 1
    assert len(adj) == N*(N-1)//2, f"Wrong length: {len(adj)} ≠ {N*(N-1)//2}"

    # Build adjacency matrix
    A = [[0]*N for _ in range(N)]
    idx = 0
    for i in range(N):
        for j in range(i+1, N):
            c = int(adj[idx]); idx += 1
            A[i][j] = A[j][i] = c

    maxR = maxB = 0
    for u in range(N):
        for v in range(u+1, N):
            cn_r = sum(A[u][w] & A[v][w] for w in range(N) if w!=u and w!=v)
            cn_b = sum((1-A[u][w]) & (1-A[v][w]) for w in range(N) if w!=u and w!=v)
            if A[u][v]: maxR = max(maxR, cn_r)
            else:       maxB = max(maxB, cn_b)

    ok = maxR <= RL and maxB <= BL
    print(f"n={n}: maxR={maxR}/{RL} maxB={maxB}/{BL} {'✓' if ok else '✗ FAIL'}")
    assert ok, f"VERIFICATION FAILED n={n}"
    return ok

# Run for every solved n before any submission
for n in solved_list:
    verify(n, solution(n))
```

---

## PRIORITY ORDER

```
Priority 1 — Single challenge n=50 (FrontierMath target)
  → SAT with CaDiCal, timeout=300s
  → If fails: parallel SA (8 workers, 300s)
  → If fails: SCIP ILP (300s)

Priority 2 — All uncovered n ≤ 20
  → SAT resolves small n in seconds

Priority 3 — All uncovered n 21..49 and 51..100
  → SAT then SA then ILP cascade

Priority 4 — Phase A: check remaining GF(p^k) for k≥4
  → Might add 2-3 more algebraic solutions for free

MINIMUM ACCEPTABLE:
  n=25 ✓ (done) + n=50 ✓ (solve now) → submit warm-up + single challenge

IDEAL:
  ≥90% of n≤100 covered → submit full problem
  100% covered or impossibility proof for remainder → breakthrough
```

---

## SUBMISSION PROTOCOL (only after full verification)

**Step 1** — Update P2PCLAW paper (ID: paper-1775617067601) with complete solution.

**Step 2** — Email Epoch AI at `math@epoch.ai`:
```
Subject: Solution attempt for "Ramsey Numbers for Book Graphs" (FrontierMath Open Problems)

We believe we have a solution to the Ramsey Book Graphs problem.
Attached: solution.py (Python script defining solution(n))
Verification output:
  n=25 (warm-up):          maxR=23/23 maxB=24/24 ✓
  n=50 (single challenge):  maxR=?/?  maxB=?/?  ✓
  ...
We request access to the official verifier to confirm.
```

**Step 3** — Only after Epoch AI verifier confirms → arXiv submission (math.CO + cs.AI + cs.LO).

**Step 4** — Only after arXiv is live → public announcement.

---

## ABSOLUTE RULE

**Zero public claims before: (1) local verification passes AND (2) Epoch AI verifier confirms.**
A false result destroys P2PCLAW's scientific credibility permanently.
A correct result verified rigorously builds it permanently.

---

## TOKEN COMPRESSION PROTOCOL (active throughout)

Replace all natural language with formal notation:

| Instead of...                        | Use...                          |
|--------------------------------------|---------------------------------|
| "for all n"                          | ∀n                              |
| "there exists n such that"           | ∃n:                             |
| "therefore"                          | ∴                               |
| "contradiction"                      | ⊥                               |
| "is not a prime power"               | ∉ {p^k}                         |
| "maximum red book ≤ n-2"            | maxR ≤ RL                       |
| verbose status reports               | `n=50: SAT[t=120s]→✗ SA[t=240s]→?` |

Code > prose. Tables > lists. Symbols > words.

**Correct**: `n=50: q=99=3²×11 ∉ prime_powers → SAT[CaDiCal,t=180s] → ✗ → SA[8w,t=240s]`
**Wrong**:   "For n equal to 50, the value of q which is 99 equals 9 times 11 which means..."

Log only state changes. Never repeat stable information.

---

## KEY REFERENCES

- FrontierMath problem page: https://epoch.ai/frontiermath/open-problems/ramsey-book-graphs
- Full problem write-up PDF: https://epoch.ai/files/open-problems/ramsey-book-graphs.pdf
- Wesley paper (construction): arXiv:2410.03625
- PySAT docs: https://pysathq.github.io
- galois (GF fields): https://mhostetter.github.io/galois
- P2PCLAW paper: https://p2pclaw.com/app/papers/paper-1775617067601
- Verification endpoint: POST https://p2pclaw-mcp-server-production-ac1c.up.railway.app/verify-lean
- Epoch AI contact: math@epoch.ai

---

*Generated: April 8, 2026 | Project: P2PCLAW | Problem: FrontierMath — Ramsey Book Graphs*
*EXCEPTIONAL CASE: attempt limit suspended. Work until complete solution.*
*Token compression skill: ACTIVE*
