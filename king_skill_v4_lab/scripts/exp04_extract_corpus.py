#!/usr/bin/env python3
"""
EXP-04 — extract ≥200 real paragraphs from P2PCLAW/OpenCLAW paper drafts under repo papers/.
Outputs verifiable paths + SHA-256 of text. Compression pairs require exp04_llm_compress.py + API key.
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

try:
    import tiktoken
except ImportError:
    tiktoken = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# papers/ directory (parent of Skills/)
PAPERS_DIR = Path(__file__).resolve().parents[3]

SKIP_DIR_PARTS = {"node_modules", ".git", "king_skill_v4_lab", ".venv", "dist", "build"}


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def classify_domain(text: str) -> str:
    t = text.lower()
    rules = [
        ("thermodynamics", ("entropy", "enthalpy", "gibbs", "helmholtz", "carnot", "heat capacity")),
        ("quantum_mechanics", ("hamiltonian", "qubit", "schrodinger", "hilbert", "unitary", "density matrix")),
        ("distributed_systems", ("p2p", "byzantine", "consensus", "quorum", "replication", "raft", "gossip")),
        ("machine_learning", ("neural", "gradient", "transformer", "loss function", "backprop", "dataset")),
        ("synthetic_biology", ("gene", "crispr", "protein", "plasmid", "rna", "cell culture")),
    ]
    scores = {name: sum(1 for k in keys if k in t) for name, keys in rules}
    best = max(scores.values())
    if best == 0:
        return "mixed_unclassified"
    return max(scores, key=scores.get)


def classify_content(text: str) -> str:
    if text.count("$") >= 4 or "∫" in text or "∑" in text or "\\(" in text:
        return "equation_heavy"
    if "→" in text or re.search(r"\b(yields|reaction|mol)\b", text.lower()):
        return "reaction_heavy"
    if len(text) > 1200:
        return "prose_heavy"
    return "mixed"


def looks_like_embedded_binary_payload(text: str) -> bool:
    t = text.strip()
    if "data:image/" in t or ";base64," in t:
        return True
    if re.match(r"^\[image\d+\]:\s*<data:image/", t, flags=re.IGNORECASE):
        return True
    # Guard against huge encoded blobs with very little whitespace.
    longest_run = max((len(x) for x in re.findall(r"[A-Za-z0-9+/=]{256,}", t)), default=0)
    if longest_run >= 2048:
        return True
    return False


def iter_markdown_files():
    for p in PAPERS_DIR.rglob("*.md"):
        if any(part in SKIP_DIR_PARTS for part in p.parts):
            continue
        try:
            if p.stat().st_size > 2_000_000:
                continue
        except OSError:
            continue
        yield p


def paragraphs_from_text(text: str) -> list[str]:
    parts = re.split(r"\n\s*\n+", text)
    out = []
    for raw in parts:
        s = raw.strip()
        if len(s) < 220:
            continue
        if s.startswith("```"):
            continue
        out.append(s)
    return out


def main() -> None:
    rows = []
    skipped_binary_payloads = 0
    enc = tiktoken.get_encoding("cl100k_base") if tiktoken else None
    for path in sorted(iter_markdown_files(), key=lambda x: str(x)):
        rel = path.relative_to(PAPERS_DIR)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for para in paragraphs_from_text(text):
            if looks_like_embedded_binary_payload(para):
                skipped_binary_payloads += 1
                continue
            rid = sha256(para)[:16]
            domain = classify_domain(para)
            ctype = classify_content(para)
            tok = len(enc.encode(para)) if enc else -1
            rows.append(
                {
                    "id": rid,
                    "source_relpath": str(rel).replace("\\", "/"),
                    "domain": domain,
                    "content_type": ctype,
                    "char_len": len(para),
                    "tokens_cl100k": tok,
                    "text_sha256": sha256(para),
                    "paragraph": para[:8000],
                }
            )
            if len(rows) >= 320:
                break
        if len(rows) >= 320:
            break

    outp = OUT / "corpus_paragraphs_v4.csv"
    with outp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            w.writeheader()
            w.writerows(rows)

    summary = OUT / "exp04_corpus_summary.json"
    import json

    summary.write_text(
        json.dumps(
            {
                "papers_root": str(PAPERS_DIR),
                "paragraph_count": len(rows),
                "meets_n200": len(rows) >= 200,
                "skipped_binary_payloads": skipped_binary_payloads,
                "output_csv": str(outp),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"paragraphs": len(rows), "csv": str(outp)}, indent=2))
    if len(rows) < 200:
        sys.exit(1)


if __name__ == "__main__":
    main()
