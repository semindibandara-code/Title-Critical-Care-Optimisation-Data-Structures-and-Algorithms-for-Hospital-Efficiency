# This file provides helper functions to generate test datasets
# for sorting algorithms (Module 4: Sorting Patient Records).
# The data is created in three styles:
#   1. Random order
#   2. Nearly sorted (some values swapped)
#   3. Reversed order




# RNG CLASS (Simple Random Number Generator)

class RNG:
    def __init__(self, seed=12345):
        """
        Initialize the random number generator with a fixed seed.
        A fixed seed ensures that we always get the same "random"
        results every time (important for reproducible testing).
        """
        self.state = seed

    def next_int(self):
        """
        Generate the next pseudo-random integer using a
        Linear Congruential Generator (LCG) formula:
            Xn+1 = (a * Xn + c) mod m
        """
        self.state = (1103515245 * self.state + 12345) % (1 << 31)
        return self.state

    def next_range(self, lo, hi):
        """
        Generate a random number between lo and hi (inclusive).
        """
        n = self.next_int()
        return lo + (n % (hi - lo + 1))



# NEARLY SORTED DATA GENERATOR

def nearly_sorted(base, displaced_pct=10):
    """
    Return a copy of the input list where up to 'displaced_pct'% of
    elements are swapped with *nearby* positions.
    This simulates a "nearly sorted" list for benchmarking purposes.

    For example:
        Input: [1, 2, 3, 4, 5]
        Output (10% displaced): [1, 3, 2, 4, 5] or similar

    Parameters:
        base (list): Input list (usually already sorted)
        displaced_pct (int): Percentage of items to swap

    Returns:
        A new list with small local swaps (slightly unsorted)
    """
    if not base:
        return []

    out = list(base)           # make a copy so we don’t modify the original
    rng = RNG(12345)           # create deterministic RNG with fixed seed
    n = len(out)
    swaps = (n * displaced_pct) // 100  # number of elements to swap
    c = 0

    # Perform the swaps
    while c < swaps:
        # Pick a random index i
        i = rng.next_range(0, n - 1)

        # Pick a nearby index j (within ±5 range)
        delta = rng.next_range(1, 5)
        j = i + (-delta if rng.next_range(0, 1) == 0 else delta)

        # Keep j within valid list bounds
        if j < 0:
            j = 0
        if j >= n:
            j = n - 1

        # Swap the two elements
        out[i], out[j] = out[j], out[i]
        c += 1

    return out
