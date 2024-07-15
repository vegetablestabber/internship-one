from typing import Callable
import numpy as np

score_categorisers = {
    "s = -1": lambda arr: arr[arr == -1],
    "s = 0": lambda arr: arr[arr == 0],
    "0 < s < 1": lambda arr: arr[(arr > 0) & (arr < 1)],
    "s = 1": lambda arr: arr[arr == 1]
}
"""Dictionary of array modifiers to categorise similarity scores."""

SCORE_CATEGORIES = score_categorisers.keys()
"""Similarity score categories."""

def classify_scores(f: Callable, lst: list) -> dict[str, list[int | float]]:
    """Classify similarity scores.

    Args:
        f (Callable): Function to be called on the array in conjunction with a modifier function.
        lst (list): List of score arrays.

    Returns:
        dict[str, list[int | float]]: Dictionary with score categories as keys and custom outputs as values.
    """

    return {c: [f(m, arr) for arr in lst] for c, m in score_categorisers.items()}

def get_count(m: Callable, arr: np.array) -> int:
    """Get the count of filtered scores.

    Args:
        m (Callable): Modifier function to filter scores.
        arr (np.array): Array of scores.

    Returns:
        int: Number of filtered scores.
    """

    return len(m(arr))

def get_percent(m: Callable, arr: np.array) -> float:
    """Get the fraction of filtered scores.

    Args:
        m (Callable): Modifier function to filter scores.
        arr (np.array): Array of scores.

    Returns:
        float: Fraction of filtered scores.
    """

    return len(m(arr)) / len(arr)