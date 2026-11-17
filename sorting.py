# Module 4: Sorting Patient Records

# This module compares two sorting algorithms — Merge Sort and Quick Sort.
# Both are implemented from scratch (no built-in sort functions).
#
# The dataset can represent patient treatment durations or similar values.
# Sorting is tested under three conditions:
#   1. Random order
#   2. Nearly sorted (10% displaced)
#   3. Reversed order
#
# Performance (execution time) is measured for array sizes 100, 500, and 1000.


import random
import time


class Sorter:
    """Contains static implementations of Merge Sort and Quick Sort."""

    
    # MERGE SORT (Top-Down, Stable)
    
    @staticmethod
    def merge_sort(a):
        """
        Performs a top-down (recursive) merge sort on the list 'a'.
        Merge sort is a stable, O(n log n) algorithm that divides
        the list into halves, sorts each, and merges them.
        """

        # Helper function to merge two sorted halves
        def _merge(arr, lo, mid, hi, tmp):
            i, j, k = lo, mid + 1, 0
            # Merge smaller elements first while both halves have data
            while i <= mid and j <= hi:
                if arr[i] <= arr[j]:  # <= keeps stability (stable sort)
                    tmp[k] = arr[i]
                    i += 1
                else:
                    tmp[k] = arr[j]
                    j += 1
                k += 1

            # Copy any remaining items from the left half
            while i <= mid:
                tmp[k] = arr[i]
                i += 1
                k += 1

            # Copy any remaining items from the right half
            while j <= hi:
                tmp[k] = arr[j]
                j += 1
                k += 1

            # Copy merged data back into the main array
            t = 0
            p = lo
            while p <= hi:
                arr[p] = tmp[t]
                p += 1
                t += 1

        # Recursive helper to split the array
        def _sort(arr, lo, hi, tmp):
            if lo >= hi:
                return
            mid = (lo + hi) // 2
            _sort(arr, lo, mid, tmp)       # Sort left half
            _sort(arr, mid + 1, hi, tmp)   # Sort right half
            _merge(arr, lo, mid, hi, tmp)  # Merge them

        if a is None:
            return a

        tmp = [None] * len(a)  # Temporary list for merging
        _sort(a, 0, len(a) - 1, tmp)
        return a

   
    # QUICK SORT (Median-of-Three Pivot)
    

    @staticmethod
    def quick_sort(a):
        """
        In-place Quick Sort with median-of-three pivot and a small
        insertion-sort cutoff to guarantee correctness on tiny partitions.
        """

        def insertion_sort(arr, lo, hi):
            i = lo + 1
            while i <= hi:
                x = arr[i]
                j = i - 1
                while j >= lo and arr[j] > x:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = x
                i += 1

        def median3(arr, lo, hi):
            mid = (lo + hi) // 2
            if arr[mid] < arr[lo]:
                arr[lo], arr[mid] = arr[mid], arr[lo]
            if arr[hi] < arr[lo]:
                arr[lo], arr[hi] = arr[hi], arr[lo]
            if arr[hi] < arr[mid]:
                arr[mid], arr[hi] = arr[hi], arr[mid]
            # pivot to hi-1
            arr[mid], arr[hi - 1] = arr[hi - 1], arr[mid]
            return arr[hi - 1]

        def partition(arr, lo, hi):
            pv = median3(arr, lo, hi)
            i = lo
            j = hi - 1
            # classic two-finger scan
            i += 1
            while arr[i] < pv:
                i += 1
            j -= 1
            while pv < arr[j]:
                j -= 1
            done = False
            while not done:
                if i >= j:
                    done = True
                else:
                    arr[i], arr[j] = arr[j], arr[i]
                    i += 1
                    while arr[i] < pv:
                        i += 1
                    j -= 1
                    while pv < arr[j]:
                        j -= 1
            # place pivot
            arr[i], arr[hi - 1] = arr[hi - 1], arr[i]
            return i

        def qsort(arr, lo, hi):
            while lo < hi:
                # handle small partitions with insertion sort
                if hi - lo <= 10:
                    insertion_sort(arr, lo, hi)
                    return
                p = partition(arr, lo, hi)
                # recurse on smaller side first (tail-call elimination)
                if p - 1 - lo < hi - (p + 1):
                    qsort(arr, lo, p - 1)
                    lo = p + 1
                else:
                    qsort(arr, p + 1, hi)
                    hi = p - 1

        if a is None or len(a) < 2:
            return a
        qsort(a, 0, len(a) - 1)
        return a



# Benchmark function

def benchmark():
    """
    Compares Merge Sort and Quick Sort for different dataset sizes
    (100, 500, 1000) and conditions (random, nearly sorted, reversed).
    Returns a list of tuples:
      (AlgorithmName, Size, Condition, ExecutionTime)
    """

    sizes = [100, 500, 1000]
    conditions = ["random", "nearly_sorted", "reversed"]
    results = []

    for size in sizes:
        base = list(range(size))  # base dataset: 0..N-1

        for cond in conditions:
          
            # Generate test data according to condition
            
            if cond == "random":
                data = base[:]
                random.shuffle(data)

            elif cond == "nearly_sorted":
                data = base[:]
                swaps = max(1, size // 10)  # 10% displacement
                for _ in range(swaps):
                    i, j = random.sample(range(size), 2)
                    data[i], data[j] = data[j], data[i]

            elif cond == "reversed":
                data = base[::-1]

            
            # Run both algorithms on the same data
           
            for alg_name, func in [
                ("MergeSort", Sorter.merge_sort),
                ("QuickSort", Sorter.quick_sort),
            ]:
                arr = list(data)  # make a copy to keep input same
                t0 = time.perf_counter()
                func(arr)
                t1 = time.perf_counter()
                elapsed = t1 - t0
                results.append((alg_name, size, cond, elapsed))

                print(
                    f"{alg_name:<10} | Size={size:4d} | {cond:<14} | Time={elapsed*1000:.3f} ms"
                )

    return results



# Example usage (for standalone testing)

if __name__ == "__main__":
    print("Running Module 4: Sorting Benchmark...\n")
    results = benchmark()
    print("\nSummary:")
    for row in results:
        print(row)
