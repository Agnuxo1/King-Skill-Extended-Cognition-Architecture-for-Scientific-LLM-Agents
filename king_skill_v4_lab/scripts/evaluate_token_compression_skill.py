#!/usr/bin/env python3
"""Evaluate Token-compression.md with reproducible token and density metrics."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np
import tiktoken

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
SKILL_PATH = ROOT.parent / "Token-compression.md"
CORPUS_CSV = OUT / "corpus_paragraphs_v4.csv"
CHEM_CSV = OUT / "chemical_compression_v4.csv"

ENC = tiktoken.get_encoding("cl100k_base")

BENCHMARK_CASES = [
    {
        "id": "logic_forall",
        "domain": "logic",
        "natural": "for all x in S, property P holds",
        "compressed": "∀x ∈ S: P(x)",
    },
    {
        "id": "logic_therefore",
        "domain": "logic",
        "natural": "therefore Q because P",
        "compressed": "∵ P ∴ Q",
    },
    {
        "id": "logic_approx",
        "domain": "logic",
        "natural": "A is approximately equal to B",
        "compressed": "A ≈ B",
    },
    {
        "id": "chem_water",
        "domain": "chemistry",
        "natural": "the water molecule consists of two hydrogen atoms bonded to one oxygen atom",
        "compressed": "H₂O",
    },
    {
        "id": "chem_co2",
        "domain": "chemistry",
        "natural": "carbon dioxide gas",
        "compressed": "CO₂(g)",
    },
    {
        "id": "chem_glucose_combustion",
        "domain": "chemistry",
        "natural": "glucose combustion produces carbon dioxide and water: one molecule of glucose plus six molecules of oxygen yield six molecules of carbon dioxide plus six molecules of water",
        "compressed": "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O",
    },
    {
        "id": "chem_sodium_ion",
        "domain": "chemistry",
        "natural": "sodium ion in aqueous solution",
        "compressed": "Na⁺(aq)",
    },
    {
        "id": "chem_acetic",
        "domain": "chemistry",
        "natural": "acetic acid structure with a methyl group attached to a carboxyl group",
        "compressed": "CH₃COOH",
    },
    {
        "id": "chem_fe2o3",
        "domain": "chemistry",
        "natural": "iron(III) oxide solid",
        "compressed": "Fe₂O₃(s)",
    },
    {
        "id": "chem_h2so4",
        "domain": "chemistry",
        "natural": "sulfuric acid",
        "compressed": "H₂SO₄",
    },
    {
        "id": "chem_ethanol",
        "domain": "chemistry",
        "natural": "ethanol structure with a hydroxyl group on a two-carbon chain",
        "compressed": "CH₃-CH₂-OH (SMILES: CCO)",
    },
    {
        "id": "chem_caffeine",
        "domain": "chemistry",
        "natural": "caffeine has molecular formula C8H10N4O2 and molar mass 194.19 grams per mole",
        "compressed": "C₈H₁₀N₄O₂  M=194.19 g/mol",
    },
    {
        "id": "chem_ph",
        "domain": "chemistry",
        "natural": "pH is defined as the negative logarithm of hydrogen ion concentration",
        "compressed": "pH = -log[H⁺]",
    },
    {
        "id": "phys_ideal_gas",
        "domain": "physics",
        "natural": "the ideal gas law states that pressure times volume equals amount of substance times gas constant times temperature",
        "compressed": "PV = nRT",
    },
    {
        "id": "thermo_entropy",
        "domain": "physics",
        "natural": "entropy of an isolated system never decreases",
        "compressed": "∂S/∂t ≥ 0",
    },
    {
        "id": "chem_gibbs",
        "domain": "chemistry",
        "natural": "Gibbs free energy change equals enthalpy change minus temperature times entropy change",
        "compressed": "ΔG = ΔH - TΔS",
    },
]

REPLACEMENTS = [
    ("sodium ion in solution", "Na⁺(aq)"),
    ("glucose combustion", "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O"),
    ("water molecule", "H₂O"),
    ("carbon dioxide", "CO₂"),
    ("acetic acid structure", "CH₃COOH"),
    ("iron(iii) oxide", "Fe₂O₃"),
    ("sulfuric acid", "H₂SO₄"),
    ("ethanol structure", "CH₃-CH₂-OH (SMILES: CCO)"),
    ("ethanol", "C₂H₅OH"),
    ("caffeine", "C₈H₁₀N₄O₂"),
    ("pH definition", "pH = -log[H⁺]"),
    ("ideal gas law", "PV = nRT"),
    ("therefore", "∴"),
    ("approximately", "≈"),
    ("for all x in s", "∀x ∈ S"),
]

FILLER = [
    "as we can see",
    "it is important to note",
    "in other words",
    "basically",
    "needless to say",
    "that being said",
    "to summarize",
    "it should be noted",
    "it is worth mentioning",
    "at the end of the day",
]


def tok_len(text: str) -> int:
    return len(ENC.encode(text))


def formal_signal_density(text: str) -> float:
    matches = re.findall(r"[∀∃∴∵≈≡≤≥∝∂∇ΔΣΠΩμρβγδθηψ→⇌⇔⊂⊆∈∉⁺⁻²³₀₁₂₃₄₅₆₇₈₉=<>[\]()/|:+-]|[A-Z][a-z]?(?:[₀₁₂₃₄₅₆₇₈₉\d]+)?", text)
    return len(matches) / max(tok_len(text), 1)


def evaluate_benchmarks() -> dict:
    rows = []
    by_domain: dict[str, list[float]] = {}
    for case in BENCHMARK_CASES:
        natural = case["natural"]
        compressed = case["compressed"]
        t_nat = tok_len(natural)
        t_cmp = tok_len(compressed)
        savings = t_nat - t_cmp
        savings_pct = savings / max(t_nat, 1) * 100.0
        ratio = t_nat / max(t_cmp, 1)
        density_nat = formal_signal_density(natural)
        density_cmp = formal_signal_density(compressed)
        row = {
            **case,
            "tokens_natural": t_nat,
            "tokens_compressed": t_cmp,
            "tokens_saved": savings,
            "savings_pct": round(savings_pct, 4),
            "compression_ratio": round(ratio, 4),
            "formal_density_natural": round(density_nat, 4),
            "formal_density_compressed": round(density_cmp, 4),
            "formal_density_gain_x": round(density_cmp / density_nat, 4) if density_nat > 0 else None,
            "formal_density_delta": round(density_cmp - density_nat, 4),
        }
        rows.append(row)
        by_domain.setdefault(case["domain"], []).append(savings_pct)

    arr = np.array([r["savings_pct"] for r in rows], dtype=float)
    descriptive_cases = [r for r in rows if r["tokens_natural"] >= 7]
    positive_cases = [r for r in rows if r["tokens_saved"] > 0]
    return {
        "n_cases": len(rows),
        "cases": rows,
        "summary": {
            "mean_savings_pct": round(float(arr.mean()), 4),
            "median_savings_pct": round(float(np.median(arr)), 4),
            "min_savings_pct": round(float(arr.min()), 4),
            "max_savings_pct": round(float(arr.max()), 4),
            "mean_compression_ratio": round(float(np.mean([r["compression_ratio"] for r in rows])), 4),
            "by_domain_mean_savings_pct": {k: round(float(np.mean(v)), 4) for k, v in sorted(by_domain.items())},
            "descriptive_cases_n": len(descriptive_cases),
            "descriptive_cases_mean_savings_pct": round(float(np.mean([r["savings_pct"] for r in descriptive_cases])), 4),
            "descriptive_cases_median_savings_pct": round(float(np.median([r["savings_pct"] for r in descriptive_cases])), 4),
            "positive_cases_n": len(positive_cases),
            "positive_cases_mean_savings_pct": round(float(np.mean([r["savings_pct"] for r in positive_cases])), 4),
        },
    }


def apply_lower_bound_rules(text: str) -> tuple[str, list[str]]:
    out = text
    fired: list[str] = []
    for src, dst in sorted(REPLACEMENTS, key=lambda x: len(x[0]), reverse=True):
        pattern = re.compile(re.escape(src), flags=re.IGNORECASE)
        out2, n = pattern.subn(dst, out)
        if n:
            fired.extend([src] * n)
            out = out2
    for phrase in FILLER:
        pattern = re.compile(rf"\b{re.escape(phrase)}\b", flags=re.IGNORECASE)
        out2, n = pattern.subn("", out)
        if n:
            fired.extend([f"omit:{phrase}"] * n)
            out = out2
    if fired:
        out = re.sub(r"[ \t]{2,}", " ", out)
        out = re.sub(r"\n{3,}", "\n\n", out)
        out = out.strip()
    return out, fired


def evaluate_real_corpus_lower_bound() -> dict:
    rows_out = []
    fired_counter: Counter[str] = Counter()
    with CORPUS_CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            original = row["paragraph"]
            rewritten, fired = apply_lower_bound_rules(original)
            t0 = tok_len(original)
            t1 = tok_len(rewritten)
            if not fired:
                continue
            fired_counter.update(fired)
            rows_out.append(
                {
                    "id": row["id"],
                    "source_relpath": row["source_relpath"],
                    "domain": row["domain"],
                    "content_type": row["content_type"],
                    "tokens_original": t0,
                    "tokens_rewritten": t1,
                    "tokens_saved": t0 - t1,
                    "savings_pct": round((t0 - t1) / max(t0, 1) * 100.0, 4),
                    "rules_fired": fired,
                }
            )

    all_rows = list(csv.DictReader(CORPUS_CSV.open(encoding="utf-8")))
    total_original = sum(tok_len(r["paragraph"]) for r in all_rows)
    total_rewritten = total_original - sum(r["tokens_saved"] for r in rows_out)
    savings_pct_affected = (
        sum(r["tokens_saved"] for r in rows_out) / max(sum(r["tokens_original"] for r in rows_out), 1) * 100.0
        if rows_out
        else 0.0
    )
    savings_pct_all = (total_original - total_rewritten) / max(total_original, 1) * 100.0
    return {
        "n_paragraphs_total": len(all_rows),
        "n_paragraphs_affected": len(rows_out),
        "share_affected_pct": round(len(rows_out) / max(len(all_rows), 1) * 100.0, 4),
        "total_tokens_original_all": total_original,
        "total_tokens_rewritten_all": total_rewritten,
        "savings_pct_all_paragraphs": round(savings_pct_all, 4),
        "savings_pct_affected_paragraphs": round(savings_pct_affected, 4),
        "top_rules": fired_counter.most_common(15),
        "examples_top_saved": sorted(rows_out, key=lambda r: r["tokens_saved"], reverse=True)[:15],
    }


def evaluate_repo_occurrences() -> dict:
    text_files = []
    search_root = ROOT.parents[1]
    for path in search_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {"node_modules", ".git", "king_skill_v4_lab", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".html", ".txt"}:
            continue
        text_files.append(path)

    occurrences = []
    for path in text_files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = path.relative_to(search_root)
        lower = text.lower()
        for src, dst in REPLACEMENTS:
            start = 0
            while True:
                idx = lower.find(src.lower(), start)
                if idx == -1:
                    break
                occurrences.append(
                    {
                        "file": str(rel).replace("\\", "/"),
                        "phrase": src,
                        "replacement": dst,
                        "tokens_before": tok_len(src),
                        "tokens_after": tok_len(dst),
                        "tokens_saved": tok_len(src) - tok_len(dst),
                    }
                )
                start = idx + len(src)
        for phrase in FILLER:
            start = 0
            while True:
                idx = lower.find(phrase.lower(), start)
                if idx == -1:
                    break
                occurrences.append(
                    {
                        "file": str(rel).replace("\\", "/"),
                        "phrase": phrase,
                        "replacement": "",
                        "tokens_before": tok_len(phrase),
                        "tokens_after": 0,
                        "tokens_saved": tok_len(phrase),
                    }
                )
                start = idx + len(phrase)

    counts = Counter(o["phrase"] for o in occurrences)
    return {
        "n_occurrences": len(occurrences),
        "top_phrases": counts.most_common(20),
        "top_files": Counter(o["file"] for o in occurrences).most_common(20),
    }


def evaluate_real_chemistry() -> dict:
    rows = list(csv.DictReader(CHEM_CSV.open(encoding="utf-8")))
    paired = [r for r in rows if int(r["tokens_iupac"]) > 2 and int(r["tokens_smiles"]) > 2]
    formula_paired = [r for r in rows if int(r["tokens_iupac"]) > 2 and int(r["tokens_formula"]) > 0]

    def frac(predicate_rows: list[dict], pred) -> float:
        return sum(1 for r in predicate_rows if pred(r)) / max(len(predicate_rows), 1)

    iupac = np.array([int(r["tokens_iupac"]) for r in paired], dtype=float)
    smiles = np.array([int(r["tokens_smiles"]) for r in paired], dtype=float)
    formula = np.array([int(r["tokens_formula"]) for r in formula_paired], dtype=float)
    iupac_formula = np.array([int(r["tokens_iupac"]) for r in formula_paired], dtype=float)

    threshold_scan = []
    for min_name_tokens in range(0, 8):
        subset = [r for r in paired if int(r["name_token_count"]) >= min_name_tokens]
        if not subset:
            continue
        beneficial = sum(1 for r in subset if int(r["tokens_smiles"]) < int(r["tokens_iupac"]))
        threshold_scan.append(
            {
                "min_name_tokens": min_name_tokens,
                "n": len(subset),
                "smiles_shorter_fraction": round(beneficial / len(subset), 4),
            }
        )

    return {
        "n_rows_total": len(rows),
        "n_iupac_smiles_pairs": len(paired),
        "smiles_vs_iupac": {
            "mean_iupac_tokens": round(float(iupac.mean()), 4),
            "mean_smiles_tokens": round(float(smiles.mean()), 4),
            "median_iupac_tokens": round(float(np.median(iupac)), 4),
            "median_smiles_tokens": round(float(np.median(smiles)), 4),
            "fraction_smiles_shorter": round(frac(paired, lambda r: int(r["tokens_smiles"]) < int(r["tokens_iupac"])), 4),
        },
        "formula_vs_iupac": {
            "n_pairs": len(formula_paired),
            "mean_iupac_tokens": round(float(iupac_formula.mean()), 4),
            "mean_formula_tokens": round(float(formula.mean()), 4),
            "median_iupac_tokens": round(float(np.median(iupac_formula)), 4),
            "median_formula_tokens": round(float(np.median(formula)), 4),
            "fraction_formula_shorter": round(frac(formula_paired, lambda r: int(r["tokens_formula"]) < int(r["tokens_iupac"])), 4),
        },
        "threshold_scan": threshold_scan,
    }


def render_markdown(report: dict) -> str:
    bench = report["benchmark_examples"]["summary"]
    corpus = report["real_corpus_lower_bound"]
    chem = report["real_chemistry"]
    return "\n".join(
        [
            "# Token Compression Skill Evaluation",
            "",
            f"Skill file: `{SKILL_PATH}`",
            f"Encoding: `{report['encoding']}`",
            "",
            "## Executive Summary",
            "",
            f"- Benchmark examples extracted from the skill save a mean of `{bench['mean_savings_pct']}%` tokens with mean compression ratio `{bench['mean_compression_ratio']}x`.",
            f"- Restricting to description-bearing benchmark cases (`n={bench['descriptive_cases_n']}`), mean savings rise to `{bench['descriptive_cases_mean_savings_pct']}%`.",
            f"- On the cleaned real corpus, exact deterministic substitutions affect `{corpus['n_paragraphs_affected']}/{corpus['n_paragraphs_total']}` paragraphs (`{corpus['share_affected_pct']}%`) and save `{corpus['savings_pct_all_paragraphs']}%` across the whole corpus.",
            f"- On affected real paragraphs only, the lower-bound saving is `{corpus['savings_pct_affected_paragraphs']}%`.",
            f"- Real chemistry data (PubChem) show formulas are shorter than IUPAC in `{chem['formula_vs_iupac']['fraction_formula_shorter']*100:.2f}%` of pairs and SMILES are shorter in `{chem['smiles_vs_iupac']['fraction_smiles_shorter']*100:.2f}%` of IUPAC/SMILES pairs.",
            f"- Negative edge case: short Unicode shorthand is not universally cheaper in `cl100k_base`; use the skill mainly for description-to-formula rewrites, not blind symbol substitution.",
            "",
            "## Scientific Reasoning Interpretation",
            "",
            "- Directly measured here: token reduction and formal-signal density increase on benchmark cases.",
            "- Mechanistically plausible: shorter output frees budget for extra reasoning/tool calls and formal notation makes constraints explicit (`=`, `≤`, `→`, formulas, SMILES).",
            "- Not proven by this script: that the model becomes intrinsically better at reasoning. That requires controlled A/B runs with the same base model and task set.",
            "",
            "## Real-Corpus Caveat",
            "",
            "- The deterministic lower bound is intentionally conservative. It only counts exact phrase substitutions and filler deletion, not the full generative behavior of an LLM following the skill.",
            "- The benchmark examples are didactic sentence-level cases. They are useful for valuing the skill, but they are not a substitute for a controlled LLM A/B study.",
        ]
    ) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        "skill_path": str(SKILL_PATH),
        "encoding": "cl100k_base",
        "benchmark_examples": evaluate_benchmarks(),
        "real_corpus_lower_bound": evaluate_real_corpus_lower_bound(),
        "real_repo_occurrences": evaluate_repo_occurrences(),
        "real_chemistry": evaluate_real_chemistry(),
        "interpretation": {
            "reasoning_claim": (
                "The skill can plausibly improve scientific reasoning by reallocating saved output tokens "
                "to thinking/tool use and by expressing relations in formal notation, but this script only "
                "measures token savings and density proxies. It does not establish causal reasoning gains."
            )
        },
    }

    json_path = OUT / "token_compression_skill_evaluation.json"
    md_path = OUT / "token_compression_skill_evaluation.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "md": str(md_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
