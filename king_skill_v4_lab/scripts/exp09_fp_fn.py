#!/usr/bin/env python3
"""EXP-09 — confusion matrix + per-label precision/recall (reference router vs labels)."""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from keyword_router import route_task  # noqa: E402

DATA = ROOT / "data"
OUT = ROOT / "outputs"


def main() -> None:
    tasks = json.loads((DATA / "routing_tasks_v4_500.json").read_text(encoding="utf-8"))
    labels = sorted({t["expected_skill"] for t in tasks} | {route_task(t["input"]) for t in tasks})
    C = defaultdict(lambda: defaultdict(int))
    for t in tasks:
        exp = t["expected_skill"]
        pred = route_task(t["input"])
        C[exp][pred] += 1

    per_label = []
    for lab in labels:
        tp = C[lab][lab]
        support = sum(C[lab][p] for p in labels)
        predicted = sum(C[e][lab] for e in labels)
        precision = tp / predicted if predicted else 0.0
        recall = tp / support if support else 0.0
        per_label.append(
            {
                "label": lab,
                "support": support,
                "predicted_as": predicted,
                "precision": round(precision, 5),
                "recall": round(recall, 5),
            }
        )

    outp = OUT / "routing_confusion_v4.csv"
    OUT.mkdir(parents=True, exist_ok=True)
    with outp.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["expected\\predicted"] + labels)
        for e in labels:
            w.writerow([e] + [C[e][p] for p in labels])

    rep = {
        "n_tasks": len(tasks),
        "labels": labels,
        "per_label": per_label,
        "csv": str(outp),
        "disclaimer": "Metrics are for keyword_router vs synthetic stratified labels (EXP-08 protocol).",
    }
    (OUT / "routing_fp_fn_v4.json").write_text(json.dumps(rep, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(outp), "rows": len(tasks)}, indent=2))


if __name__ == "__main__":
    main()
