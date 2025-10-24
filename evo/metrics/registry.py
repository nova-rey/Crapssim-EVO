from __future__ import annotations

from typing import Callable, Dict

_METRICS: Dict[str, Callable[..., float]] = {}


def register(name: str):
    """Decorator to register a metric function."""

    def _wrap(fn: Callable[..., float]):
        _METRICS[name] = fn
        return fn

    return _wrap


def get(name: str) -> Callable[..., float]:
    return _METRICS[name]


def all_metrics() -> Dict[str, Callable[..., float]]:
    return dict(_METRICS)
