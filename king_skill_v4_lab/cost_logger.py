"""EXP-06 / EXP-17 / EXP-18 — minimal cost + latency logger (real runs append JSONL)."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class CallRecord:
    ts: float
    skill: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_usd: float
    model: str


class CostLogger:
    """Wrap API responses; caller supplies usage dict-like Anthropic/OpenAI."""

    def __init__(self, log_path: Path | None = None):
        self.records: list[CallRecord] = []
        self._t0: float | None = None
        self.log_path = log_path

    def start(self) -> None:
        self._t0 = time.perf_counter()

    def _elapsed_ms(self) -> float:
        if self._t0 is None:
            return 0.0
        return (time.perf_counter() - self._t0) * 1000.0

    def log_call(
        self,
        *,
        skill_id: str,
        usage: Any,
        cost_usd: float,
        model: str = "",
    ) -> None:
        inp = int(getattr(usage, "input_tokens", None) or usage.get("input_tokens", 0))
        outp = int(getattr(usage, "output_tokens", None) or usage.get("output_tokens", 0))
        rec = CallRecord(
            ts=time.time(),
            skill=skill_id,
            input_tokens=inp,
            output_tokens=outp,
            latency_ms=self._elapsed_ms(),
            cost_usd=cost_usd,
            model=model,
        )
        self.records.append(rec)
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(rec), ensure_ascii=False) + "\n")

    def summary(self) -> dict[str, float]:
        if not self.records:
            return {"calls": 0}
        return {
            "calls": len(self.records),
            "total_input_tokens": sum(r.input_tokens for r in self.records),
            "total_output_tokens": sum(r.output_tokens for r in self.records),
            "total_cost_usd": round(sum(r.cost_usd for r in self.records), 6),
            "total_latency_ms": round(sum(r.latency_ms for r in self.records), 3),
        }
