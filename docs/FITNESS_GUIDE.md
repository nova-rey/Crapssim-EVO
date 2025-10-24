# Fitness & Metrics Guide

Phase 5 introduces a consistent scoring framework for evaluating strategy performance.

## Metrics Implemented
| Metric | Description |
|:--|:--|
| ROI | Return on investment `(final - start) / start`. |
| Drawdown | Largest bankroll drop from peak. |
| PSO Rate | Frequency of point–seven–out hands. |

## Fitness Formula (v1)

score = 0.5roi - 0.3(abs(drawdown)/start) + 0.2*(1 - pso_rate)

## File Output
A `fitness.json` file is written under each `/run/<seed_id>/` directory.

### Example
```json
{
  "schema_version": "1.0",
  "seed_id": "seed_0001",
  "roi": 0.54,
  "drawdown_max": -120.0,
  "pso_rate": 0.14,
  "fitness_score": 0.47
}
```

Notes
- Deterministic across identical inputs.
- CSV fallback active when report.json missing.
- No dependency on external libraries (pure stdlib).
