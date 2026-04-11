#!/usr/bin/env python3
"""
EXP-04 (optional LLM leg) — reads corpus_paragraphs_v4.csv, calls Anthropic once per row
if ANTHROPIC_API_KEY is set, writes compression_corpus_v4.csv with before/after token counts.

Without API key: exits 0 and writes a stub manifest (honest disclosure for paper).
"""

from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def main() -> None:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    corp = OUT / "corpus_paragraphs_v4.csv"
    if not corp.is_file():
        print("Missing", corp, "— run exp04_extract_corpus.py first", file=sys.stderr)
        sys.exit(2)
    if not key:
        (OUT / "exp04_llm_compress_skipped.json").write_text(
            json.dumps({"reason": "ANTHROPIC_API_KEY unset", "instruction": "export key then re-run"}, indent=2)
            + "\n",
            encoding="utf-8",
        )
        print("Skipped LLM compression (no API key). See outputs/exp04_llm_compress_skipped.json")
        return

    import tiktoken
    from anthropic import Anthropic

    enc = tiktoken.get_encoding("cl100k_base")
    client = Anthropic()

    rows_out = []
    with corp.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 200:
                break
            natural = row["paragraph"]
            model = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
            msg = client.messages.create(
                model=model,
                max_tokens=2000,
                system=(
                    "Apply formal notation compression: replace verbose descriptions with math, "
                    "chemical formulas, and equations where appropriate. Output only the compressed text."
                ),
                messages=[{"role": "user", "content": natural}],
            )
            compressed = msg.content[0].text
            tn = len(enc.encode(natural))
            tc = len(enc.encode(compressed))
            savings = (tn - tc) / max(tn, 1) * 100.0
            rows_out.append(
                {
                    "id": row["id"],
                    "domain": row["domain"],
                    "content_type": row["content_type"],
                    "tokens_natural": tn,
                    "tokens_compressed": tc,
                    "savings_pct": round(savings, 4),
                    "natural_sha256": row["text_sha256"],
                }
            )

    outp = OUT / "compression_corpus_v4.csv"
    with outp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)
    print("Wrote", outp, "rows", len(rows_out))


if __name__ == "__main__":
    main()
