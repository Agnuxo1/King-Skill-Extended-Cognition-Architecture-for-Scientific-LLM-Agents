---
name: skill-18-parallel-search
description: >
  Parallelized search, optimization, and exhaustive computation using
  multiprocessing. For large parameter sweeps, SA runs, hyperparameter search,
  and any embarrassingly parallel workload.
  Triggers: "parallel", "grid search", "parameter sweep", "multiple trials",
  "hyperparameter", "exhaustive search", "multiprocessing", "concurrent".
token_savings: 5/5
dependencies: multiprocessing (stdlib), joblib, ray (optional)
---

## Core pattern: ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor
import numpy as np

def parallel_sweep(fn, param_list, workers=8):
    """Run fn(param) for all params in parallel."""
    with ProcessPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(fn, param_list))
    return results

# Example: hyperparameter search for OpenCLAW judge calibration
def evaluate_config(config):
    score = run_experiment(config)
    return {"config": config, "score": score}

configs = [{"lr": lr, "temp": t}
           for lr in [0.001, 0.01, 0.1]
           for t in [0.5, 1.0, 2.0]]

results = parallel_sweep(evaluate_config, configs, workers=8)
best = max(results, key=lambda r: r["score"])
```

## Joblib (simpler syntax)

```python
from joblib import Parallel, delayed

results = Parallel(n_jobs=-1)(  # -1 = all cores
    delayed(fn)(param) for param in param_list
)
```

## SA with multiple restarts (OpenCLAW agent tuning)

```python
def parallel_sa(objective, n_restarts=100, workers=8):
    seeds = range(n_restarts)
    def sa_run(seed):
        rng = np.random.default_rng(seed)
        state = rng.random(dim)
        # ... simulated annealing ...
        return {"state": state, "energy": objective(state)}

    results = parallel_sweep(sa_run, seeds, workers=workers)
    return min(results, key=lambda r: r["energy"])
```
