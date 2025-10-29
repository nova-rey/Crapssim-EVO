# Convergence Analysis

Phase 9 introduces deterministic rollups and trends across generations.

## What we compute (per generation)
- `ef_top1`, `ef_top5_mean`, `ef_top10_mean` (from fitness scores)
- `roi_mean`, `drawdown_mean` (if present in fitness)
- `diversity` (hash-based proxy; see Phase 8)
- `los` (from Phase 8 adaptive manifest snapshot)
- `mode` (NORMAL/WILDCARD)

## Trends (across last N generations, default 5)
- `ef_slope` (least-squares slope over `ef_top5_mean`)
- `best_plateau_len` (gens since a new best)
- `volatility` (population EF variability, as population standard deviation)

## Files we write
- `convergence.json`
- `convergence.csv`
- `operator_stats.json` (counts and normalized rates)

## Determinism
- Stable ordering (`g001 < g002 < ...`)
- No timestamps in output
- Rounding applied for floats where applicable
- Pure stdlib (no pandas/matplotlib)

_Added note:_ When `--deterministic` is used during export, convergence
artifacts are included verbatim in the stable bundle. See `PACKAGING_GUIDE.md`
for details.

## Resilience
- Missing generations are listed in `skipped`
- Missing ROI/drawdown fields do not error; they remain null

## Example
```json
{
  "schema_version": "1.0",
  "window": 5,
  "gens": [
    {"gen_id":"g004","ef_top1":1.42,"ef_top5_mean":1.31,"diversity":0.62,"los":44.2,"mode":"NORMAL"},
    {"gen_id":"g005","ef_top1":1.51,"ef_top5_mean":1.36,"diversity":0.59,"los":38.0,"mode":"WILDCARD"}
  ],
  "trends": {"ef_slope": 0.027, "best_plateau_len": 1, "volatility": 0.041}
}
```
