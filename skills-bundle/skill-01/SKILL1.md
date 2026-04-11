---
name: skill-01-python-executor
description: >
  Execute any deterministic numerical, statistical, algebraic or signal-processing
  computation via bash_tool + Python. ALWAYS use instead of reasoning through math.
  Triggers: "calculate", "compute", "eigenvalues", "FFT", "integral", "matrix",
  "statistics", "fit", "interpolate", "solve equation", "optimize numerically".
token_savings: ★★★★★
verified: true
tested_env: Python 3.12, numpy, scipy, sympy
---

## Critical imports (verified correct)

```python
import numpy as np
from scipy.integrate import quad, solve_ivp    # NOT: from scipy import quad
from scipy.linalg import eig, inv, det
from scipy.optimize import minimize, curve_fit
from scipy import signal
import sympy as sp
from sympy import symbols, integrate, diff, solve, Matrix, exp, sin, oo, latex
```

## Verified patterns

```python
# Eigenvalues
A = np.array([[4,2],[1,3]])
evals = np.linalg.eigvals(A)          # → [2. 5.]

# Definite integral
result, err = quad(lambda x: np.sin(x)**2, 0, np.pi)   # → 1.5707... = π/2

# Optimization
res = minimize(lambda x: (x[0]-1)**2 + (x[1]-2)**2, [0,0])  # → [1,2]

# FFT — find dominant frequency
t = np.linspace(0, 1, 1000)
sig = np.sin(2*np.pi*50*t)
freqs = np.fft.fftfreq(len(t), t[1]-t[0])
peak_freq = abs(freqs[np.argmax(np.abs(np.fft.fft(sig))[:500])])  # → 50 Hz

# Sympy symbolic integration
x = sp.Symbol('x')
sp.integrate(x**2 * sp.exp(-x), (x, 0, sp.oo))   # → 2

# ODE solve
sol = solve_ivp(lambda t,y: [-y[0]], [0,10], [1.0], method='RK45', rtol=1e-8)
```

## Verification
```python
assert np.allclose(result, expected, rtol=1e-6)
assert sol.success
```
