---
name: skill-12-data-pipeline
description: >
  ETL, data cleaning, analysis, and visualization pipelines using pandas/polars.
  For OpenCLAW experiment logs, benchmark results, peer-review score analysis.
  Triggers: "analyze data", "CSV", "dataframe", "statistics", "correlation",
  "benchmark results", "experiment logs", "plot", "histogram", "regression".
token_savings: 4/5
dependencies: pandas, polars, matplotlib, seaborn, scikit-learn
---

## Core patterns

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load and inspect
df = pd.read_csv("openclaw_results.csv")
print(df.describe())
print(df.dtypes)
print(df.isnull().sum())

# OpenCLAW: analyze LLM judge scores
judge_cols = [f"judge_{i}" for i in range(17)]
df["consensus_score"] = df[judge_cols].mean(axis=1)
df["score_std"]       = df[judge_cols].std(axis=1)
df["agreement"]       = 1 - df["score_std"] / df["score_std"].max()

# Outlier detection
from scipy import stats
z_scores = np.abs(stats.zscore(df["consensus_score"]))
outliers = df[z_scores > 3]

# Correlation matrix
corr = df[judge_cols].corr()

# Export for paper
df.to_csv("cleaned_results.csv", index=False)
df.describe().to_latex("summary_stats.tex")
```

## Polars (faster for large datasets)

```python
import polars as pl
df = pl.read_csv("large_log.csv")
result = (df
    .filter(pl.col("verified") == True)
    .group_by("method")
    .agg([pl.col("score").mean().alias("avg_score"),
          pl.col("score").std().alias("std_score")])
    .sort("avg_score", descending=True))
```
