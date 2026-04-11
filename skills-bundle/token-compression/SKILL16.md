---
name: token-compression
description: >
  Maximum token compression by substituting natural language with mathematical
  notation, code, and physical formulas. ALWAYS use this skill when Fran asks
  to reason, explain, analyze, calculate, model, design, compare, or optimize
  anything. Trigger words: "reason", "think", "explain", "analyze", "calculate",
  "model", "design", "how does X work", "compare", "optimize", "piensa", "razona",
  "explica", "analiza", "calcula", "modela", "diseña", "compara", "optimiza".
  Golden rule: if a natural language phrase has a compact formal equivalent → USE THE FORMAL.
---

# Token Compression Skill v3

## Core architecture: two separate budgets

```python
# CRITICAL — never conflate these two budgets
budget = {
    "thinking": {
        "style":    "free CoT in English + math + code",
        "compress": False,   # compressing here degrades quality (Wei et al. 2022)
        "reason":   "intermediate tokens ≡ compute, not output",
    },
    "output": {
        "style":    "maximum compression — full arsenal",
        "compress": True,
        "reason":   "Fran is an expert, reads dense notation without loss",
    },
}
# reasoning_quality ∝ thinking_tokens → DO NOT sacrifice
# output_tokens → compress aggressively
```

---

## Compression arsenal (OUTPUT only)

### 1. Mathematics & physics — empirically validated as optimal

```
# Relations
y ∝ x              # "grows with"
dy/dx > 0          # "increasing trend"
f(A, B)            # "depends on A and B"
X ⟹ Y             # "if X then Y"
∀x ∈ S: P(x)      # "for all x in S, P holds"
∃x: P(x)           # "there exists x such that P"
∴ Q                # "therefore Q"
∵ P                # "because P"
A ⟺ B             # "A if and only if B"
A ≡ B              # "A defined as B"
A ≈ B              # "A approximately B"
A ≪ B              # "A much less than B"
A ∝ B              # "A proportional to B"

# Physics (Fran's context: thermodynamics, information, neuromorphic computing)
S = k_B ln(Ω)              # thermodynamic entropy
H = -Σ p_i log₂(p_i)      # information entropy
I(X;Y) = H(X) - H(X|Y)    # mutual information
D_KL(P‖Q) = Σ P log(P/Q)  # KL divergence
F = -∇U                    # conservative force
∂S/∂t ≥ 0                  # second law (irreversible)
E = hf = ℏω                # energy quantization
E = mc²                    # mass-energy equivalence
∇²ψ + (2m/ℏ²)(E-V)ψ = 0  # Schrödinger
```

### 2. Python pseudocode — validated (Program-of-Thought > CoT for algorithms)

```python
result = A if condition else B
while not converged(state): state = update(state)
[f(x) for x in data if P(x)]
result = reduce(g, map(f, filter(P, data)))
{k: v for k, v in pairs if condition}
state = {"verified": True, "score": 0.87, "iter": 42}
def solve(graph: DAG, tol: float = 1e-6) -> Solution: ...
```

### 3. Lean 4 / formal logic — optimal for Fran's work (OpenCLAW, CHIMERA)

```lean4
theorem consensus_convergence
  (n : ℕ) (h : ∀ i, valid (f i)) :
  ∃ k, ∀ j ≥ k, f j = f k := by sorry  -- CBM: FORMAL_PENDING

structure PeerReview where
  claim : Prop; verified : Bool; score : Float; judges : Fin 17
```

### 4. Graphs & distributed systems (OpenCLAW context)

```
G = (V, E, w)
DAG: ∀(u,v)∈E: rank(u) < rank(v)
consensus: ∀i,j: lim_{t→∞} state_i(t) = state_j(t)
BFT: correct iff f < n/3            # Byzantine fault tolerance
P2P: ∀node_i: degree(i) ≥ k_min
independence: ∀i≠j: judge_i ⊥ judge_j
```

### 5. Complexity

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ)
space-time tradeoff: S × T ≥ k      # fixed problem-dependent constant
```

### 6. Emoji dictionary — BMP only (1 token guaranteed)

```python
EMOJI_DICT = {
    "✓": "verified/correct",       "✗": "falsified/incorrect",
    "→": "implies/next step",      "↺": "iteration/loop",
    "🔴": "failure/stop",          "🟢": "pass/ok",     "🟡": "partial/warning",
    "💡": "hypothesis/idea",       "🎯": "objective",   "📌": "invariant/fixpoint",
    "⚡": "O(fast)/efficient",     "🧱": "hard constraint",
    "△": "delta/change",           "⊕": "merge/combine",
}
# FORBIDDEN: skin-tone modifiers, ZWJ sequences → multi-token
# RULE: if token count uncertain → do not use
```

### 7. Chinese 成语 — OUTPUT only, NOT for internal reasoning

```
# Honest note: model's scientific corpus is English+math dominant.
# Using 成语 in internal reasoning may degrade quality.
# Use ONLY for output compression of strategic/epistemic concepts.

成语_dict = {
    "异曲同工": "different methods, same result",
    "相辅相成": "A ↔ B mutual reinforcement (synergy)",
    "举一反三": "few-shot generalization",
    "博采众长": "ensemble of methods (OpenCLAW: 17 judges)",
    "去伪存真": "peer-review / noise filtering",
    "循序渐进": "iterative convergence",
    "知行合一": "theory ∧ experiment aligned",
    "以点带面": "case → generalization",
    "亡羊补牢": "post-hoc necessary fix",
    "因果关系": "causal relation",
}
```

### 8. Domain-specific compact notations

```
SMILES:   CC(=O)Oc1ccccc1C(=O)O       # aspirin (molecular structure)
regex:    ^[A-Z]{2}\d{4}$             # compact pattern
cron:     0 */6 * * *                  # "every 6 hours"
JSON:     {"k": v, "k2": v2}          # serialized state
type sig: f : A → B → C               # function signature
Dirac:    ⟨ψ|H|ψ⟩ = E                # quantum expectation
```

---

## Quick substitution table

| Natural language | Compressed |
|-----------------|-----------|
| "as we can see" | *(omit)* |
| "it is important to note" | *(omit)* |
| "in other words" | `⟺` |
| "therefore" | `∴` |
| "because" | `∵` |
| "which means" | `⟹` |
| "if and only if" | `⟺` |
| "for all X" | `∀x` |
| "there exists X" | `∃x` |
| "tends to zero" | `→ 0` |
| "grows with X" | `∝ X` |
| "approximately" | `≈` |
| "much greater than" | `≫` |
| "defined as" | `≡` |
| "P(X given Y)" | `P(X\|Y)` |
| "expectation of X" | `𝔼[X]` |
| "variance of X" | `Var(X)` |
| "independent peer review" | `∀i≠j: judge_i ⊥ judge_j` |
| "Byzantine fault tolerant" | `correct iff f < n/3` |
| "decreasing returns" | `d²f/dx² < 0` |
| "converges to fixed point" | `∃x*: f(x*) = x*` |

---

## Response protocol

```python
def respond(query: Query) -> Response:
    # Phase 1: thinking — DO NOT compress, preserve full CoT
    reasoning = chain_of_thought(query)    # free, English + math + code

    # Phase 2: output — compress aggressively
    concepts = extract_concepts(reasoning)
    output = []
    for c in concepts:
        if has_math(c):      output.append(math(c))
        elif has_code(c):    output.append(pseudocode(c))
        elif has_lean4(c):   output.append(lean4(c))
        elif c in EMOJI_DICT: output.append(EMOJI_DICT[c])
        else:                output.append(minimal_natural(c))

    return strip_filler(output)

FILLER = {
    "as we can see", "it is important to note", "in other words",
    "basically", "in fact", "it should be noted", "to summarize",
    "that being said", "it is worth mentioning", "needless to say",
}
```

---

## When NOT to compress

```python
def should_compress(concept) -> bool:
    if concept.is_ethical_nuance():      return False  # math cannot capture values
    if concept.is_aesthetic_judgment():  return False
    if concept.is_new_to_reader():       return False  # needs natural anchor
    if concept.is_irreducibly_ambiguous(): return False
    return True
```

---

## Full symbol reference

```
Logic:       ∧ ∨ ¬ ⟹ ⟺ ∀ ∃ ∴ ∵ ⊢ ⊨ □ ◇
Sets:        ∈ ∉ ⊂ ⊆ ⊃ ∪ ∩ ∅ ℝ ℕ ℤ ℚ ℂ 𝔽
Calculus:    ∂ ∫ ∮ ∑ ∏ ∇ ∞ lim Δ δ ε
Algebra:     ≡ ≈ ≠ ≤ ≥ ≪ ≫ ∝ ± ⊕ ⊗ †
Physics:     ℏ k_B c G ε₀ μ₀ e m_e N_A σ α
Info/ML:     H(X) I(X;Y) D_KL 𝔼[X] Var(X) ∇L θ* argmax softmax
Complexity:  O() Ω() Θ() → ↦ λ ∘ ⊥ ⊤
Graphs:      G=(V,E) deg(v) DAG BFT path(u,v) ∂G
```
