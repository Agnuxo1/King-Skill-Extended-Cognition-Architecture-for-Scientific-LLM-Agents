---
name: skill-19-knowledge-cache
description: >
  Cache verified results to avoid recomputation. Check BEFORE any computation.
  Triggers: "cache", "already computed", "store result", "memoize",
  "have we done this before", "save for later", "reuse result".
token_savings: ★★★★☆
verified: true
dependencies: json, hashlib (stdlib only)
---

## Verified implementation (Python 3.12 compatible)

```python
import json, hashlib, os
from datetime import datetime, timezone   # use timezone.utc, NOT utcnow()

CACHE_DIR = '/tmp/openclaw_cache'

def _key(query: str) -> str:
    return hashlib.sha256(query.encode()).hexdigest()[:16]

def cache_set(query: str, result, metadata: dict = {}) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    entry = {
        'query':     query,
        'result':    result,
        'timestamp': datetime.now(timezone.utc).isoformat(),  # ← correct API
        'verified':  metadata.get('verified', False),
        **metadata,
    }
    path = f'{CACHE_DIR}/{_key(query)}.json'
    with open(path, 'w') as f:
        json.dump(entry, f, indent=2)
    return path

def cache_get(query: str):
    path = f'{CACHE_DIR}/{_key(query)}.json'
    if os.path.exists(path):
        with open(path) as f: return json.load(f)
    return None

def cache_list() -> list:
    if not os.path.exists(CACHE_DIR): return []
    return [json.load(open(f'{CACHE_DIR}/{f}'))
            for f in os.listdir(CACHE_DIR) if f.endswith('.json')]

def smart_compute(query: str, compute_fn):
    """Check cache first. Call compute_fn only on miss."""
    cached = cache_get(query)
    if cached:
        return cached['result'], True    # (result, from_cache=True)
    result = compute_fn(query)
    cache_set(query, result, {'verified': True})
    return result, False

# Usage pattern:
# result, from_cache = smart_compute('eigenvals_A', lambda _: np.linalg.eigvals(A).tolist())
# if from_cache: print('0 tokens, 0 compute')
```
