#!/usr/bin/env python3
"""
EXP-05 — real chemical token-length data from PubChem PUG REST (no API key).
Measures tiktoken cl100k_base counts for MolecularFormula, IUPACName, IsomericSMILES.
Derives exploratory threshold: beneficial if tokens(SMILES) < tokens(IUPAC).
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import requests

try:
    import tiktoken
except ImportError:
    print("pip install tiktoken", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# Deterministic CID list (diverse small molecules + drugs); verifiable via PubChem.
CIDS = (
    list(range(1, 51))
    + [2244, 3672, 3386, 5090, 5793, 6029, 6057, 3168, 3301, 4033]
    + list(range(100, 150))
    + list(range(500, 550))
    + list(range(2000, 2050))
)
# cap to 220 unique
CIDS = sorted(set(CIDS))[:220]

ENC = tiktoken.get_encoding("cl100k_base")
PROP = "MolecularFormula,MolecularWeight,IUPACName,IsomericSMILES,ConnectivitySMILES,Title"


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def fetch_batch(cids: list[int]) -> list[dict]:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{','.join(map(str, cids))}/property/{PROP}/JSON"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    data = r.json()
    props = data.get("PropertyTable", {}).get("Properties", [])
    return props


def tok(s: str | None) -> int:
    if not s:
        return 0
    return len(ENC.encode(s))


def main() -> None:
    rows = []
    for batch in chunks(CIDS, 40):
        props = fetch_batch(batch)
        for p in props:
            cid = p.get("CID")
            formula = p.get("MolecularFormula", "")
            iupac = p.get("IUPACName", "")
            smiles = (
                p.get("IsomericSMILES")
                or p.get("ConnectivitySMILES")
                or p.get("SMILES")
                or ""
            )
            mw = p.get("MolecularWeight")
            title = p.get("Title", "")
            t_form = tok(formula)
            t_iup = tok(iupac)
            t_sm = tok(smiles)
            name_tokens = len(iupac.split()) if iupac else 0
            beneficial_smiles = bool(t_sm > 2 and t_iup and t_sm < t_iup)
            context = "C_IUPAC_vs_SMILES" if (iupac and smiles and t_iup > 2 and t_sm > 2) else "A_or_B_partial"
            rows.append(
                {
                    "cid": cid,
                    "context_type": context,
                    "mw": mw,
                    "name_token_count": name_tokens,
                    "tokens_formula": t_form,
                    "tokens_iupac": t_iup,
                    "tokens_smiles": t_sm,
                    "smiles_saves_vs_iupac_pct": (
                        round((t_iup - t_sm) / max(t_iup, 1) * 100, 4) if t_iup and t_sm else ""
                    ),
                    "beneficial_smiles_vs_iupac": beneficial_smiles,
                    "title": title[:120],
                }
            )
        time.sleep(0.34)

    outp = OUT / "chemical_compression_v4.csv"
    with outp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # Threshold scan: minimal name_token_count such that majority beneficial
    with_iupac_smiles = [r for r in rows if r["tokens_iupac"] > 2 and r["tokens_smiles"] > 2]
    scan = {}
    for x in range(0, 25):
        sub = [r for r in with_iupac_smiles if r["name_token_count"] >= x]
        if not sub:
            continue
        scan[str(x)] = sum(1 for r in sub if r["beneficial_smiles_vs_iupac"]) / len(sub)

    best_x = max(scan, key=lambda k: float(scan[k])) if scan else None
    report = {
        "n_rows": len(rows),
        "pubchem_batches": len(list(chunks(CIDS, 40))),
        "beneficial_fraction_by_min_name_tokens": scan,
        "exploratory_rule": (
            f"If IUPAC name has ≥ {best_x} tokens, fraction(SMILES shorter) = {scan.get(best_x)}"
            if best_x
            else None
        ),
        "csv": str(outp),
    }
    (OUT / "chemical_compression_v4_summary.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "csv": str(outp)}, indent=2))


if __name__ == "__main__":
    main()
