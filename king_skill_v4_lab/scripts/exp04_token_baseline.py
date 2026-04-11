#!/usr/bin/env python3
"""Baseline token statistics on extracted corpus (EXP-04 leg — no LLM compression)."""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def main() -> None:
    p = OUT / "corpus_paragraphs_v4.csv"
    if not p.is_file():
        print("Run exp04_extract_corpus.py first", file=sys.stderr)
        sys.exit(1)
    by_dom: dict[str, list[int]] = defaultdict(list)
    by_ct: dict[str, list[int]] = defaultdict(list)
    with p.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tok = int(row["tokens_cl100k"])
            by_dom[row["domain"]].append(tok)
            by_ct[row["content_type"]].append(tok)

    def stats(xs: list[int]) -> dict:
        if not xs:
            return {}
        import numpy as np

        a = np.array(xs)
        return {
            "n": len(a),
            "mean": float(a.mean()),
            "std": float(a.std(ddof=1)) if len(a) > 1 else 0.0,
            "median": float(np.median(a)),
            "p5": float(np.percentile(a, 5)),
            "p95": float(np.percentile(a, 95)),
        }

    report = {
        "source_csv": str(p),
        "by_domain": {k: stats(v) for k, v in sorted(by_dom.items())},
        "by_content_type": {k: stats(v) for k, v in sorted(by_ct.items())},
    }
    outp = OUT / "exp04_token_baseline_v4.json"
    outp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(outp.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
