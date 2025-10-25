from evo.metrics.los import compute_los
from evo.policy.adaptive import AdaptiveState


def test_compute_los_scales_correctly():
    los_low = compute_los([0.9, 1.0], [1.0, 1.1], 0.9)
    los_high = compute_los([1.0], [0.9], 0.2)
    assert 0 <= los_low < los_high <= 100


def test_adaptive_triggers_stagnation_and_meh_band():
    state = AdaptiveState()
    # strong stagnation
    state.update([1.0], [0.5], 0.1)
    assert state.mode == "WILDCARD" and state.last_reason == "stagnation"
    # reset
    state.update([1.0], [1.2], 0.9)
    assert state.mode == "NORMAL"
    # sustained meh plateau
    state = AdaptiveState()
    for _ in range(state.meh_limit):
        state.update([1.0], [0.95], 0.8)
    assert state.mode == "WILDCARD" and state.last_reason == "meh-plateau"


def test_snapshot_structure():
    state = AdaptiveState()
    snap = state.snapshot()
    assert {"mode", "los", "meh_counter", "trigger_reason"} <= snap.keys()
