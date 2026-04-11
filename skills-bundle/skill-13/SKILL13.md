---
name: skill-13-wolfram-query
description: >
  Query WolframAlpha for advanced mathematics, physics, chemistry, and
  scientific computations. Use when sympy/scipy are insufficient.
  Triggers: "WolframAlpha", "advanced math", "closed form", "definite integral
  symbolic", "number theory", "prime factorization", "special functions".
token_savings: 4/5
dependencies: requests (WolframAlpha API key needed) OR wolframalpha pip
---

## Setup

```bash
pip install wolframalpha --break-system-packages
# Free API key: https://developer.wolframalpha.com
# Store in env: export WOLFRAM_APP_ID="your_key"
```

## Pattern

```python
import wolframalpha, os

client = wolframalpha.Client(os.environ["WOLFRAM_APP_ID"])

def wolfram_query(query: str) -> str:
    res = client.query(query)
    pods = list(res.pods)
    results = []
    for pod in pods:
        if pod.title in ["Result", "Exact result", "Solution"]:
            results.append(f"{pod.title}: {next(pod.texts)}")
    return "\n".join(results) or str(next(res.results).text)

# Examples:
wolfram_query("integrate sin(x)^2 * cos(x) from 0 to pi")
wolfram_query("eigenvalues of {{4,2},{1,3}}")
wolfram_query("is 982451653 prime")
wolfram_query("Riemann zeta(3) closed form")
```

## Free alternative: Sympy first, Wolfram as fallback

```python
def compute(query_sympy, query_wolfram_fallback):
    try:
        from sympy import *
        return eval(query_sympy)
    except:
        return wolfram_query(query_wolfram_fallback)
```
