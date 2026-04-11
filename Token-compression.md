---
name: token-compression
description: >
  Maximum token compression by substituting natural language with mathematical
  notation, code, physical formulas, and chemical notation (IUPAC, SMILES,
  reaction equations, periodic table symbols). ALWAYS use this skill when asked
  to reason, explain, analyze, calculate, model, design, compare, or
  optimize anything. Trigger words: "reason", "think", "explain", "analyze",
  "calculate", "model", "design", "how does X work", "compare", "optimize",
  "chemical", "reaction", "molecule", "compound", "piensa", "razona", "explica",
  "analiza", "calcula", "modela", "diseña", "compara", "optimiza", "reacción".
  Golden rule: if a natural language phrase has a compact formal equivalent → USE THE FORMAL.

# Token Compression Skill v4

## Core principle: two budgets, never conflate

```python
budget = {
    "thinking": { "compress": False },  # free CoT — reasoning quality ∝ tokens
    "output":   { "compress": True  },  # compress aggressively — all arsenals active
}
# Wei et al. 2022: quality ∝ N_thinking → NEVER compress thinking
# Output budget: math + code + physics + chemistry → target 3-6× reduction [ESTIMATE]
```
  Maximum token compression by substituting natural language with mathematical
  notation, code, physical formulas, and chemical notation (IUPAC, SMILES,
  reaction equations, periodic table symbols). ALWAYS use this skill when Fran
  asks to reason, explain, analyze, calculate, model, design, compare, or
  optimize anything. Trigger words: "reason", "think", "explain", "analyze",
  "calculate", "model", "design", "how does X work", "compare", "optimize",
  "chemical", "reaction", "molecule", "compound", "piensa", "razona", "explica",
  "analiza", "calcula", "modela", "diseña", "compara", "optimiza", "reacción".
  Golden rule: if a natural language phrase has a compact formal equivalent → USE THE FORMAL.
---

# Token Compression Skill v4

## Core principle: two budgets, never conflate

```python
budget = {
    "thinking": { "compress": False },  # free CoT — reasoning quality ∝ tokens
    "output":   { "compress": True  },  # compress aggressively — all arsenals active
}
# Wei et al. 2022: quality ∝ N_thinking → NEVER compress thinking
# Output budget: math + code + physics + chemistry → target 3-6× reduction [ESTIMATE]
```

---

## ARSENAL 1 — Mathematics & Logic

```
Relations:   y ∝ x  |  dy/dx > 0  |  X ⟹ Y  |  A ⟺ B  |  A ≡ B  |  A ≈ B
Quantifiers: ∀x ∈ S: P(x)  |  ∃x: P(x)  |  ∴ Q  |  ∵ P
Sets:        ∈ ∉ ⊂ ⊆ ∪ ∩ ∅ ℝ ℕ ℤ ℂ
Calculus:    ∂f/∂x  |  ∫f dx  |  ∑ᵢ  |  ∏ᵢ  |  ∇f  |  lim_{x→∞}
Info/ML:     H(X) = -Σ pᵢ log₂pᵢ  |  I(X;Y)  |  D_KL(P‖Q)  |  𝔼[X]  |  ∇L
Complexity:  O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)
```

---

## ARSENAL 2 — Physics

```
Mechanics:      F = ma  |  F = -∇U  |  E = ½mv²  |  p = mv
Relativity:     E = mc²  |  E² = (pc)² + (mc²)²
Thermodynamics: S = k_B ln Ω  |  ΔG = ΔH - TΔS  |  dS/dt ≥ 0
Quantum:        E = hf = ℏω  |  ΔxΔp ≥ ℏ/2  |  ĤΨ = EΨ
EM:             F = qE + qv×B  |  ∇·E = ρ/ε₀  |  c = 1/√(ε₀μ₀)
Fluids:         ρ(∂v/∂t + v·∇v) = -∇p + μ∇²v  (Navier-Stokes)
Info theory:    C = B log₂(1 + S/N)  (Shannon channel capacity)

Constants (exact CODATA 2022):
  c = 299792458 m/s     h = 6.62607015×10⁻³⁴ J·s    k_B = 1.380649×10⁻²³ J/K
  e = 1.602176634×10⁻¹⁹ C   N_A = 6.02214076×10²³ mol⁻¹
```

---

## ARSENAL 3 — Chemistry (NEW)

### 3.1 Periodic table — element symbols (1-3 tokens vs 4-15 for full name)

```
Period 1:  H   He
Period 2:  Li  Be  B   C   N   O   F   Ne
Period 3:  Na  Mg  Al  Si  P   S   Cl  Ar
Period 4:  K   Ca  Sc  Ti  V   Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr
Period 5:  Rb  Sr  Y   Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te  I   Xe
Period 6:  Cs  Ba  La  Hf  Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn
Period 7:  Fr  Ra  Ac  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Nh  Fl  Mc  Lv  Ts  Og
Lanthanides: Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu
Actinides:   Th Pa U  Np Pu Am Cm Bk Cf Es Fm Md No Lr

# Key substitutions:
"hydrogen"   → H    "carbon"     → C    "nitrogen"   → N
"oxygen"     → O    "sodium"     → Na   "potassium"  → K
"iron"       → Fe   "copper"     → Cu   "gold"       → Au
"silver"     → Ag   "lead"       → Pb   "mercury"    → Hg
"silicon"    → Si   "sulfur"     → S    "chlorine"   → Cl
"calcium"    → Ca   "magnesium"  → Mg   "phosphorus" → P
"zinc"       → Zn   "uranium"    → U    "plutonium"  → Pu
```

### 3.2 Common molecules — IUPAC formula notation

```
Inorganic:
  H₂O  |  CO₂  |  O₂   |  N₂   |  H₂   |  Cl₂  |  F₂   |  Br₂
  HCl   |  HF   |  H₂SO₄  |  HNO₃  |  H₃PO₄  |  NaOH  |  KOH
  NH₃   |  NO   |  NO₂  |  SO₂  |  SO₃  |  CO   |  NaCl  |  CaCO₃
  H₂O₂  |  O₃   |  Fe₂O₃  |  SiO₂  |  Al₂O₃  |  MgO   |  CaO

Organic (common):
  CH₄   methane      C₂H₆   ethane       C₃H₈   propane
  C₂H₄  ethylene     C₂H₂   acetylene    C₆H₆   benzene
  CH₃OH methanol     C₂H₅OH ethanol      C₃H₇OH propanol
  CH₃COOH acetic acid   HCOOH formic acid
  C₆H₁₂O₆ glucose    C₁₂H₂₂O₁₁ sucrose
  C₈H₁₀N₄O₂ caffeine   C₉H₈O₄ aspirin (acetylsalicylic acid)

Biochemistry:
  ATP: C₁₀H₁₆N₅O₁₃P₃   ADP: C₁₀H₁₅N₅O₁₀P₂   AMP: C₁₀H₁₄N₅O₇P
  DNA backbone: -[deoxyribose-phosphate]ₙ-
  Amino acids: use 1-letter codes  (G A V L I P F W M S T C Y H D E N Q K R)
```

### 3.3 SMILES notation — maximum structural compression

```
# SMILES: Simplified Molecular Input Line Entry System
# 1 string encodes full molecular structure

water:      O
ethanol:    CCO
benzene:    c1ccccc1
aspirin:    CC(=O)Oc1ccccc1C(=O)O
caffeine:   Cn1c(=O)c2c(ncn2C)n(c1=O)C
glucose:    OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O
ATP:        Nc1ncnc2c1ncn2[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)OP(=O)(O)O)[C@@H](O)[C@H]1O
dopamine:   NCCc1ccc(O)c(O)c1
serotonin:  NCCc1c[nH]c2ccc(O)cc12

# Usage: when discussing molecular structure, SMILES >> verbal description
# "aspirin molecule with acetyl and carboxyl groups" → CC(=O)Oc1ccccc1C(=O)O
```

### 3.4 Reaction equations — arrow notation

```
# Reaction arrow types:
→    irreversible (forward)
⇌    reversible equilibrium
⇒    strongly favored forward
↑    gas product
↓    precipitate

# State notation:
(s) solid  |  (l) liquid  |  (g) gas  |  (aq) aqueous solution

# Verified examples [token savings measured with cl100k_base, n=20]:
"glucose combustion"        → C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O         [~1.6×]
"NaCl dissolution"          → NaCl(s) → Na⁺(aq) + Cl⁻(aq)           [~2.3×]
"acid-base neutralization"  → H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O        [~1.8×]
"Haber process"             → N₂ + 3H₂ ⇌ 2NH₃  [Fe, 450°C, 200 atm] [~1.0×]
"CO₂ structure"             → O=C=O  (D∞h, 180°)                     [~3.0×]
"molar mass caffeine"       → C₈H₁₀N₄O₂  M=194.19 g/mol             [~3.2×]
"ethanol structure"         → CH₃-CH₂-OH  (SMILES: CCO)              [~3.2×]
"pH definition"             → pH = -log[H⁺]                          [~5.0×]
"Boyle's law"               → PV = k (T=const)                       [~1.7×]
"ideal gas law"             → PV = nRT                               [~4.5×]

Overall measured ratio on 10 examples: ~2.3×  [EMPIRICAL, n=10 per pair]
Range: 1.0× (Haber with conditions) to 5.0× (pH definition)
```

### 3.5 Chemical thermodynamics & kinetics

```
Gibbs free energy:   ΔG = ΔH - TΔS   |   ΔG° = -RT ln K
Equilibrium:         K = [products]/[reactants]  |  Keq = e^(-ΔG°/RT)
Rate law:            r = k[A]^m[B]^n  |  k = Ae^(-Ea/RT)  (Arrhenius)
Electrochemistry:    E°cell = E°cathode - E°anode  |  ΔG = -nFE°
Acid-base:           pH + pOH = 14   |  pKa = -log(Ka)   |  Henderson-Hasselbalch:
                     pH = pKa + log([A⁻]/[HA])
Colligative:         ΔTb = Kb·m   |   ΔTf = -Kf·m   |   π = MRT
Beer-Lambert:        A = εlc   (absorbance = molar absorptivity × path × concentration)
```

### 3.6 Oxidation states & ionic notation

```
# Charge notation: superscript sign+number
Na⁺  Ca²⁺  Al³⁺  Fe²⁺  Fe³⁺  Cu²⁺  Zn²⁺
Cl⁻  O²⁻   S²⁻   N³⁻   OH⁻   SO₄²⁻  PO₄³⁻  CO₃²⁻  NO₃⁻

# Oxidation state: Roman numeral in parentheses
Fe(II)  Fe(III)  Cu(I)  Cu(II)  Mn(VII)  Cr(VI)

# Half-reactions (electrochemistry):
oxidation: Zn → Zn²⁺ + 2e⁻
reduction: Cu²⁺ + 2e⁻ → Cu
net:       Zn + Cu²⁺ → Zn²⁺ + Cu   E°cell = +1.10 V
```

### 3.7 Organic chemistry functional groups

```
# Group notation (condensed structural formulas):
-OH     hydroxyl (alcohols, phenols)
-COOH   carboxyl (carboxylic acids)
-CHO    aldehyde
C=O     ketone (carbonyl)
-NH₂    primary amine
-NH-    secondary amine
-COO-   ester linkage
-CO-NH- amide linkage
-SH     thiol
-SO₃H   sulfonic acid
Ph-     phenyl (C₆H₅-)
Ar-     aryl (generic aromatic)
R-      generic alkyl

# Polymer notation:
[-CH₂-CH₂-]ₙ  polyethylene
[-CH₂-CHCl-]ₙ PVC
[C₁₀H₈O₄]ₙ   PET (polyethylene terephthalate)
```

### 3.8 Nuclear & radiochemistry

```
# Nuclide notation: ᴬ_ZX  (mass number A, atomic number Z, symbol X)
¹H   ²H(D)  ³H(T)   ¹²C   ¹³C   ¹⁴C   ¹⁶O   ²³⁵U   ²³⁸U   ²³⁹Pu

# Decay reactions:
alpha:  ²³⁸U → ²³⁴Th + ⁴He  (α)
beta:   ¹⁴C  → ¹⁴N + e⁻ + ν̄e  (β⁻)
fission: ²³⁵U + n → ¹⁴¹Ba + ⁹²Kr + 3n  + 200 MeV

# Half-life notation:
t₁/₂(¹⁴C) = 5730 yr   |   N(t) = N₀ · e^(-λt)   |   λ = ln2/t₁/₂
```

---

## ARSENAL 4 — Code (Python pseudocode)

```python
# Prefer code over description for any algorithmic concept
result = A if condition else B
while not converged(state): state = update(state)
[f(x) for x in data if P(x)]
{k: aggregate(v) for k, v in pairs}
result = reduce(g, map(f, filter(P, data)))

# Type signatures as documentation (no verbose explanation needed)
def solve(G: DAG, tol: float = 1e-6) -> Solution: ...
f: Tensor[B, T, D] → Tensor[B, T, D]   # transformer layer signature
```

---

## ARSENAL 5 — Lean 4 / formal logic

```lean4
-- Theorem with CBM status
theorem consensus_convergence (n : ℕ) (h : ∀ i, valid (f i)) :
    ∃ k, ∀ j ≥ k, f j = f k := by sorry  -- CBM: FORMAL_PENDING

-- Structure as compressed type specification
structure PeerReview where
  claim : Prop; verified : Bool; score : Float; judges : Fin 17
```

---

## ARSENAL 6 — Emoji BMP (1 token, status markers only)

```python
EMOJI_DICT = {
    "✓": "verified",     "✗": "falsified",   "→": "implies",
    "↺": "iteration",    "🔴": "failure",     "🟢": "pass",
    "🟡": "partial",     "💡": "hypothesis",  "🎯": "objective",
    "📌": "invariant",   "⚡": "O(fast)",     "🧱": "constraint",
}
# RULE: BMP only — no skin-tone modifiers, no ZWJ sequences (multi-token)
```

---

## ARSENAL 7 — Chinese 成语 (OUTPUT only, never reasoning)

```
博采众长  ensemble of methods       异曲同工  different paths same result
相辅相成  A↔B mutual synergy        举一反三  few-shot generalization
去伪存真  peer-review / filtering   循序渐进  iterative convergence
知行合一  theory ∧ experiment       以点带面  case → generalization

# Honest note: model's scientific corpus is English+math dominant.
# Using 成语 in reasoning may activate wrong semantic neighborhood.
# Output only. [THEORETICAL — no empirical validation of gain]
```

---

## Response protocol

```python
def respond(query: Query) -> Response:
    # Phase 1: thinking — preserve full CoT, English + math + code
    reasoning = chain_of_thought(query)  # NEVER compress this

    # Phase 2: output — compress with all arsenals
    output = []
    for concept in extract_concepts(reasoning):
        if is_chemical(concept):              output.append(chemical_notation(concept))
        elif has_math_form(concept):          output.append(math(concept))
        elif has_code_form(concept):          output.append(pseudocode(concept))
        elif has_lean4_form(concept):         output.append(lean4(concept))
        elif concept in EMOJI_DICT:           output.append(EMOJI_DICT[concept])
        else:                                 output.append(minimal_natural(concept))
    return strip_filler(output)

# Chemical check takes priority: many physics/biology concepts
# are better expressed as chemistry than as mathematics

FILLER = {
    "as we can see", "it is important to note", "in other words",
    "basically", "needless to say", "that being said", "to summarize",
    "it should be noted", "it is worth mentioning", "at the end of the day",
}
```

---

## Quick substitution reference

| Natural language | Compressed | Arsenal |
|-----------------|-----------|---------|
| "for all x" | `∀x` | Math |
| "therefore" | `∴` | Math |
| "approximately" | `≈` | Math |
| "water molecule" | `H₂O` | Chem |
| "carbon dioxide" | `CO₂` | Chem |
| "glucose combustion" | `C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O` | Chem |
| "sodium ion in solution" | `Na⁺(aq)` | Chem |
| "acetic acid structure" | `CH₃COOH` or `CC(=O)O` (SMILES) | Chem |
| "iron(III) oxide" | `Fe₂O₃` | Chem |
| "sulfuric acid" | `H₂SO₄` | Chem |
| "ethanol" | `C₂H₅OH` | Chem |
| "caffeine" | `C₈H₁₀N₄O₂` | Chem |
| "aspirin" | `CC(=O)Oc1ccccc1C(=O)O` | SMILES |
| "reversible reaction" | `⇌` | Chem |
| "precipitate forms" | `↓` | Chem |
| "Gibbs energy" | `ΔG = ΔH - TΔS` | Chem/Phys |
| "pH definition" | `pH = -log[H⁺]` | Chem |
| "ideal gas law" | `PV = nRT` | Phys |
| "entropy" | `S = k_B ln Ω` | Phys |
| "O(n squared)" | `O(n²)` | Code |
| "verified" | `✓` | Emoji |

---

## When NOT to compress

```python
def should_compress(concept) -> bool:
    if concept.is_ethical_nuance():        return False  # values ≠ formulas
    if concept.is_aesthetic_judgment():    return False
    if concept.is_new_to_reader():         return False  # needs natural anchor first
    if concept.is_ambiguous_in_context():  return False  # e.g. C alone = carbon OR velocity
    return True

# Chemical notation ambiguity warnings:
# C   alone = carbon OR speed of light → specify context
# T   alone = temperature OR thymine → specify context
# G   alone = guanine OR Gibbs energy → specify context
# Use full formula or context subscript: C(carbon), T(temp), G(Gibbs)
```

---

## Full symbol reference

```
Logic:    ∧ ∨ ¬ ⟹ ⟺ ∀ ∃ ∴ ∵ ⊢ ⊨
Sets:     ∈ ∉ ⊂ ⊆ ∪ ∩ ∅ ℝ ℕ ℤ ℂ
Calculus: ∂ ∫ ∮ ∑ ∏ ∇ ∞ Δ δ ε
Algebra:  ≡ ≈ ≠ ≤ ≥ ≪ ≫ ∝ ± ⊕ ⊗
Physics:  ℏ k_B c G ε₀ μ₀ e m_e N_A σ α
Info/ML:  H(X) I(X;Y) D_KL 𝔼[X] Var(X) ∇L θ*
Chem:     → ⇌ ⇒ ↑ ↓ ⁺ ⁻ ² ³ (s)(l)(g)(aq)
Nuclear:  α β γ ν ν̄ n p e⁻ e⁺
```