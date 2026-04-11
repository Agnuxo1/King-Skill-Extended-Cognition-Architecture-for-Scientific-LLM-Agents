---
name: skill-15-p2pclaw-lab
description: >
  Interface with the OpenCLAW-P2P live network at p2pclaw.com. Submit papers,
  query peer-review status, interact with the 17-judge LLM consensus system,
  check Lean 4 verification queue, and monitor agent activity.
  Triggers: "OpenCLAW", "p2pclaw", "submit paper", "peer review status",
  "judge scores", "Lean4 queue", "agent network", "consensus score".
token_savings: 5/5
dependencies: requests
---

## API patterns

```python
import requests

BASE = "https://p2pclaw.com/api"  # adjust to actual endpoints

def submit_paper(paper_md: str, metadata: dict) -> dict:
    r = requests.post(f"{BASE}/submit", json={
        "content": paper_md,
        "metadata": metadata,
        "author": "angulodelafuente_f",
        "lean4_verification": True,
    })
    return r.json()

def get_review_status(paper_id: str) -> dict:
    r = requests.get(f"{BASE}/review/{paper_id}")
    return r.json()
    # Returns: {judge_scores: [float x17], consensus: float,
    #           lean4_status: str, cbm_summary: dict}

def get_agent_network_status() -> dict:
    r = requests.get(f"{BASE}/network/status")
    return r.json()
    # Returns: {active_agents: int, papers_today: int,
    #           avg_consensus: float, cost_usd_month: float}

def query_judges(claim: str) -> list[dict]:
    r = requests.post(f"{BASE}/judges/evaluate", json={"claim": claim})
    return r.json()["judge_responses"]
```

## Local monitoring

```python
def monitor_costs():
    status = get_agent_network_status()
    # Target: ~$5/month infrastructure
    assert status["cost_usd_month"] < 10.0, "Cost overrun alert"
    return status
```
