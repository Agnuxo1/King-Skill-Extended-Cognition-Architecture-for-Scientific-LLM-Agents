"""
Simple evaluation of King-Skill and skills bundle.
"""

import json
import re
from pathlib import Path

SKILLS_DIR = Path("E:/OpenCLAW-4/papers/Skills")
OUTPUT_DIR = SKILLS_DIR / "outputs"


def simple_token_count(text: str) -> int:
    return len(text.split())


def extract_metadata(content: str) -> dict:
    meta = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
    return meta


def analyze(path: Path) -> dict:
    content = path.read_text(encoding="utf-8", errors="ignore")
    meta = extract_metadata(content)
    return {
        "path": str(path),
        "tokens": simple_token_count(content),
        "lines": len(content.splitlines()),
        "name": meta.get("name", path.stem),
        "savings": meta.get("token_savings", "N/A"),
    }


def main():
    print("=" * 60)
    print("SKILLS EVALUATION")
    print("=" * 60)

    results = {"king": None, "skills": [], "summary": {}}

    # King-Skill
    king_path = SKILLS_DIR / "king-skill" / "SKILL.md"
    if king_path.exists():
        king = analyze(king_path)
        results["king"] = king
        print(f"\nKing-Skill: {king['tokens']} tokens")

    # Skills bundle
    bundle = SKILLS_DIR / "skills-bundle"
    files = sorted(bundle.glob("skill-*/SKILL*.md"))
    files = [f for f in files if "token-compression" not in str(f)]

    total = 0
    ratings = {}

    print(f"\n{len(files)} Skills:")
    for f in files:
        s = analyze(f)
        results["skills"].append(s)
        total += s["tokens"]
        r = s["savings"]
        r_clean = r.replace("*", "").replace("/", "") if r else "N/A"
        if r_clean not in ratings:
            ratings[r_clean] = 0
        ratings[r_clean] += 1
        print(f"  {s['name']}: {s['tokens']} tokens")

    print(f"\nTotal: {total} tokens")
    print(f"Avg: {total // len(files)} per skill")
    print(f"Skills by rating category: {len(ratings)} types")

    results["summary"] = {
        "total": len(files),
        "total_tokens": total,
        "avg": total // len(files),
        "ratings": ratings,
    }

    OUTPUT_DIR.mkdir(exist_ok=True)

    out_json = OUTPUT_DIR / "all_skills_eval.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved: {out_json}")
    return 0


if __name__ == "__main__":
    exit(main())
