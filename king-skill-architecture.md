# King-Skill Architecture — Extended Cognition for LLM Agents
### Guía de diseño, implementación y catálogo de skills

> **Principio rector:** El LLM es el orquestador, no el ejecutor.  
> Tokens ≠ cómputo óptimo. Externalizar donde ∃ herramienta → 0 tokens de razonamiento.

---

## Índice

1. [Filosofía del sistema](#1-filosofía-del-sistema)
2. [Arquitectura general](#2-arquitectura-general)
3. [La King-Skill — diseño y protocolo](#3-la-king-skill)
4. [Formato estándar de una skill](#4-formato-estándar-de-una-skill)
5. [Catálogo de 20 skills esenciales](#5-catálogo-de-20-skills)
6. [Protocolo de instalación](#6-protocolo-de-instalación)
7. [Flujo de decisión completo](#7-flujo-de-decisión)
8. [Métricas de éxito](#8-métricas)

---

## 1. Filosofía del sistema

### El problema que resuelve

Los humanos no resuelven problemas complejos "pensando en palabras". Construyen simulaciones mentales, usan herramientas físicas, delegan subproblemas. Un matemático no calcula integrales a mano cuando tiene Mathematica. Un ingeniero no simula fluidos con papel cuando tiene ANSYS.

Un LLM que gasta 2000 tokens describiendo cómo calcular la transformada de Fourier de una señal está haciendo exactamente eso: calculando con papel.

```
paradigma_viejo:  tarea → LLM razona → output        (tokens ∝ complejidad)
paradigma_nuevo:  tarea → LLM orquesta → tools → LLM sintetiza
                                         (tokens ∝ novedad, no complejidad)
```

### La analogía correcta

No es "la calculadora que no gasta tokens". Es la **cognición extendida** (Clark & Chalmers, 1998): la mente incluye las herramientas que usa. La pizarra del matemático no es externa a su pensamiento — es parte de él.

El sistema de skills hace lo mismo: extiende la cognición del agente hacia herramientas verificadas, deterministas y especializadas.

### Regla de oro

```python
def should_delegate(task) -> bool:
    """Delegar si y solo si la herramienta produce resultado verificable."""
    return (
        task.is_deterministic()        # mismo input → mismo output
        and task.has_known_tool()      # existe skill para esto
        and not task.needs_judgment()  # no requiere razonamiento genuino
    )
    # Ejemplos DELEGAR:  primos hasta 10^6, FFT de señal, parse PDF, sort datos
    # Ejemplos RAZONAR:  estrategia de ataque para n=50, interpretación de resultados
```

---

## 2. Arquitectura general

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENTE LLM                               │
│                                                                  │
│   input → [KING-SKILL] → dispatch → [SKILL_X] → resultado      │
│                ↓                                                  │
│           síntesis + razonamiento genuino sobre el resultado     │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    bash_tool             APIs externas        MCPs
    ─────────             ─────────────        ────
    python/numpy          WolframAlpha         Gmail
    cadical SAT           arXiv API            Google Drive
    pandoc                OEIS                 P2PCLAW Lab
    sympy/scipy           NIST data            Slack
    networkx              DeepL                Asana
    lean4                 GitHub API
    ffmpeg
```

### Niveles de la jerarquía

| Nivel | Nombre | Función |
|-------|--------|---------|
| 0 | **King-Skill** | Enrutador maestro. Lee la tarea, selecciona skill(s), gestiona errores |
| 1 | **Skills de dominio** | Especializadas por área (matemáticas, código, docs, etc.) |
| 2 | **Skills atómicas** | Una sola operación (ejecutar python, fetch URL, parse PDF) |

---

## 3. La King-Skill

### Archivo: `KING-SKILL.md`

```yaml
---
name: king-skill
description: >
  Enrutador maestro. Se activa SIEMPRE como primera evaluación de cualquier
  tarea. Analiza el tipo de problema, determina si existe una skill que pueda
  resolverlo sin gastar tokens de razonamiento, y orquesta la ejecución.
  Trigger: absolutamente cualquier tarea. Sin excepciones.
priority: 0  # se ejecuta antes que cualquier otra skill
---
```

### Algoritmo de despacho

```python
def king_dispatch(task: Task) -> Response:

    # Fase 1: clasificación rápida (< 50 tokens)
    category = classify(task)
    # categorías: COMPUTE | TRANSFORM | RETRIEVE | VERIFY | GENERATE | REASON

    # Fase 2: lookup de skill
    skill = SKILL_REGISTRY.get(category, task.keywords)

    if skill is None:
        # No hay skill → razonar directamente, pero aplicar token-compression
        return reason_with_compression(task)

    # Fase 3: ejecución delegada
    try:
        result = skill.execute(task)
        # Fase 4: síntesis mínima sobre el resultado
        return synthesize(result, task.context)
    except ToolError as e:
        # Fallback: registrar el error, razonar sobre él
        return fallback_reason(task, error=e)

# Tabla de despacho primaria
DISPATCH_TABLE = {
    "numerical_computation":  "skill-python-executor",
    "sat_solving":            "skill-sat-solver",
    "document_conversion":    "skill-doc-transform",
    "literature_search":      "skill-arxiv-fetch",
    "formula_verification":   "skill-lean4-check",
    "data_lookup":            "skill-oeis-nist",
    "code_translation":       "skill-code-converter",
    "physics_simulation":     "skill-scipy-sim",
    "graph_analysis":         "skill-networkx",
    "token_compression":      "skill-token-compress",  # ← ya instalada
}
```

### Protocolo de error y fallback

```
skill.execute() → error
    │
    ├─ ToolNotAvailable  → instalar_dependencia() → reintentar
    ├─ TimeoutError      → reducir_scope() → reintentar con parámetros menores
    ├─ WrongResult       → verificar_con_segunda_herramienta()
    └─ UnknownError      → razonar_directamente() + registrar_para_mejora_skill
```

---

## 4. Formato estándar de una skill

Cada skill es un directorio con exactamente dos archivos:

```
skills/
└── skill-nombre/
    ├── SKILL.md          ← instrucciones para el LLM
    └── examples/         ← opcional: casos de uso verificados
        ├── example_01.py
        └── example_01_expected.txt
```

### Plantilla `SKILL.md`

```markdown
---
name: skill-nombre
description: >
  [Una frase que describe cuándo activar esta skill. Incluir verbos trigger.]
  Trigger words: [lista de palabras clave en español e inglés]
version: 1.0
dependencies: [lista de paquetes/herramientas necesarias]
install: [comando de instalación]
verified_envs: [python 3.11, ubuntu 24, etc.]
token_savings: [estimación: alto/medio/bajo]
---

## Cuándo usar esta skill
[Descripción precisa del dominio]

## Cuándo NO usar esta skill
[Límites explícitos]

## Instalación
[Instrucciones]

## Uso
[Código ejemplo mínimo funcional]

## Verificación
[Cómo saber que el resultado es correcto]

## Integración con King-Skill
[Cómo la King-Skill debe llamar a esta skill]
```

---

## 5. Catálogo de 20 Skills

### SKILL-01 — `skill-python-executor`
**Dominio:** Cómputo numérico general  
**Token savings:** ★★★★★ (máximo)

Ejecuta código Python arbitrario en bash_tool. Cubre numpy, scipy, sympy. Sustituye cualquier cálculo que el LLM haría "mentalmente".

```bash
# trigger: cualquier cálculo numérico, estadístico o algebraico
python3 -c "
import numpy as np
result = np.linalg.eigvals([[4,2],[1,3]])
print(result)
"
# output: [5. 2.] — 0 tokens de razonamiento usados
```

**Regla de activación:** `∃ operación aritmética/algebraica determinista → DELEGAR`

---

### SKILL-02 — `skill-sat-solver`
**Dominio:** Problemas de satisfacibilidad booleana, coloración de grafos, constraint satisfaction  
**Token savings:** ★★★★★ (crítico para P2PCLAW)

```bash
# Instalación (requiere Python ≤ 3.11)
python3.11 -m venv /tmp/sat_env
source /tmp/sat_env/bin/activate
pip install python-sat

# Uso: problema 2-coloración para Ramsey n=22
python3 solve_ramsey.py --n 22 --solver cadical
```

**Por qué es crítica:** SA heurístico con 10⁶ tokens vs CaDiCal en 50ms.  
**Regla:** `q = 2n-1 primo, q≡3 mod 4 → SAT solver, NO búsqueda local`

---

### SKILL-03 — `skill-arxiv-fetch`
**Dominio:** Búsqueda y extracción de papers científicos  
**Token savings:** ★★★★☆

```python
# Fetch directo de arXiv + extracción de resultados clave
import urllib.request, xml.etree.ElementTree as ET

def fetch_arxiv(arxiv_id: str) -> dict:
    url = f"https://export.arxiv.org/abs/{arxiv_id}"
    # web_fetch disponible en el agente
    return {"id": arxiv_id, "url": url}

# Para Wesley 2024: arxiv:2410.03625
# Resultado: construcción 2-block completa, apéndice con D-sets
```

**Regla:** `necesito información de paper → fetch primero, razonar después`

---

### SKILL-04 — `skill-oeis-lookup`
**Dominio:** Secuencias de enteros, combinatoria, teoría de números  
**Token savings:** ★★★☆☆

```bash
# Lookup OEIS API — ejemplo: secuencia de números de Ramsey R(n,n)
curl "https://oeis.org/search?q=1,2,6,18&fmt=json" | python3 -c "
import json,sys; data=json.load(sys.stdin)
print(data['results'][0]['name'] if data['results'] else 'not found')
"
```

**Regla:** `∃ secuencia entera → OEIS antes de razonar sobre patrones`

---

### SKILL-05 — `skill-lean4-verify`
**Dominio:** Verificación formal de teoremas, lógica, matemáticas  
**Token savings:** ★★★★☆ (alta calidad de verificación)

```bash
# Instalación
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
lake new verification_project

# Ejemplo: verificar propiedad de grafo circulante
theorem circulant_vertex_transitive (q : ℕ) (D : Finset ℤ) :
  ∀ v w : ZMod q, ∃ φ : Equiv.Perm (ZMod q), isGraphIso φ := by
  sorry -- SAT output → Lean proof
```

**Regla:** `resultado SAT/numérico importante → Lean4 para certificar`

---

### SKILL-06 — `skill-doc-transform`
**Dominio:** Conversión entre formatos de documento  
**Token savings:** ★★★★★

```bash
# PDF → Markdown
pandoc input.pdf -o output.md

# DOCX → Markdown
pandoc input.docx -o output.md --extract-media=./media

# LaTeX → PDF
pdflatex paper.tex

# HTML → PDF
weasyprint page.html output.pdf
```

**Regla:** `conversión de documento → pandoc/herramienta, NUNCA reescribir manualmente`

---

### SKILL-07 — `skill-scipy-simulation`
**Dominio:** Simulación de sistemas físicos, EDOs, optimización numérica  
**Token savings:** ★★★★★

```python
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import numpy as np

# Ejemplo: simular sistema termodinámico (relevante para P2PCLAW + física)
def system(t, y, k):
    return [-k * y[0], k * y[0] - k * y[1]]

sol = solve_ivp(system, [0, 10], [1, 0], args=(0.5,), dense_output=True)
# Resultado en ms, no tokens
```

**Regla:** `∃ EDO / sistema dinámico → scipy.integrate, no razonar la trayectoria`

---

### SKILL-08 — `skill-networkx-graphs`
**Dominio:** Análisis y manipulación de grafos  
**Token savings:** ★★★★★ (crítico para teoría de Ramsey)

```python
import networkx as nx

# Verificar propiedad de Book Graph B_n
def verify_book_graph(G: nx.Graph, n: int) -> bool:
    # B_n = n triángulos compartiendo una arista común
    # Buscar K_2 (arista base) + n triángulos
    for u, v in G.edges():
        common = list(nx.common_neighbors(G, u, v))
        if len(common) >= n:
            return True
    return False

# Verificar coloración 2-block circulante para n=25
# Resultado: verificado en <1s vs 500 tokens de razonamiento verbal
```

**Regla:** `propiedad de grafo → networkx, no describir la estructura verbalmente`

---

### SKILL-09 — `skill-sympy-algebra`
**Dominio:** Álgebra simbólica, cuerpos finitos, teoría de números  
**Token savings:** ★★★★☆

```python
from sympy import *
from sympy.polys.galoistools import gf_irreducible_p

# Verificar que q = p^k es potencia de primo
def is_prime_power(q):
    for p in primerange(2, q+1):
        k = 1
        while p**k <= q:
            if p**k == q: return True, p, k
            k += 1
    return False, None, None

# Construir GF(p^k) para extensiones de campo
# Ejemplo: GF(3^4) para n=41
p, k = 3, 4
print(GF(p**k))  # campo finito con 81 elementos
```

**Regla:** `∃ cálculo en cuerpo finito / factorización → sympy, no calcular a mano`

---

### SKILL-10 — `skill-code-translator`
**Dominio:** Traducción entre lenguajes de programación  
**Token savings:** ★★★☆☆

Usa el propio LLM pero con un prompt ultra-comprimido + verificación automática de que el output compila y produce el mismo resultado.

```python
# Protocolo:
# 1. Recibir código fuente en lenguaje A
# 2. Generar código en lenguaje B (mínimo de tokens)
# 3. Ejecutar ambos con mismo input → verificar output idéntico
# 4. Si divergen → corregir (no regenerar desde cero)

# Ejemplo: Python SAT solver → Rust para velocidad
# Input:  python pysat solution (verified)
# Output: equivalent Rust + cargo test passing
```

**Regla:** `traducción de código donde ∃ test de corrección → traducir + verificar automáticamente`

---

### SKILL-11 — `skill-latex-renderer`
**Dominio:** Generación de documentos matemáticos formales  
**Token savings:** ★★★☆☆

```bash
# Generar paper con notación matemática densa
cat > paper.tex << 'EOF'
\documentclass{article}
\usepackage{amsmath,amssymb}
\begin{document}
\section{2-Block Circulant Construction}
Let $q = 2n-1$ be a prime power, $q \equiv 1 \pmod{4}$.
Define $Q \subset \mathbb{Z}_q$ as the set of quadratic residues...
\end{document}
EOF
pdflatex paper.tex
# Output: PDF con notación correcta, sin gastar tokens en formateo
```

---

### SKILL-12 — `skill-data-pipeline`
**Dominio:** ETL, transformación y limpieza de datos  
**Token savings:** ★★★★☆

```python
import pandas as pd

# En lugar de describir la transformación token a token:
df = pd.read_csv("results.csv")
summary = df.groupby("n")["penalty"].agg(["min","mean","count"])
summary.to_markdown("summary.md")
# Resultado: tabla lista en 3 líneas, no 300 tokens describiendo la estructura
```

---

### SKILL-13 — `skill-wolfram-query`
**Dominio:** Matemáticas avanzadas con respaldo de Wolfram  
**Token savings:** ★★★★☆

```bash
# WolframAlpha API (free tier: 2000 queries/mes)
curl "https://api.wolframalpha.com/v1/result?i=R(3,3)&appid=YOUR_KEY"
# Output: "6" — número de Ramsey en milisegundos

# Para consultas más complejas: SimpleAPI
curl "https://api.wolframalpha.com/v1/spoken?i=eigenvalues+of+[[4,2],[1,3]]&appid=KEY"
```

**Regla:** `∃ resultado matemático conocido → Wolfram, no derivar desde primeros principios`

---

### SKILL-14 — `skill-git-operations`
**Dominio:** Control de versiones, gestión de código  
**Token savings:** ★★★☆☆

```bash
# Operaciones git sin describir el estado verbalmente
git log --oneline -10          # historia compacta
git diff HEAD~1 --stat         # cambios resumidos
git stash list                 # estado del stash

# Para el agente P2PCLAW: commit automático de resultados verificados
git add results/n_${N}_verified.json
git commit -m "feat: n=${N} solved, penalty=0, method=cadical"
```

---

### SKILL-15 — `skill-p2pclaw-lab`
**Dominio:** Integración directa con P2PCLAW Lab API  
**Token savings:** ★★★★★ (específica del proyecto)

```python
# Wrapper para todas las operaciones del Lab
import requests

BASE = "https://lab.p2pclaw.com"

def submit_experiment(params: dict, token: str) -> dict:
    r = requests.post(f"{BASE}/experiments", json=params,
                      headers={"Authorization": f"Bearer {token}"})
    return r.json()

def poll_result(exp_id: str, token: str, timeout=300) -> dict:
    import time
    for _ in range(timeout):
        r = requests.get(f"{BASE}/experiments/{exp_id}", 
                         headers={"Authorization": f"Bearer {token}"})
        data = r.json()
        if data["status"] in ["completed", "failed"]:
            return data
        time.sleep(1)

# En lugar de describir el experimento en 200 tokens → submit + poll
```

---

### SKILL-16 — `skill-token-compression`
**Dominio:** Optimización de output del LLM  
**Token savings:** ★★★☆☆ (meta-skill)

> ⚠️ **Ya instalada.** Ver `token-compression/SKILL.md`.

Activar siempre en output. Separación estricta: thinking libre, output comprimido.

---

### SKILL-17 — `skill-benchmark-verifier`
**Dominio:** Verificación automática de soluciones contra benchmarks conocidos  
**Token savings:** ★★★★☆

```python
# Para FrontierMath: verifier oficial cuando esté disponible
# Por ahora: verificación interna contra valores conocidos

KNOWN_SOLUTIONS = {
    25: {"maxR": 23, "maxB": 24},   # warm-up verificado
    41: {"maxR": 39, "maxB": 40},   # GF(3^4)
    63: {"maxR": 61, "maxB": 62},   # GF(5^3)
}

def verify_solution(n: int, coloring: dict) -> bool:
    if n in KNOWN_SOLUTIONS:
        expected = KNOWN_SOLUTIONS[n]
        actual_maxR = compute_max_clique(coloring, "red")
        actual_maxB = compute_max_clique(coloring, "blue")
        return (actual_maxR == expected["maxR"] and 
                actual_maxB == expected["maxB"])
    # Para n desconocido: verificación desde definición
    return verify_from_definition(n, coloring)
```

---

### SKILL-18 — `skill-parallel-search`
**Dominio:** Búsqueda exhaustiva paralelizada  
**Token savings:** ★★★★★

```python
from concurrent.futures import ProcessPoolExecutor
import itertools

def parallel_dset_search(q: int, target_size: int, 
                          workers: int = 8) -> list:
    """
    Busca D-sets válidos para construcción 2-block.
    Paraleliza sobre múltiples puntos de inicio SA.
    Sustituye 'lanzar 1000 trials SA secuencialmente'.
    """
    with ProcessPoolExecutor(max_workers=workers) as ex:
        seeds = range(workers * 100)
        results = list(ex.map(
            lambda seed: sa_search(q, target_size, seed=seed),
            seeds
        ))
    return [r for r in results if r["penalty"] == 0]

# Ejemplo: n=22, q=43 → lanzar 800 búsquedas en paralelo
# Tiempo: ~30s vs días de tokens de reasoning secuencial
```

---

### SKILL-19 — `skill-knowledge-cache`
**Dominio:** Caché de resultados verificados para evitar recomputar  
**Token savings:** ★★★★☆

```python
import json, hashlib, os

CACHE_DIR = "/tmp/p2pclaw_cache"

def cache_result(key: str, value: dict) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    h = hashlib.sha256(key.encode()).hexdigest()[:16]
    with open(f"{CACHE_DIR}/{h}.json", "w") as f:
        json.dump({"key": key, "value": value}, f)

def get_cached(key: str) -> dict | None:
    h = hashlib.sha256(key.encode()).hexdigest()[:16]
    path = f"{CACHE_DIR}/{h}.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)["value"]
    return None

# Uso: antes de atacar n=X, verificar si ya está en caché
result = get_cached(f"ramsey_n={n}_q={q}")
if result: return result  # 0 tokens
else: compute_and_cache(n, q)  # solo si necesario
```

---

### SKILL-20 — `skill-report-generator`
**Dominio:** Generación automática de reportes científicos  
**Token savings:** ★★★☆☆

```python
# Genera paper P2PCLAW-compatible desde resultados verificados
def generate_paper(results: dict, template: str = "ramsey") -> str:
    """
    Input:  dict con {n: {solved: bool, method: str, verified: bool}}
    Output: Markdown con estructura paper P2PCLAW
    Proceso: template + datos → pandoc → PDF
    """
    coverage = sum(1 for r in results.values() if r["solved"])
    total = len(results)
    
    md = f"""# 2-Block Circulant Construction for Ramsey Book Graphs
    
## Abstract
We present verified solutions for {coverage}/{total} values of n ≤ 100...

## Results
| n | q | method | verified |
|---|---|--------|----------|
"""
    for n, r in sorted(results.items()):
        status = "✓" if r["solved"] else "✗"
        md += f"| {n} | {2*n-1} | {r['method']} | {status} |\n"
    
    return md

# Output directo a paper.md → pandoc → P2PCLAW submission
```

---

## 6. Protocolo de instalación

### Paso 1: Estructura de directorios

```bash
mkdir -p ~/.claude/skills/{king-skill,skill-python-executor,skill-sat-solver,...}
```

### Paso 2: Instalar King-Skill

```bash
# Copiar KING-SKILL.md al directorio de skills del agente
cp king-skill/SKILL.md ~/.claude/skills/king-skill/SKILL.md

# Verificar que el agente la lee en el contexto de sistema
echo "✓ King-Skill instalada"
```

### Paso 3: Instalar dependencias base

```bash
# Python 3.11 para SAT solvers
sudo apt-get install python3.11 python3.11-venv -y  # Ubuntu
brew install python@3.11                             # macOS

# Entorno SAT
python3.11 -m venv /opt/p2pclaw_env
source /opt/p2pclaw_env/bin/activate
pip install python-sat networkx sympy scipy numpy pandas

# Herramientas de documento
sudo apt-get install pandoc texlive-latex-base -y

# Verificar
python3 -c "from pysat.solvers import Cadical153; print('✓ SAT solver listo')"
```

### Paso 4: Verificar integración

```python
# test_king_skill.py
tasks = [
    "calcula los primeros 100 números primos",         # → skill-python-executor
    "resuelve n=22 para Ramsey book graphs",           # → skill-sat-solver
    "convierte este PDF a markdown",                    # → skill-doc-transform
    "¿qué dice el paper arXiv:2410.03625?",            # → skill-arxiv-fetch
    "diseña la estrategia para n=50",                  # → RAZONAR (no hay tool)
]
# Los primeros 4 deben delegar. El último debe razonar.
# Si los primeros 4 gastan >100 tokens: King-Skill no está funcionando.
```

---

## 7. Flujo de decisión

```
TAREA RECIBIDA
      │
      ▼
¿Es determinista y ∃ tool?
      │
    SÍ │                    NO
      │                      │
      ▼                      ▼
DELEGAR a skill        ¿Requiere datos externos?
      │                      │
      ▼                    SÍ │              NO
resultado verificado         │               │
      │                      ▼               ▼
      ▼                 fetch/API      razonar con
sintetizar                  │           token-compression
(mínimos tokens)            ▼
                       datos → razonar
                       con compression
```

---

## 8. Métricas de éxito

```python
metrics = {
    # Objetivo principal
    "token_reduction":        "> 60% vs baseline sin skills",
    "reasoning_quality":      "≥ baseline (no degradación)",

    # Por skill
    "delegation_rate":        "> 80% de tareas deterministas",
    "tool_success_rate":      "> 95% (con fallback)",
    "cache_hit_rate":         "> 40% en sesiones largas",

    # Para P2PCLAW específicamente
    "n_solved_per_hour":      "objetivo: 5 valores/hora con SAT",
    "verification_coverage":  "objetivo: 100/100 valores n ≤ 100",
}

# Señal de alarma: si el agente gasta > 500 tokens describiendo
# un cálculo que python podría hacer en 3 líneas → King-Skill fallando
```

---

## Apéndice: Tabla resumen de skills

| # | Skill | Dominio | Token savings | Crítica para P2PCLAW |
|---|-------|---------|--------------|----------------------|
| 01 | python-executor | Cómputo numérico | ★★★★★ | ✓ |
| 02 | sat-solver | SAT / coloración grafos | ★★★★★ | ✓ ← urgente |
| 03 | arxiv-fetch | Literatura científica | ★★★★☆ | ✓ |
| 04 | oeis-lookup | Secuencias enteras | ★★★☆☆ | ✓ |
| 05 | lean4-verify | Verificación formal | ★★★★☆ | △ |
| 06 | doc-transform | Conversión documentos | ★★★★★ | △ |
| 07 | scipy-simulation | Simulación física | ★★★★★ | △ |
| 08 | networkx-graphs | Análisis de grafos | ★★★★★ | ✓ |
| 09 | sympy-algebra | Álgebra simbólica | ★★★★☆ | ✓ |
| 10 | code-translator | Traducción de código | ★★★☆☆ | △ |
| 11 | latex-renderer | Documentos formales | ★★★☆☆ | ✓ |
| 12 | data-pipeline | ETL / análisis datos | ★★★★☆ | △ |
| 13 | wolfram-query | Matemáticas avanzadas | ★★★★☆ | ✓ |
| 14 | git-operations | Control de versiones | ★★★☆☆ | △ |
| 15 | p2pclaw-lab | API P2PCLAW | ★★★★★ | ✓ |
| 16 | token-compression | Optimización output | ★★★☆☆ | ✓ (instalada) |
| 17 | benchmark-verifier | Verificación automática | ★★★★☆ | ✓ |
| 18 | parallel-search | Búsqueda paralela | ★★★★★ | ✓ ← urgente |
| 19 | knowledge-cache | Caché de resultados | ★★★★☆ | ✓ |
| 20 | report-generator | Papers automáticos | ★★★☆☆ | ✓ |

---

*v1.0 — Diseñado para agentes P2PCLAW y uso científico general*  
*Principio: el LLM razona sobre lo nuevo. Las herramientas ejecutan lo conocido.*
