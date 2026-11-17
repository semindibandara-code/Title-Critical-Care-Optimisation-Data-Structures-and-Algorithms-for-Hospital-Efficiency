# This file contains two major sorting algorithms:
#   1. Merge Sort  – stable, recursive, uses extra memory (O(n log n))
#   2. Quick Sort  – unstable, in-place, uses median-of-three pivot (O(n log n) avg)
# Both are implemented "from scratch" (no built-in sort functions)
# for your Module 4: Sorting Patient Records assignment.


from typing import Callable, List, Any, Optional


class Sorter:
   
    # MERGE SORT (Top-Down Recursive)

    @staticmethod
    def merge_sort(a: List[Any], key: Optional[Callable[[Any], Any]] = None) -> None:
        """
        Main entry point for merge sort.
        :param a: list to sort (modified in place)
        :param key: optional key function for custom sorting
        """
        if key is None:
            key = lambda x: x  # default key is the value itself
        if len(a) <= 1:        # base case: already sorted
            return
        Sorter._merge_sort_rec(a, 0, len(a) - 1, key)

    @staticmethod
    def _merge_sort_rec(a: List[Any], lo: int, hi: int, key: Callable[[Any], Any]) -> None:
        """Recursive helper that splits and merges sublists."""
        if lo < hi:
            mid = (lo + hi) // 2
            Sorter._merge_sort_rec(a, lo, mid, key)       # sort left half
            Sorter._merge_sort_rec(a, mid + 1, hi, key)   # sort right half
            Sorter._merge(a, lo, mid, hi, key)            # merge results

    @staticmethod
    def _merge(a: List[Any], lo: int, mid: int, hi: int, key: Callable[[Any], Any]) -> None:
        """
        Merges two sorted halves: [lo..mid] and [mid+1..hi].
        Stable because it uses <= to preserve equal-element order.
        """
        n = hi - lo + 1
        temp = [None] * n  # temporary array for merging
        i, j, k = lo, mid + 1, 0

        # Compare elements from both halves
        while i <= mid and j <= hi:
            if key(a[i]) <= key(a[j]):  # <= ensures STABILITY
                temp[k] = a[i]
                i += 1
            else:
                temp[k] = a[j]
                j += 1
            k += 1

        # Copy remaining elements (if any)
        while i <= mid:
            temp[k] = a[i]
            i += 1
            k += 1
        while j <= hi:
            temp[k] = a[j]
            j += 1
            k += 1

        # Copy merged elements back to original list
        for t in range(n):
            a[lo + t] = temp[t]

   
    # QUICK SORT (Median-of-Three Pivot)
    
    @staticmethod
    def quick_sort(a: List[Any], key: Optional[Callable[[Any], Any]] = None) -> None:
        """
        Main entry point for quick sort.
        Uses the median-of-three pivot strategy to reduce worst-case risk.
        """
        if key is None:
            key = lambda x: x
        if len(a) <= 1:
            return
        Sorter._qs_rec(a, 0, len(a) - 1, key)

    @staticmethod
    def _median_of_three_index(a: List[Any], i: int, j: int, k: int, key: Callable[[Any], Any]) -> int:
        """
        Returns index of the median among elements a[i], a[j], a[k].
        This helps to choose a good pivot and avoid worst-case O(n^2) behavior.
        """
        ai, aj, ak = key(a[i]), key(a[j]), key(a[k])
        if ai <= aj:
            if aj <= ak:
                return j
            else:
                return k if ai <= ak else i
        else:
            if ai <= ak:
                return i
            else:
                return k if aj <= ak else j

    @staticmethod
    def _qs_rec(a: List[Any], lo: int, hi: int, key: Callable[[Any], Any]) -> None:
        """Recursive helper for Quick Sort."""
        if hi <= lo:
            return
        mid = (lo + hi) // 2
        piv_idx = Sorter._median_of_three_index(a, lo, mid, hi, key)
        new_piv = Sorter._partition(a, lo, hi, piv_idx, key)
        Sorter._qs_rec(a, lo, new_piv - 1, key)   # sort left partition
        Sorter._qs_rec(a, new_piv + 1, hi, key)   # sort right partition

    @staticmethod
    def _partition(a: List[Any], lo: int, hi: int, piv_idx: int, key: Callable[[Any], Any]) -> int:
        """
        Partitions the list around the chosen pivot:
        - Elements < pivot go to the left
        - Elements >= pivot go to the right
        Returns the final pivot index after partitioning.
        """
        # Move pivot to the end
        a[piv_idx], a[hi] = a[hi], a[piv_idx]
        piv_val = key(a[hi])
        store = lo

        # Compare and swap
        for i in range(lo, hi):
            if key(a[i]) < piv_val:  # < (not <=) makes Quick Sort unstable
                a[i], a[store] = a[store], a[i]
                store += 1

        # Move pivot to its final position
        a[store], a[hi] = a[hi], a[store]
        return store
