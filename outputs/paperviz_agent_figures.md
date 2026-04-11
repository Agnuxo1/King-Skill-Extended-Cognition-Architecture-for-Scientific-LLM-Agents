# PaperVizAgent Input Data - King-Skill v4 Figures

All figure descriptions ready for PaperVizAgent generation.

---

## FIGURE 1: Token Savings Spectrum - Maximum vs Mean

**Chart type**: Grouped bar chart  
**Style**: Academic, side-by-side bars  
**Data**:

| Category | Max Savings (%) | Mean Savings (%) |
|----------|-----------------|------------------|
| Chemical Names (Verbose) | 80 | 30 |
| Reaction Equations | 68 | 50 |
| SMILES (long IUPAC) | 65 | 15 |
| SMILES (common name) | 0 | -40 |
| Physics Formulas | 82 | 12 |
| Complexity O() | 77 | 23 |
| Formal Logic | 68 | 18 |
| Python Pseudocode | 40 | -7 |
| Lean 4 Syntax | 5 | 0 |

**Description for PaperVizAgent**:
```
Create a grouped bar chart showing token savings percentages for 9 different content categories.
Two bars per category: "Maximum (First Mention)" in teal #1a5c4f and "Realistic Mean (Running Text)" in amber #7a5a1e.
X-axis: Content categories (Chemical Names, Reaction Equations, SMILES, Physics, etc.)
Y-axis: Token savings percentage from -50% to +100%
Bar style: Clean academic with subtle border, rounded corners (3px)
Background: Off-white #faf8f4
Include zero line marked prominently.
Legend in top right: "Maximum savings" and "Realistic mean"
Title: "Token Savings Spectrum: Maximum vs. Realistic Mean"
Font: Libre Franklin or similar sans-serif, 12pt
```

---

## FIGURE 2: Informational Density Comparison

**Chart type**: Grouped bar chart (conceptual)  
**Data**:

| Metric | Natural Language | Compressed |
|-------|-------------------|------------|
| Conceptual Density | 0.378 | 0.624 |
| Technical Density | 0.218 | 0.359 |

**Description for PaperVizAgent**:
```
Create a grouped bar chart comparing informational density between natural language and compressed notation.
Two metrics: "Conceptual density" and "Technical density"
Two groups: "Natural language" in blue #1e4d7a and "Compressed notation" in teal #0d6e6e
Y-axis: Density value (0 to 0.8)
Style: Clean academic bars with error bars indicating this is illustrative
Label as "Illustrative estimates - not validated" in small italic text below chart
Title: "Informational Density: Natural Language vs. Compressed Notation"
Subtitle: "Concept counts per token (illustrative, n=20)"
```

---

## FIGURE 3: Test Pass Rates by Skill Category

**Chart type**: Horizontal bar chart  
**Data**:

| Category | Pass Rate (%) |
|----------|---------------|
| Compute (01,09,18) | 100 |
| SAT/CSP (02) | 100 |
| Retrieval (03,04) | 100 |
| Simulation (07,08) | 100 |
| Documents (06,11) | 100 |
| OpenCLAW (15,20) | 100 |
| Infrastructure (14,19) | 100 |
| Verification (05,17) | 75 |

**Description for PaperVizAgent**:
```
Create a horizontal bar chart showing test pass rates by skill category.
8 categories listed vertically on Y-axis (left to right by pass rate)
X-axis: Pass rate from 0% to 110%
All bars in teal #1a5c4f EXCEPT "Verification" in amber #7a5a1e (75%)
Mark 100% as a reference line in light gray
Category labels: "Compute (01,09,18)", "SAT/CSP (02)", "Retrieval (03,04)", etc.
Title: "Test Pass Rates by Skill Category"
Subtitle: "Default environment: 51/53 tests passing"
Note: "Verification at 75% due to Lean 4 runtime (manual install required)"
```

---

## FIGURE 4: Annual Cost Savings by Model Tier

**Chart type**: Grouped bar chart (log scale)  
**Data**:

| Model | Output-Only (33%) | Net Total (~23%) |
|-------|------------------|-----------------|
| DeepSeek V3 | $23.76 | $16 |
| Gemini Flash | $49.50 | $35 |
| GPT-5.4 Nano | $103.13 | $72 |
| DeepSeek R1 | $180.68 | $127 |
| GPT-5.4 Mini | $371.25 | $260 |
| Sonnet 4.6 | $1,237.50 | $866 |
| GPT-5.4 | $1,237.50 | $866 |
| o3 | $3,300.00 | $2,310 |
| Opus 4.6 | $6,187.50 | $4,331 |

**Description for PaperVizAgent**:
```
Create a grouped bar chart with LOGARITHMIC Y-axis showing annual savings in USD.
Models listed on X-axis, ordered by price tier (budget to frontier)
Two bars per model: "Output-only (33%)" in teal #0d6e6e and "Net total (~23%)" in amber #7a5a1e
Y-axis: Log scale with dollars ($10 to $10,000)
Reference line at $1,000 for scale context
Color-coded badges per tier: Budget (green), Mid (amber), Premium (purple), Frontier (blue)
Title: "Annual API Cost Savings by Model Tier"
Subtitle: "At 1,000 papers/day - Output-only vs. Net total savings"
Footnote: "Estimates from n=20 compression examples without confidence intervals"
```

---

## FIGURE 5: Credibility Evolution v1 → v2 → v3 → v4

**Chart type**: Stacked bar chart  
**Data**:

| Version | Empirically Supported | Honest Estimate | Theoretical/Open | Unsupported/Retracted |
|---------|-------------------|---------------|---------------|-------------------|
| v1 (original) | 2 | 1 | 2 | 7 |
| v2 (first revision) | 5 | 4 | 4 | 1 |
| v3 (second revision) | 6 | 5 | 6 | 1 |
| v4 (external eval) | 8 | 4 | 5 | 0 |

**Description for PaperVizAgent**:
```
Create a stacked horizontal bar chart showing claim credibility evolution.
4 versions on Y-axis: "v1 (original)", "v2 (first revision)", "v3 (second revision)", "v4 (external evaluation)"
Stacked segments (left to right):
- "Empirically supported" in teal #1a5c4f (bottom)
- "Honest estimate" in blue #1e4d7a
- "Theoretical / open" in amber #7a5a1e  
- "Unsupported / retracted" in red #8b2020 (top)
X-axis: Number of claims (0 to 10)
Title: "Claim Credibility Evolution: v1 → v4"
Legend: All four categories with color coding
Arrow annotation showing improvement direction between v1 and v4
```

---

## FIGURE 6: System Architecture Diagram

**Description for PaperVizAgent**:
```
Create a flowchart/diagram showing the King-Skill architecture.
Style: Clean academic with rounded rectangles

Box 1 (top, center): "User Input" -> arrow down
Box 2: "King-Skill Router" ( dispatcher) -> arrows to 20 skill boxes arranged in 2x10 grid
Skill boxes arranged by category:
  - Computation: skill-01, skill-18
  - SAT: skill-02  
  - Retrieval: skill-03, skill-04
  - Verification: skill-05, skill-17
  - Documents: skill-06, skill-11, skill-20
  - Simulation: skill-07, skill-08
  - Data: skill-12
  - Math: skill-09, skill-13
  - Code: skill-10
  - Infrastructure: skill-14, skill-15, skill-19

From selected skill -> arrow to "Token Compression Layer"
Token Compression -> arrow to "Output (compressed)"

Color scheme: 
- Router: purple #4a2580
- Skills by category: different accent colors
- Compression: teal #0d6e6e

Title: "King-Skill Architecture: Hierarchical Skill Routing with Token Compression"
Style: Academic diagram with subtle shadows, clean arrows
```

---

## FIGURE 7: Two-Budget System

**Description for PaperVizAgent**:
```
Create a split-panel diagram showing the two-budget system.

LEFT PANEL - "Thinking Budget":
Background: Light blue tint #e8f0f8
Title: "NEVER COMPRESSED"
Content: "Chain-of-thought reasoning"
"Full verbosity preserved"
"Wei et al. 2022: more tokens = better reasoning"
Icon/warning: Green checkmark

RIGHT PANEL - "Output Budget":  
Background: Light teal tint #e0f4f4
Title: "COMPRESS WHERE BENEFICIAL"
Content: "Chemical formulas ✓"
"Math notation ✓"
"Pseudocode (carefully) ✓"
"Icon: ⚠️ "NOT: Python pseudocode on short descriptions"
Icon/thumb: Up thumbs for yes, down for no

BOTTOM: "Separation principle: Compressing thinking DOES NOT expand reasoning depth"

Style: Two-column comparison with clear visual separation
Title: "The Two-Budget Architecture"
Subtitle: "Thinking (free, expand) vs. Output (compress selectively)"
```

---

## FIGURE 8: P2PCLAW Network Status (External Data)

**Description for PaperVizAgent**:
```
Create an infographic-style dashboard showing P2PCLAW network status.

Four metric cards in a 2x2 grid:

CARD 1 - "Active Agents":
  Large number: 49
  Subtitle: "26 real + 23 simulated"
  Icon: Network nodes

CARD 2 - "Papers Verified":
  Large number: 249
  Subtitle: "in network"
  Icon: Document

CARD 3 - "Pending Review":
  Large number: 6
  Subtitle: "mempool"
  Icon: Queue

CARD 4 - "Top Score":
  Large number: 8.6
  Subtitle: "consensus 0.82"
  Icon: Trophy/medal

Style: Clean dashboard with subtle cards, rounded corners
Background: Gradient purple to off-white
Title: "P2PCLAW Network Status - Real API Data"
Caption: "Verified via API: April 11, 2026"
Source: "GET /swarm-status, /leaderboard, /podium endpoints"
```

---

## How to Generate These Figures

1. **Clone and setup PaperVizAgent**:
```bash
git clone https://github.com/bvalach/papervizagent.git
cd papervizagent
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

2. **Set API keys**:
```bash
# Choose one (OpenRouter is cheapest):
export OPENROUTER_API_KEY=your_key
# or
export ANTHROPIC_API_KEY=your_key
```

3. **Run the demo**:
```bash
streamlit run demo.py
```

4. **Paste each description** above into the text box and generate.

---

## Alternative: Manual Improvements

If you can't run PaperVizAgent, I can manually improve the existing Chart.js charts by:
1. Better color schemes
2. Improved annotations
3. Better legends
4. Additional data labels

Let me know if you'd like me to enhance the existing charts instead.