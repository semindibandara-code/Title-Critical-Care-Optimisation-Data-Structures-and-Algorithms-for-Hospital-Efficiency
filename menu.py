from graph import Graph
from hash_table import HashTable, Patient
from scheduler import EmergencyScheduler
from sorting import Sorter, benchmark
import csv
import time

# Helper input utilities

def ask_int(prompt, min_val=None, max_val=None):
    value = 0
    ok = False
    while not ok:
        s = input(prompt).strip()
        try:
            value = int(s)
            if min_val is not None and value < min_val:
                print("  ! Must be >=", min_val)
            elif max_val is not None and value > max_val:
                print("  ! Must be <=", max_val)
            else:
                ok = True
        except ValueError:
            print("Please enter an integer")
    return value


def ask_float(prompt, min_val=None):
    value = 0.0
    ok = False
    while not ok:
        s = input(prompt).strip()
        try:
            value = float(s)
            if min_val is not None and value < min_val:
                print("  ! Must be >=", min_val)
            else:
                ok = True
        except ValueError:
            print("   Please enter a number")
    return value


def ask_nonempty(prompt):
    s = ""
    while s == "":
        s = input(prompt).strip()
        if s == "":
            print("   Cannot be empty")
    return s


# MODULE 1 – Graph-Based Hospital Navigation

class GraphMenu:
    def __init__(self):
        self.g = Graph()

    def add_department(self):
        d = ask_nonempty("  Department name: ")
        self.g.add_department(d)
        print(" Department added")

    def add_corridor(self):
        u = ask_nonempty("  From: ")
        v = ask_nonempty("  To: ")
        w = ask_float("  Walking time (minutes): ", 0)
        self.g.add_corridor(u, v, w)
        print(" Corridor added")

    def display(self):
        print("\n--- Hospital Graph ---")
        print(self.g.adjacency_list_str())

    def bfs(self):
        src = ask_nonempty("  Source department: ")
        levels = self.g.bfs_levels(src)
        if levels:
            for i, L in enumerate(levels):
                print(f"Level {i}: {', '.join(L)}")
        else:
            print("No reachable departments")

    def dfs(self):
        src = ask_nonempty("  Source department: ")
        has, cyc = self.g.dfs_cycle(src)
        print("Cycle detected:", has)
        if has:
            print("Cycle nodes:", " -> ".join(cyc))

    def dijkstra(self):
        src = ask_nonempty("  From: ")
        dst = ask_nonempty("  To: ")
        path, cost = self.g.dijkstra(src, dst)
        if path:
            print("Path:", " -> ".join(path))
            print("Total walking time:", cost, "minutes")
        else:
            print("No path found")

    def load_csv(self):
        fname = ask_nonempty("  CSV file(departments/corridors): ")
        with open(fname, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            fields = set(r.fieldnames or [])
            if {"From", "To", "Weight"}.issubset(fields):
                for row in r:
                    self.g.add_corridor(row["From"], row["To"], float(row["Weight"]))
                print(" Corridors loaded")
            elif "Department" in fields:
                for row in r:
                    self.g.add_department(row["Department"])
                print(" Departments loaded")
            else:
                print(" Invalid CSV format")

    def save_csv(self):
        with open("departments.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Department"])
            for d in sorted(self.g._adj.keys()):
                w.writerow([d])
        with open("corridors.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["From", "To", "Weight"])
            for u in self.g._adj:
                for v, wt in self.g._adj[u]:
                    if u <= v:
                        w.writerow([u, v, wt])
        print(" Graph saved to CSV")

    def menu(self):
        opt = 0
        while opt != 10:
            print("""
===============================
Module 1: Graph Menu
===============================
1. Add Department
2. Add Corridor
3. Display Graph
4. BFS Traversal
5. DFS Cycle Detection
6. Dijkstra Shortest Path
7. Load Graph from CSV
8. Save Graph to CSV
9. Return to Main Menu
""")
            opt = ask_int("Enter choice: ", 1, 9)
            if opt == 1:
                self.add_department()
            elif opt == 2:
                self.add_corridor()
            elif opt == 3:
                self.display()
            elif opt == 4:
                self.bfs()
            elif opt == 5:
                self.dfs()
            elif opt == 6:
                self.dijkstra()
            elif opt == 7:
                self.load_csv()
            elif opt == 8:
                self.save_csv()
            elif opt == 9:
                return    


# MODULE 2 – Hash-Based Patient Lookup

class HashMenu:
    def __init__(self):
        self.ht = HashTable(29)

    def insert(self):
        pid = ask_int("  Patient ID: ")
        name = ask_nonempty("  Name: ")
        age = ask_int("  Age: ", 0)
        dept = ask_nonempty("  Department: ")
        urg = ask_int("  Urgency (1–5): ", 1, 5)
        status = ask_nonempty("  Treatment Status: ")
        self.ht.insert(Patient(pid, name, age, dept, urg, status))
        print(" Record inserted")

    def search(self):
        pid = ask_int("  Patient ID: ")
        rec = self.ht.search(pid)
        if rec:
            print(rec)
        else:
            print("Not found")

    def delete(self):
        pid = ask_int("  Patient ID: ")
        ok = self.ht.delete(pid)
        if ok:
            print(" Deleted")
        else:
            print(" Not found")

    def load_csv(self):
        fname = ask_nonempty("  CSV file(patients): ")
        count = 0
        with open(fname, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                try:
                    p = Patient(int(row["PatientID"]), row["Name"], int(row["Age"]),
                                row["Department"], int(row["UrgencyLevel"]), row["TreatmentStatus"])
                    self.ht.insert(p)
                    count += 1
                except Exception:
                    pass
        print(" Loaded", count, "records")

    def save_csv(self):
        fname = ask_nonempty("  Filename to save: ")
        with open(fname, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["PatientID", "Name", "Age", "Department", "UrgencyLevel", "TreatmentStatus"])
            for slot in self.ht._table:
                if slot not in (None, self.ht._TOMBSTONE):
                    p = slot
                    w.writerow([p.patient_id, p.name, p.age, p.department, p.urgency, p.status])
        print(" Saved hash table to", fname)

    def display(self):
        print("\n--- Hash Table Contents ---")
        for i, slot in enumerate(self.ht._table):
            if slot not in (None, self.ht._TOMBSTONE):
                print(f"{i:3d}: {slot}")

    def menu(self):
        opt = 0
        while opt != 7:
            print("""
===============================
Module 2: Patient Lookup Menu
===============================
1. Insert Record
2. Search Record
3. Delete Record
4. Load from CSV
5. Save to CSV
6. Display Table
7. Return to Main Menu
""")
            opt = ask_int("Enter choice: ", 1, 7)
            if opt == 1:
                self.insert()
            elif opt == 2:
                self.search()
            elif opt == 3:
                self.delete()
            elif opt == 4:
                self.load_csv()
            elif opt == 5:
                self.save_csv()
            elif opt == 6:
                self.display()


# MODULE 3 – Heap-Based Emergency Scheduler


class SchedulerMenu:
    def __init__(self):
        self.ht = HashTable(59)                  # patient store
        self.sched = EmergencyScheduler(self.ht) # wrapper that uses a heap

    # internal helpers 
    def _entry_to_tuple(self, e):
        """
        Normalize any heap entry to (pid, priority, U, T).
        Supports:
          - custom entries with e._value / e._priority
          - lecturer heap nodes with getValue() / getPriority()
        """
        try:
            val = e._value
            pr  = e._priority
        except AttributeError:
            val = e.getValue()
            pr  = e.getPriority()
        return val.get("pid"), float(pr), val.get("U"), val.get("T")

    def _heap_root(self):
        """Return (pid, priority, U, T) for the current root if available."""
        try:
            if getattr(self.sched._heap, "_count", 0) > 0:
                e = self.sched._heap._heap[0]
                if e is not None:
                    return self._entry_to_tuple(e)
        except Exception:
            pass
        return None

    # option 1 
    def insert_into_heap(self):
        pid = ask_int("  Patient ID: ")
        t   = ask_float("  Expected treatment time (minutes): ", 0.1)

        # EmergencyScheduler will fetch U from hashtable and compute priority
        # If patient not yet in HT, ask minimum info and insert a temp record
        p = self.ht.search(pid)
        if p is None:
            print("   Patient not in hash table. Enter minimal details.")
            name = ask_nonempty("  Name: ")
            age  = ask_int("  Age: ", 0, 150)
            dept = ask_nonempty("  Department: ")
            urg  = ask_int("  Urgency (1-5): ", 1, 5)
            self.ht.insert(Patient(pid, name, age, dept, urg, "waiting"))

        try:
            self.sched.add_request(pid, t)
        except Exception as ex:
            print("  Could not insert request:", ex)

    # option 2 
    def extract_highest(self):
        try:
            self.sched.next_patient()  # scheduler prints the served patient/logs
        except Exception as ex:
            print("   Extract failed:", ex)

    # option 3 
    def peek_highest(self):
        root = self._heap_root()
        if root is None:
            print("   Heap is empty.")
        else:
            pid, pr, u, t = root
            print(f"  Top -> PID={pid}  P={pr:.3f}  U={u}  T={t}")

    #  option 4 
    def update_priority(self):
        pid = ask_int("  Patient ID to update: ")
        u   = ask_int("  New Urgency (1-5): ", 1, 5)
        t   = ask_float("  New expected treatment time (minutes): ", 0.1)

        # Update the patient record’s urgency in the hash table (if present)
        p = self.ht.search(pid)
        if p is not None:
            p.urgency = u
            self.ht.insert(p)  # upsert

        # Strategy: reinsert request with new (U,T). Scheduler handles compute.
        try:
            self.sched.add_request(pid, t)
            print("  Priority updated via reinsertion.")
        except Exception as ex:
            print("  Update failed:", ex)

    # option 5
    def display_heap(self):
        print("\n  Current Heap (priority, patient):")
        try:
            total = getattr(self.sched._heap, "_count", 0)
            if total == 0:
                print("  (empty)")
                return
            i = 0
            while i < total:
                e = self.sched._heap._heap[i]
                if e is not None:
                    pid, pr, u, t = self._entry_to_tuple(e)
                    print(f"  {i+1:>2}. P={pr:>8.3f} | PID={pid} | U={u} | T={t}")
                i += 1
        except Exception as ex:
            print("  Cannot display heap:", ex)

    # option 6 
    def load_hash_and_rebuild(self):
        """
        Load patients into the hash table from CSV,
        then (optionally) rebuild heap from a requests CSV.
        """
        try:
            fname = ask_nonempty("  Patients CSV file: ")
            with open(fname, newline="", encoding="utf-8") as f:
                r = csv.DictReader(f)
                cnt = 0
                for row in r:
                    try:
                        p = Patient(
                            int(row["PatientID"]),
                            row["Name"].strip(),
                            int(row["Age"]),
                            row.get("Department","").strip(),
                            int(row.get("UrgencyLevel", 3)),
                            row.get("TreatmentStatus","waiting").strip()
                        )
                        self.ht.insert(p); cnt += 1
                    except Exception:
                        pass
            print(f"   Loaded {cnt} patients into hash.")

            ans = input("  Load requests CSV too? (y/n): ").strip().lower()
            if ans == "y":
                rname = ask_nonempty("  Requests CSV file: ")
                with open(rname, newline="", encoding="utf-8") as f:
                    r = csv.DictReader(f)
                    rcnt = 0
                    for row in r:
                        try:
                            self.sched.add_request(int(row["PatientID"]), float(row["ExpectedMinutes"]))
                            rcnt += 1
                        except Exception:
                            pass
                print(f"  Loaded {rcnt} requests into heap.")
        except FileNotFoundError:
            print("   File not found.")
        except Exception as ex:
            print("  Failed to load CSVs:", ex)

    # menu loop
    def menu(self):
        opt = 0
        while opt != 7:
            print("""
================================================
 Module 3 - Patient Heap Menu              
================================================
  1. Insert into Heap                          
  2. Extract Patient with Highest Priority     
  3. Peek Highest Priority                    
  4. Update Patient Priority                   
  5. Display Heap                              
  6. Load Hash CSV and Rebuild Heap            
  7. Return to Main Menu                       
""")
        # ask for input 
            opt = ask_int("Enter choice: ", 1, 7)
            if opt == 1:
                self.insert_into_heap()
            elif opt == 2:
                self.extract_highest()
            elif opt == 3:
                self.peek_highest()
            elif opt == 4:
                self.update_priority()
            elif opt == 5:
                self.display_heap()
            elif opt == 6:
                self.load_hash_and_rebuild()
            else:
                # opt == 7, return to main menu
                print("  Returning to Main Menu...")



# MODULE 4 – Sorting Patient Records

class SortMenu:
    def __init__(self):
        self.data = []

    def load_csv(self):
        fname = ask_nonempty("  CSV file (numeric column): ")
        vals = []
        with open(fname, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                for val in row.values():
                    try:
                        vals.append(float(val))
                    except ValueError:
                        pass
        self.data = vals
        print(" Loaded", len(vals), "values")

    def save_csv(self):
        fname = ask_nonempty("  Filename to save sorted data: ")
        with open(fname, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for val in self.data:
                w.writerow([val])
        print(" Saved", len(self.data), "values to", fname)

    def enter_manual(self):
        s = ask_nonempty("  Enter numbers (comma/space separated): ")
        vals = []
        for p in s.replace(",", " ").split():
            try:
                vals.append(float(p))
            except ValueError:
                print("  ! Skipping:", p)
        self.data = vals
        print(" Loaded", len(vals), "numbers")

    def run_sorts(self):
        if len(self.data) == 0:
            print("No data loaded.")
            return
        a1 = list(self.data)
        a2 = list(self.data)
        t0 = time.perf_counter()
        Sorter.merge_sort(a1)
        t1 = time.perf_counter()
        t2 = time.perf_counter()
        Sorter.quick_sort(a2)
        t3 = time.perf_counter()
        print("\nMergeSort:", a1[:15], "...")
        print("QuickSort:", a2[:15], "...")
        print(f"Timings: Merge={t1-t0:.6f}s, Quick={t3-t2:.6f}s")
        self.data = a1  # save sorted data for export

    def benchmark(self):
        rows = benchmark()
        print("\nAlgorithm | Size | Condition | Time(s)")
        for alg, n, cond, sec in rows:
            print(f"{alg:12s} {n:5d} {cond:12s} {sec:10.5f}")

    def menu(self):
        opt = 0
        while opt != 6:
            print("""
===============================
Module 4: Sorting Menu
===============================
1. Load Numbers from CSV
2. Save Sorted Data to CSV
3. Enter Numbers Manually
4. Run Merge & Quick Sort
5. Run Benchmark
6. Return to Main Menu
""")
            opt = ask_int("Enter choice: ", 1, 6)
            if opt == 1:
                self.load_csv()
            elif opt == 2:
                self.save_csv()
            elif opt == 3:
                self.enter_manual()
            elif opt == 4:
                self.run_sorts()
            elif opt == 5:
                self.benchmark()


# MAIN MENU

def main():
    gmenu = GraphMenu()
    hmenu = HashMenu()
    smenu = SchedulerMenu()
    sortmenu = SortMenu()
    ch = 0
    while ch != 5:
        print("""
================================================
                   Main Menu
================================================
1. Module 1: Graph-Based Hospital Navigation
2. Module 2: Hash-Based Patient Lookup
3. Module 3: Heap-Based Emergency Scheduling
4. Module 4: Sorting Patient Records
5. Exit
""")
        ch = ask_int("Enter choice: ", 1, 5)
        if ch == 1:
            gmenu.menu()
        elif ch == 2:
            hmenu.menu()
        elif ch == 3:
            smenu.menu()
        elif ch == 4:
            sortmenu.menu()
    print("Exiting program. Goodbye!")


# ---------------------------------------------------------------
# Run
# ---------------------------------------------------------------
if __name__ == "__main__":
    main()
