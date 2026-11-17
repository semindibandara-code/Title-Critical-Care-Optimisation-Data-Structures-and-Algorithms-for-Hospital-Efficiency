# This module compares the performance of Merge Sort and Quick Sort
# for different input sizes and conditions (random, nearly-sorted, reversed).
# It measures the execution time of each algorithm and optionally writes
# the results to a CSV file for later analysis or reporting.

import csv
import random
import time
from typing import Any, List, Tuple

# Import helper modules
from datasets import nearly_sorted     # to make "almost sorted" test cases
from helpers import make_random        # to generate random number lists
from sorting import Sorter             # our class containing merge_sort and quick_sort


#  Measure execution time of one sort function
def _time_once(fn, arr: List[Any]) -> float:
    """
    Runs a sorting function once on the provided array and returns elapsed time (in seconds).
    """
    t0 = time.perf_counter()   # start the timer
    fn(arr)                    # execute sorting function
    t1 = time.perf_counter()   # stop the timer
    return t1 - t0             # return total time taken


#  Check if array is sorted correctly
def _is_sorted(arr: List[Any]) -> bool:
    """
    Verifies that the array is sorted in ascending order.
    Returns True if sorted, False otherwise.
    """
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


# Main benchmark function

def benchmark(seed: int = 42, sizes: Tuple[int, ...] = (100, 500, 1000),
              displaced_pct: int = 10, write_csv: bool = False,
              csv_path: str = "sorting_results.csv") -> List[Tuple[str, int, str, float]]:
    """
    Benchmarks Merge Sort and Quick Sort across multiple dataset sizes and conditions.
    Parameters:
        seed          - Random seed for reproducibility
        sizes         - List of dataset sizes to test (default: 100, 500, 1000)
        displaced_pct - % of elements displaced for 'nearly sorted' test
        write_csv     - If True, writes results to a CSV file
        csv_path      - Output CSV file path

    Returns:
        List of tuples (Algorithm, N, Condition, Seconds)
    """
    rng = random.Random(seed)
    results: List[Tuple[str, int, str, float]] = []  # to store all timing results

    # Loop over each dataset size
    for n in sizes:
        base = make_random(n, rng)  # generate a random list of n numbers

        # Define three types of test inputs
        cases = {
            "random": list(base),                                   # completely random
            "nearly_sorted": nearly_sorted(sorted(base), displaced_pct, rng),  # slightly shuffled
            "reversed": list(reversed(sorted(base)))                # worst case for some sorts
        }

        # For each test condition, run both algorithms
        for cond, data in cases.items():

            # --- MERGE SORT ---
            a1 = list(data)  # make a copy so we don't reuse the same array
            t_ms = _time_once(lambda arr=a1: Sorter.merge_sort(arr), a1)
            assert _is_sorted(a1), f"MergeSort failed for n={n} cond={cond}"
            results.append(("MergeSort", n, cond, t_ms))

            # --- QUICK SORT (median-of-three) ---
            a2 = list(data)
            t_qs = _time_once(lambda arr=a2: Sorter.quick_sort(arr), a2)
            assert _is_sorted(a2), f"QuickSort failed for n={n} cond={cond}"
            results.append(("QuickSort(m3)", n, cond, t_qs))

    # Optionally save the benchmark results into a CSV file
    if write_csv:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Algorithm", "N", "Condition", "Seconds"])
            for row in results:
                w.writerow(row)

    return results



# Print the benchmark results as a formatted table

def _print_table(rows: List[Tuple[str, int, str, float]]) -> None:
    """
    Nicely formats and prints the benchmark results for easy comparison.
    Example table:
    Algorithm/Cond |  N=100   N=500   N=1000
    ----------------------------------------
    MergeSort random        0.00100  0.00560  0.01022
    QuickSort(m3) random    0.00089  0.00490  0.00998
    """
    by = {}
    # Group results by algorithm and condition
    for alg, n, cond, sec in rows:
        by.setdefault((alg, cond), []).append((n, sec))

    # Print header
    header = "Algorithm/Cond |  N=100    N=500    N=1000"
    print(header)
    print("-" * len(header))

    # Print each row of data in sorted order
    for key in sorted(by.keys()):
        alg, cond = key
        cells = {n: s for (n, s) in by[key]}
        print(f"{alg:13s} {cond:12s} "
              f"{cells.get(100, float('nan')):8.5f} "
              f"{cells.get(500, float('nan')):8.5f} "
              f"{cells.get(1000, float('nan')):8.5f}")
