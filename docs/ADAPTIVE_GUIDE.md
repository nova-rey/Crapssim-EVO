# Adaptive Stagnation Control

## Purpose
Monitors population health and automatically injects exploration when stagnation is detected.

## Level of Stagnation (LoS)
```text
LoS = 100 × (0.6 × (1 – ΔEF_norm) + 0.4 × (1 – diversity_norm))

    •  Low (0–30): healthy
    •  Mid (30–70): slowing improvement
    •  High (70–100): stagnant
```

## Modes

| Mode | Description | Duration |
|:--|:--|:--|
| NORMAL | Standard evolution, fine-tuning mutations | Default |
| WILDCARD | Broad mutations, hybrids, domain flips | One generation |

## Grace Handling

Wildcard offspring are tagged `trial_cohort=true` with a 2-generation grace period.

## Manifest Entries

```
"adaptive": {"mode": "WILDCARD", "los": 83.4, "trigger_reason": "stagnation"},
"grace": {"enabled": true, "grace_remaining": 2}
```

## Policy Files

- `evo/metrics/los.py`
- `evo/policy/adaptive.py`
- `evo/metrics/diversity.py`
