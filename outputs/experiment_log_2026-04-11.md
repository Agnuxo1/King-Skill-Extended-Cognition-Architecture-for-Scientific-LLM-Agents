# Experiment Log - 2026-04-11

## Skills Evaluated Today

### 1. token_compression_skill (previously)
- Token savings: 15.80% average (26.31% for description→formula cases)
- Chemical compression: 96.65% where formula < IUPAC name
- Verdict: Good for domain-specific rewriting, savings vary by use case

### 2. frontier_math_solver (this evaluation)
- **Token cost**: 11,349 tokens (cl100k_base)
- **Overhead**: +8,849 tokens vs simple math (+354%)
- **External APIs**: 0/5 accessible
- **Local tools**: 6/6 available
- **Math verification**: Code present and structurally correct
- **Verdict**: MAXIMIZES rigor at cost of context; NOT a token-saving skill

## Real Data Collected

| Metric | frontier_math_solver |
|--------|-----------------|
| Total tokens | 11,349 |
| Thinking ratio | 18.9% |
| Problems in registry | 15 |
| Tool availability | 100% (local) |
| External API availability | 0% |
| Cost overhead | +354% |

## Pending for Honest Paper

1. A/B comparison with baseline (OSF preregistration)
2. 17-judge panel evaluation
3. Krippendorff's alpha reliability
4. Real production cost tracking

## Files

- `outputs/frontier_math_solver_evaluation.json`
- `outputs/frontier_math_solver_evaluation.md`