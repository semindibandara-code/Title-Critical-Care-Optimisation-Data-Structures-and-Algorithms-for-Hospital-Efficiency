# Demonstrates all four modules:
#   Module 1 – Graph-Based Hospital Navigation
#   Module 2 – Hash-Based Patient Lookup
#   Module 3 – Heap-Based Emergency Scheduling
#   Module 4 – Sorting Patient Records (performance test)
#
# Each section runs automatically and prints readable outputs that


from typing import Hashable
from EmergencyScheduler import EmergencyScheduler
from datasets import RNG, nearly_sorted
from graph import Graph
from sorting import Sorter
from hash_table import HashTable, Patient



# MODULE 1 – GRAPH DEMO

def demo_graph():
    """
    Builds the hospital floor-plan as a weighted undirected graph
    and demonstrates:
      1. Adjacency list + matrix (visual graph)
      2. BFS levels
      3. DFS cycle detection
      4. Dijkstra shortest path
      5. Behaviour of isolated department
    """
    g = Graph()

    # Step 1: Add departments (≥8, including one isolated)
    for d in [
        "Emergency", "ICU", "Pharmacy", "Radiology", "Laboratories",
        "Theatres", "WardA", "WardB", "Outpatients"   # Outpatients is isolated
    ]:
        g.add_department(d)

    # Step 2: Add 10–12 corridors (edges) including at least one cycle
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

    #  Expected Output 1: Textual / Visual graph structure 
    print("Adjacency List (dept: neighbor(weight)):\n" + g.adjacency_list_str())

    # Optional adjacency matrix view
    labels = sorted(g._adj.keys())
    header = "  " + " ".join(labels)
    rows = [header]
    for r in labels:
        cells = []
        for c in labels:
            cells.append("1" if any(n == c for (n, _w) in g._adj[r]) else "0")
        rows.append(f"{r:<12s} " + " ".join(cells))
    print("\nAdjacency Matrix:\n" + "\n".join(rows))

    #  Expected Output 2: BFS level grouping 
    levels = g.bfs_levels("Emergency")
    for i, lvl in enumerate(levels):
        print(f"Level {i}: {', '.join(lvl)}")

    # Expected Output 3: DFS cycle detection 
    has_cycle, cyc = g.dfs_cycle("Emergency")
    print("Cycle detected:", has_cycle)
    if has_cycle:
        print("Cycle nodes:", " -> ".join(cyc))

    #  Expected Output 4: Shortest path (Dijkstra) 
    path, cost = g.dijkstra("Emergency", "Radiology")
    print("Shortest Emergency → Radiology:", " -> ".join(path), f"({cost} minutes)")

    # Demonstrate isolated department behaviour
    iso_levels = g.bfs_levels("Outpatients")
    print("BFS from Outpatients (isolated):", iso_levels)
    iso_path, iso_cost = g.dijkstra("Emergency", "Outpatients")
    print("Shortest Emergency → Outpatients:", iso_path, iso_cost)



# MODULE 2 – HASH TABLE DEMO

def demo_hash_table(ht: HashTable):
    """
    Inserts ≥20 patient records to demonstrate:
      • collisions and probe sequences
      • duplicate updates
      • search hits and misses
      • deletion and resizing (rehash)
    """
    sample = [
        (1000,"P1000",31,"ER",3,"waiting"), (1001,"P1001",22,"ICU",2,"waiting"),
        (1002,"P1002",28,"Lab",5,"waiting"), (1003,"P1003",24,"Ward",1,"waiting"),
        (1004,"P1004",26,"Pharm",4,"waiting"), (1005,"P1005",33,"ER",2,"waiting"),
        (1006,"P1006",41,"ICU",1,"waiting"), (1007,"P1007",19,"Ward",3,"waiting"),
        (1008,"P1008",45,"Theatre",5,"waiting"), (1009,"P1009",38,"ER",4,"waiting"),
        (1029,"P1029",30,"ER",2,"waiting"), (1058,"P1058",27,"ER",2,"waiting"),
        (1087,"P1087",25,"ER",2,"waiting"), (1010,"P1010",29,"Pharm",3,"waiting"),
        (1011,"P1011",35,"ICU",5,"waiting"), (1012,"P1012",21,"Lab",4,"waiting"),
        (1013,"P1013",20,"Ward",2,"waiting"), (1014,"P1014",36,"Pharm",1,"waiting"),
        (1015,"P1015",23,"ER",5,"waiting"), (1016,"P1016",42,"ICU",3,"waiting"),
    ]

    # Insert and print probe sequence for collision demonstration
    for tup in sample:
        rec = Patient(*tup)
        result = ht.insert(rec)
        print(f"insert {rec.pid}: {result}; probes {ht.debug_last_probe()}")

    print(f"Load factor: {ht._count}/{ht._cap} = {ht._count/ht._cap:.3f}")

    # Demonstrate duplicate handling
    upd = Patient(1004,"P1004",26,"Pharm",4,"treated")
    res_upd = ht.insert(upd)
    print(f"insert duplicate (1004): {res_upd}; probes {ht.debug_last_probe()}")

    # Search demonstration
    hit = ht.search(1058)
    print("search 1058 ->", hit)
    print("search 1058 probes:", ht.debug_last_probe())
    miss = ht.search(1999)
    print("search 1999 ->", miss)

    # Delete and verify
    print("delete 1007 ->", ht.delete(1007))
    print("search 1007 after delete ->", ht.search(1007))

    # Trigger resize to show load management
    extra = [
        (2000,"P2000",30,"ER",2,"waiting"),
        (2029,"P2029",30,"ER",2,"waiting")
    ]
    for tup in extra:
        rec = Patient(*tup)
        ht.insert(rec)
        print(f"insert {rec.pid}: probes {ht.debug_last_probe()}")
    print("resize events:", ht.debug_resize_events())



# MODULE 3 – HEAP SCHEDULER DEMO

def demo_heap_scheduler(ht: HashTable):
    """
    Uses EmergencyScheduler to:
      • Compute priorities for 10 requests
      • Show heap after each insert & extract
      • Confirm higher-priority patients are served first
    """
    sched = EmergencyScheduler(ht)
    for pid, mins in [
        (1002,30),(1003,60),(1004,15),(1005,45),(1008,10),
        (1010,25),(1012,90),(1014,20),(1016,35),(1013,12)
    ]:
        sched.add_request(pid, mins)
    for _ in range(5):
        item = sched.next_patient()
        print("NEXT:", item)



# MODULE 4 – SORTING DEMO

def demo_sorting():
    """
    Benchmarks Merge Sort and Quick Sort using different dataset
    sizes and input conditions (random, nearly-sorted, reversed).
    Prints timing results that can be copied into the report table.
    """
    import time
    sizes = [100, 500, 1000]
    rng = RNG(42)

    def make_random(n):
        arr = [0] * n
        for i in range(n):
            arr[i] = rng.next_range(0, 100000)
        return arr

    for n in sizes:
        base = make_random(n)
        cases = {
            "random": list(base),
            "nearly": nearly_sorted(sorted(base), 10),
            "reversed": list(reversed(sorted(base)))
        }
        for name, data in cases.items():
            a1 = list(data)
            t0 = time.time(); Sorter.merge_sort(a1); t1 = time.time()
            a2 = list(data)
            t2 = time.time(); Sorter.quick_sort(a2); t3 = time.time()
            print(f"n={n:4d} case={name:8s} merge={t1-t0:.4f}s quick={t3-t2:.4f}s")



# MAIN DRIVER

def main():
    print("───────── MODULE 1: GRAPH ─────────")
    demo_graph()

    print("\n───────── MODULE 2: HASH TABLE ─────────")
    ht = HashTable(29)  # small initial capacity to force collisions
    demo_hash_table(ht)

    print("\n───────── MODULE 3: HEAP SCHEDULER ─────────")
    demo_heap_scheduler(ht)

    print("\n───────── MODULE 4: SORTING ─────────")
    demo_sorting()


if __name__ == "__main__":
    main()


