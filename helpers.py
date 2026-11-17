# MODULE 4: Helper Functions for Sorting Experiments

# This module provides small utility functions to generate
# random, reversed, and nearly-sorted numeric datasets.

# These are used by the benchmarking script (Module 4) to test
# Merge Sort and Quick Sort performance under different conditions.


import math
import random
from typing import List



# FUNCTION: make_random

def make_random(n: int, rng: random.Random) -> List[float]:
    """
    Generates a list of 'n' random floating-point numbers.
    Each number is between 5.0 and 240.0 (representing, for example,
    patient treatment durations in minutes).

    Args:
        n (int): number of elements to generate
        rng (random.Random): random number generator instance
                             (used for reproducibility)
    Returns:
        List[float]: list of random numbers (rounded to 3 decimals)
    """
    return [round(rng.uniform(5.0, 240.0), 3) for _ in range(n)]



# FUNCTION: make_reversed

def make_reversed(n: int, rng: random.Random) -> List[float]:
    """
    Creates a reversed (descending) list of 'n' random numbers.
    Useful for testing worst-case scenarios in sorting algorithms,
    such as Quick Sort with poor pivot selection.

    Args:
        n (int): number of elements
        rng (random.Random): random generator
    Returns:
        List[float]: reversed (descending) list
    """
    arr = make_random(n, rng)  # start with random numbers
    arr.sort()                 # sort ascending
    arr.reverse()              # then reverse to descending
    return arr



# FUNCTION: nearly_sorted

def nearly_sorted(base: List[float], displaced_pct: float, rng: random.Random) -> List[float]:
    """
    Returns a modified version of a sorted list where a small
    percentage of elements are displaced (swapped with nearby
    elements). This simulates a "nearly sorted" dataset,
    which is common in real-world situations.

    Args:
        base (List[float]): sorted input list
        displaced_pct (float): percentage of elements to move (0–100)
        rng (random.Random): deterministic RNG for reproducibility

    Returns:
        List[float]: slightly shuffled version of 'base'
    """
    if not base:
        return []

    a = list(base)                     # make a safe copy
    n = len(a)

    # Number of elements to be displaced (at least 1)
    k = max(1, int(math.floor(n * displaced_pct / 100.0)))

    # Defines how far each swap may move an element (local window)
    window = max(1, n // 10)

    for _ in range(k):
        idx = rng.randrange(0, n)                     # random index
        delta = rng.randrange(-window, window + 1)    # nearby offset
        j = min(n - 1, max(0, idx + delta))           # keep within range
        a[idx], a[j] = a[j], a[idx]                   # swap positions

    return a
