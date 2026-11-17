# MODULE 3: Heap-Based Emergency Scheduling

# This script demonstrates how emergency patients are prioritized
# using a heap (max-heap). The scheduler calculates a priority score:
#     Priority = (6 - UrgencyLevel) + 1000 / TreatmentTime
# Higher values mean higher priority (served first).

# Expected Output:
# • Heap state after each insert and extract
# • Priority computation logs
# • Proof that high-priority patients are treated first


from scheduler import EmergencyScheduler   # Module 3 scheduler

# Try importing the patient hash table (Module 2)
try:
    from hash_table import HashTable, Patient
except Exception:
    from DSAHashTable import DSAHashTable as HashTable  # backup class name
    class Patient:
        pass

# Function: build_patients()

# Creates a hash table of patient records (used by the scheduler)
# Each record contains:
#   (PatientID, Name, Age, Department, UrgencyLevel, Status)

def build_patients():
    ht = HashTable(59)   # prime table size to reduce collisions
    sample = [
        (1000,"P1000",31,"ER",3,"waiting"), (1001,"P1001",22,"ICU",2,"waiting"),
        (1002,"P1002",28,"Lab",5,"waiting"), (1003,"P1003",24,"Ward",1,"waiting"),
        (1004,"P1004",26,"Pharm",4,"waiting"), (1005,"P1005",33,"ER",2,"waiting"),
        (1006,"P1006",41,"ICU",1,"waiting"), (1007,"P1007",19,"Ward",3,"waiting"),
        (1008,"P1008",45,"Theatre",5,"waiting"), (1009,"P1009",38,"ER",4,"waiting"),
        (1010,"P1010",29,"Pharm",3,"waiting"), (1011,"P1011",35,"ICU",5,"waiting"),
        (1012,"P1012",21,"Lab",4,"waiting"), (1013,"P1013",20,"Ward",2,"waiting"),
        (1014,"P1014",36,"Pharm",1,"waiting"), (1015,"P1015",23,"ER",5,"waiting"),
        (1016,"P1016",42,"ICU",3,"waiting"), (1017,"P1017",34,"ER",2,"waiting"),
        (1018,"P1018",27,"Ward",4,"waiting"), (1019,"P1019",39,"Lab",1,"waiting"),
    ]
    
    # Insert each record into the hash table
    for tup in sample:
        try:
            # Preferred version (using Patient class)
            res = ht.insert(Patient(*tup)) if 'Patient' in globals() else ht.put(tup[0], tup)
        except Exception:
            # Fallback if insert() not available
            try:
                ht.put(tup[0], tup)
            except Exception:
                pass
    return ht



# MAIN FUNCTION

# Demonstrates:
#   1. Adding 10 patient requests (with different urgency/time)
#   2. Extracting 5 highest-priority patients
#   3. Updating one patient’s urgency and reinserting

def main():
    ht = build_patients()                 # Step 1: load patients
    sched = EmergencyScheduler(ht)        # Step 2: create scheduler

    # List of (PatientID, ExpectedTreatmentTime)
    requests = [
        (1006, 10),  # U=1 (highest urgency) + short time → very high priority
        (1003, 60),  # U=1 but long time
        (1019, 20),  # U=1 moderate
        (1005, 30),  # U=2
        (1017, 25),  # U=2
        (1001, 15),  # U=2
        (1000, 40),  # U=3
        (1007, 12),  # U=3
        (1014, 50),  # U=1 long time
        (1008, 18),  # U=5 (low urgency)
    ]

    # Insert each request and print the heap after each insert
    for pid, T in requests:
        sched.add_request(pid, T)   # computes and logs priority automatically

    # Extract (treat) 5 highest-priority patients
    for _ in range(5):
        sched.next_patient()        # removes top of heap, prints heap state

    
    # Update case: Patient 1008 (was low priority) now becomes urgent
  
    print("\n-- Update demo: set U=1 for pid=1008 and reinsert with T=15 --")
    sched.update_request(1008, new_urgency=1, new_time=15)
    sched.next_patient()            # check that it now appears at top



# RUN THE DEMO

if __name__ == "__main__":
    main()
