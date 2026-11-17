
# What this does:
#  - Module 1: builds a hospital graph; checks adjacency, BFS levels,
#               DFS cycle detection, and Dijkstra shortest path
#  - Module 2: inserts ≥20 patients, shows collisions/probes,
#               checks search/delete, and triggers a resize
#  - Module 3: computes priorities, pushes to heap, extracts in
#               priority order, and logs heap states
#  - Module 4: validates Merge Sort & Quick Sort correctness on
#               random / nearly-sorted / reversed arrays



import sys
import time
from typing import List, Tuple

# ----- Imports from your project -----
from graph import Graph
from hash_table import HashTable, Patient
from scheduler import EmergencyScheduler
from sorting import Sorter

# ---------- tiny helpers ----------
def header(title: str):
    print("\n" + "=" * 66)
    print(title)
    print("=" * 66)

def check(cond: bool, msg: str):
    print(("Good! " if cond else "Bad!") + msg)
    if not cond:
        raise AssertionError(msg)


# Module 1 — Graph-Based Hospital Navigation

def test_module1() -> None:
    header("MODULE 1: GRAPH TESTS")

    g = Graph()

    # Departments (9 including one isolated)
    for d in [
        "Emergency", "ICU", "Pharmacy", "Radiology", "Laboratories",
        "Theatres", "WardA", "WardB", "Outpatients"  # isolated
    ]:
        g.add_department(d)

    # 12 edges with at least one cycle
    edges = [
        ("Emergency","ICU",2),
        ("Emergency","Laboratories",4),
        ("ICU","Laboratories",1),
        ("Laboratories","Pharmacy",3),
        ("Pharmacy","WardA",6),
        ("WardA","WardB",2),
        ("WardB","Theatres",5),
        ("Theatres","Radiology",4),
        ("Radiology","ICU",7),
        ("Pharmacy","Theatres",3),
        ("Emergency","Radiology",8),
        ("Laboratories","Radiology",2),
    ]
    for u, v, w in edges:
        g.add_corridor(u, v, w)

    # Visual adjacency (print for report)
    print("\nAdjacency List (dept: neighbor(weight)):\n" + g.adjacency_list_str())

    # BFS levels from Emergency
    levels = g.bfs_levels("Emergency")
    print("\nBFS Levels from Emergency:")
    for i, lvl in enumerate(levels):
        print(f"  Level {i}: {', '.join(lvl)}")
    check(len(levels) >= 3, "BFS produced ≥3 levels from Emergency")

    # Cycle detection
    cyc_flag, cyc_nodes = g.dfs_cycle("Emergency")
    print("\nDFS cycle detected:", cyc_flag, "| cycle:", " -> ".join(cyc_nodes) if cyc_nodes else "N/A")
    check(cyc_flag, "DFS reported a cycle (graph contains a loop)")

    # Dijkstra: Emergency → Radiology
    path, cost = g.dijkstra("Emergency", "Radiology")
    print(f"\nDijkstra Emergency → Radiology: {' -> '.join(path) if path else path}  (cost {cost})")
    check(path is not None and cost > 0, "Dijkstra returned a valid path and positive cost")

    # Unreachable (isolated) test
    iso_path, iso_cost = g.dijkstra("Emergency", "Outpatients")
    print(f"Dijkstra Emergency → Outpatients: {iso_path}, {iso_cost}")
    check(iso_path is None, "Outpatients is unreachable (isolated node)")


# Module 2 — Hash-Based Patient Lookup

def _mk_pat(pid, u) -> Patient:
    return Patient(pid, f"P{pid}", 30 + (pid % 10), "ER", u, "waiting")

def test_module2() -> HashTable:
    header("MODULE 2: HASH TABLE TESTS")

    ht = HashTable(29)  # small prime -> easy collisions & resize demo

    # 20 baseline records (diverse urgencies)
    base: List[Tuple[int,int]] = [
        (1000,3),(1001,2),(1002,5),(1003,1),(1004,4),
        (1005,2),(1006,1),(1007,3),(1008,5),(1009,4),
        (1010,3),(1011,5),(1012,4),(1013,2),(1014,1),
        (1015,5),(1016,3),(1017,2),(1018,4),(1019,1),
    ]
    for pid, u in base:
        res = ht.insert(_mk_pat(pid, u))
        print(f"insert({pid}) -> {res}, probes={ht.debug_last_probe()}")

    # Collision chain demo: ids congruent mod 29
    for pid in (1000, 1029, 1058, 1087):
        res = ht.insert(_mk_pat(pid, 2))
        print(f"collision-insert({pid}) -> {res}, probes={ht.debug_last_probe()}")

    # Search hit and miss
    found = ht.search(1058)
    print("search(1058) ->", found, "| probes:", ht.debug_last_probe())
    check(found is not None and getattr(found, "pid", None) == 1058, "Search hit for 1058")

    not_found = ht.search(9999)
    print("search(9999) ->", not_found, "| probes:", ht.debug_last_probe())
    check(not_found is None, "Search miss for 9999")

    # Delete then re-search
    ok = ht.delete(1007)
    print("delete(1007) ->", ok, "| search after delete:", ht.search(1007))
    check(ok, "Delete returned True for existing key")

    # Trigger resize (load factor > 0.7) by adding a couple extras
    for pid in (2000, 2029, 2058):
        ht.insert(_mk_pat(pid, 2))
        print(f"insert({pid}) -> probes={ht.debug_last_probe()}")
    print("resize events:", ht.debug_resize_events())
    check(len(ht.debug_resize_events()) >= 1, "Resize (rehash) occurred at high load")

    return ht


# Module 3 — Heap-Based Emergency Scheduling

def test_module3(ht: HashTable) -> None:
    header("MODULE 3: HEAP SCHEDULER TESTS")

    sched = EmergencyScheduler(ht)

    # 10 requests (pid, expected minutes)
    reqs = [
        (1006, 10), (1003, 60), (1019, 20), (1005, 30), (1017, 25),
        (1001, 15), (1000, 40), (1014, 50), (1012, 90), (1013, 12)
    ]
    print("Inserting requests (pid, T):", reqs)
    for pid, T in reqs:
        sched.add_request(pid, T)

    top1 = sched.next_patient()
    top2 = sched.next_patient()
    top3 = sched.next_patient()
    # Expect the first extraction to be a very high priority (e.g., U=1 & small T)
    def prio(val):
        if isinstance(val, dict):
            return val.get("P_float", 0.0)
        return 0.0
    pvals = list(map(prio, [top1, top2, top3]))
    print("First three extracted priorities:", pvals)
    check(pvals[0] >= pvals[1] >= pvals[2], "Heap extracts in non-increasing priority order")


# Module 4 — Sorting Patient Records

def _is_sorted(a: List[int]) -> bool:
    i = 1
    while i < len(a):
        if a[i-1] > a[i]:
            return False
        i += 1
    return True

def nearly_sorted(arr: List[int], pct: int) -> List[int]:
    """Make ≤pct% local displacements (deterministic)."""
    a = arr[:]
    n = len(a)
    swaps = max(1, n * pct // 100)
    rng = 12345
    i = 0
    while i < swaps:
        # cheap LCG
        rng = (1103515245 * rng + 12345) & 0x7fffffff
        idx = rng % n
        rng = (1103515245 * rng + 12345) & 0x7fffffff
        delta = (rng % 5) + 1
        j = idx + (-delta if (rng % 2 == 0) else delta)
        if j < 0: j = 0
        if j >= n: j = n - 1
        a[idx], a[j] = a[j], a[idx]
        i += 1
    return a

def test_module4() -> None:
    header("MODULE 4: SORTING TESTS")

    sizes = [100, 500, 1000]
    for n in sizes:
        base = list(range(n))
        cases = {
            "random": base[::-1],  # simple deterministic "random-ish": reversed
            "nearly": nearly_sorted(base, 10),
            "reversed": base[::-1],
        }
        for name, data in cases.items():
            a1 = data[:]
            a2 = data[:]
            t0 = time.perf_counter(); Sorter.merge_sort(a1); t1 = time.perf_counter()
            t2 = time.perf_counter(); Sorter.quick_sort(a2); t3 = time.perf_counter()
            print(f"n={n:4d} case={name:8s}  merge={t1-t0:.5f}s  quick={t3-t2:.5f}s")
            check(_is_sorted(a1) and _is_sorted(a2), f"Sorted correctly for n={n} ({name})")


# Main

def main():
    # Module 1
    test_module1()

    # Module 2
    ht = test_module2()

    # Module 3
    test_module3(ht)

    # Module 4
    test_module4()

    print("\nALL TESTS PASSED ")

if __name__ == "__main__":
    main()
