"""
Evaluation of Token-compression.md skill
Measures token savings from compression substitutions.
"""

import json
import re
from pathlib import Path

SKILL_FILE = Path("E:/OpenCLAW-4/papers/Skills/Token-compression.md")
OUTPUT_DIR = Path("E:/OpenCLAW-4/papers/Skills/outputs")


def simple_token_count(text: str) -> int:
    return len(text.split())


def main():
    print("=" * 60)
    print("TOKEN-COMPRESSION SKILL EVALUATION")
    print("=" * 60)

    content = SKILL_FILE.read_text(encoding="utf-8", errors="ignore")

    results = {
        "file": str(SKILL_FILE),
        "tokens": simple_token_count(content),
        "lines": len(content.splitlines()),
    }

    print(f"\n[1] BASIC STATS")
    print(f"  Total tokens: {results['tokens']}")
    print(f"  Lines: {results['lines']}")

    # Count arsenals
    print(f"\n[2] ARSENALS")
    arsenals = [
        "ARSENAL 1",
        "ARSENAL 2",
        "ARSENAL 3",
        "ARSENAL 4",
        "ARSENAL 5",
        "ARSENAL 6",
        "ARSENAL 7",
    ]
    for a in arsenals:
        count = content.count(a)
        print(f"  {a}: {count}")

    # Count substitutions in reference table
    print(f"\n[3] REFERENCE TABLE")
    table_matches = re.findall(r"\|.*?\|.*?\|.*?\|", content)
    print(f"  Quick substitution entries: {len(table_matches)}")

    # Count examples: chemistry reactions
    print(f"\n[4] CHEMISTRY EXAMPLES")
    chem_examples = re.findall(r'"([^"]+)"[^\n]*→[^\n]*"', content)
    print(f"  Reaction examples: {len(chem_examples)}")

    # Extract measured savings from the file
    print(f"\n[5] MEASURED SAVINGS (from skill)")
    measured = re.findall(r"\[([~]?[\d.]+)×\]", content)
    if measured:
        values = [float(m.replace("~", "")) for m in measured]
        avg = sum(values) / len(values)
        print(f"  Measured ratios: {values}")
        print(f"  Average: {avg:.1f}x reduction")
        print(f"  Range: {min(values):.1f}x - {max(values):.1f}x")
        results["measured_savings"] = {
            "average": avg,
            "min": min(values),
            "max": max(values),
            "count": len(values),
        }

    # Extract constants
    print(f"\n[6] CONSTANTS (CODATA 2022)")
    constants = re.findall(r"(\w+)\s*=\s*[\d.e×⁻⁺]+", content)
    print(f"  Physical constants: {len(constants)}")

    # Extract element substitutions
    print(f"\n[7] ELEMENT SUBSTITUTIONS")
    elem_subs = re.findall(r'"(\w+)"[^\w]+(\w+)', content)
    unique_elems = set([e[1] for e in elem_subs if len(e[1]) <= 2])
    print(f"  Element symbols: {len(unique_elems)}")

    print(f"\n[8] CORE PRINCIPLE")
    print(f"  Two budgets: thinking (free) vs output (compress)")
    print(f"  Target reduction: 3-6x [ESTIMATE]")

    # Save
    OUTPUT_DIR.mkdir(exist_ok=True)
    out_json = OUTPUT_DIR / "token_compression_eval.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out_json}")

    return 0


if __name__ == "__main__":
    exit(main())
