---
name: skill-07-scipy-sim
description: >
  Scientific simulation using scipy, numpy, and open-source simulators.
  Covers ODEs, PDEs, thermodynamics, signal processing, fluid dynamics (basic),
  quantum mechanics (qutip), circuit simulation (PySpice).
  NEVER simulate physics by reasoning — delegate to this skill.
  Triggers: "simulate", "ODE", "differential equation", "thermodynamic",
  "physics simulation", "heat equation", "oscillator", "reservoir computing".
token_savings: 5/5
dependencies: scipy, numpy, qutip, matplotlib
---

## ODE / dynamical systems

```python
from scipy.integrate import solve_ivp
import numpy as np

# Lorenz attractor (chaotic system)
def lorenz(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    return [sigma*(y-x), x*(rho-z)-y, x*y-beta*z]

sol = solve_ivp(lorenz, [0, 50], [1,1,1],
                method='RK45', rtol=1e-9, dense_output=True)
```

## Thermodynamic reservoir computing (CHIMERA context)

```python
# Model ASIC thermal dynamics as reservoir
def thermal_reservoir(t, T, P_in, k_cool, T_amb=25.0):
    """dT/dt = P_in/C - k_cool*(T - T_amb)"""
    C = 50.0  # thermal capacity J/K
    return P_in/C - k_cool*(T - T_amb)

sol = solve_ivp(thermal_reservoir, [0, 100], [T0],
                args=(P_in, k_cool), method='Radau')
```

## Signal processing

```python
from scipy import signal

# Design bandpass filter
b, a = signal.butter(N=4, Wn=[f_low, f_high], btype='band', fs=sample_rate)
filtered = signal.filtfilt(b, a, raw_signal)

# Spectrogram
f, t, Sxx = signal.spectrogram(data, fs=sample_rate)
```

## Quantum simulation (QuTiP)

```bash
pip install qutip --break-system-packages
```

```python
import qutip as qt
# Two-level system (qubit)
H = qt.sigmax()
psi0 = qt.basis(2, 0)
times = np.linspace(0, 10, 100)
result = qt.sesolve(H, psi0, times)
```

## Open-source external simulators (local install)

```
OpenFOAM:   CFD fluid dynamics    → sudo apt install openfoam
Elmer FEM:  multiphysics FEM      → sudo apt install elmerfem
QUCS:       circuit simulation    → sudo apt install qucs
Ngspice:    SPICE circuits        → sudo apt install ngspice
Scilab:     MATLAB alternative    → sudo apt install scilab
```
