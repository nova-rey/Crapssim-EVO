# Adaptive Stagnation Control

## Purpose
Monitors population health and automatically injects exploration when stagnation is detected.

## Level of Stagnation (LoS)

LoS = 100 × (0.6 × ΔEF_norm + 0.4 × (1 − diversity_norm))
where ΔEF_norm = clamp((prev_mean − curr_mean) / max(|prev_mean|, |curr_mean|, ε) × S, 0, 1)
and diversity_norm ∈ [0, 1]

- **Low (0–30):** healthy
- **Mid (30–70):** slowing improvement
- **High (70–100):** stagnant

**Implementation note:** We use a scaling constant `S = LOS_DELTA_SCALE = 16` to keep LoS
responsive to small EF changes. The calculation is pure stdlib; no NumPy dependency.

## Modes
| Mode | Description | Duration |
|:--|:--|:--|
| NORMAL | Standard evolution, fine-tuning mutations | Default |
| WILDCARD | Broad mutations, hybrids, domain flips | One generation |

## Grace Handling
Wildcard offspring are tagged `trial_cohort=true` with a 2-generation grace period.

## Manifest Entries
```json
"adaptive": {"mode": "WILDCARD", "los": 83.4, "trigger_reason": "stagnation"},
"grace": {"enabled": true, "grace_remaining": 2}
```

## Diversity
Current diversity proxy is hash-based on spec shape/content (fast, coarse). Future work may add a
Hamming/Euclidean mix over parameter vectors for finer signal.

## Policy Files
- `evo/metrics/los.py`
- `evo/policy/adaptive.py`
- `evo/metrics/diversity.py`
