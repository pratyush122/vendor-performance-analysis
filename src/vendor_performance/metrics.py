from __future__ import annotations

from typing import Iterable

import numpy as np
from scipy import stats


def confidence_interval(values: Iterable[float], confidence: float = 0.95) -> tuple[float, float, float]:
    array = np.asarray([value for value in values if np.isfinite(value)], dtype=float)
    if array.size == 0:
        return (float("nan"), float("nan"), float("nan"))
    mean_value = float(np.mean(array))
    if array.size == 1:
        return (mean_value, mean_value, mean_value)
    standard_error = stats.sem(array)
    interval = stats.t.interval(confidence, len(array) - 1, loc=mean_value, scale=standard_error)
    return (mean_value, float(interval[0]), float(interval[1]))


def format_currency(value: float) -> str:
    absolute_value = abs(value)
    if absolute_value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if absolute_value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if absolute_value >= 1_000:
        return f"${value / 1_000:.2f}K"
    return f"${value:.2f}"


def herfindahl_hirschman_index(shares: Iterable[float]) -> float:
    share_array = np.asarray(list(shares), dtype=float)
    if share_array.size == 0:
        return float("nan")
    normalized = share_array / share_array.sum()
    return float(np.square(normalized).sum())
