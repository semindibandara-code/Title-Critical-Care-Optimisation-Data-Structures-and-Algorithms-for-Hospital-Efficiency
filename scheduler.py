# This module manages patient scheduling using a MAX HEAP data structure.
# Patients with higher urgency and shorter treatment time are given
# higher priority. Priority is computed using:
#       Priority = (6 - UrgencyLevel) + (1000 / TreatmentTime)

# Dependencies:
#   - DSAHeap and DSAHeapEntry (custom heap implementation)
#   - HashTable / Patient records from Module 2

# Features:
#   - Add new emergency requests based on urgency and time
#   - Extract highest-priority patient (max heap property)
#   - Print heap states after each operation
#   - Update patient urgency or time


from typing import Optional, Tuple
from DSAHeap import DSAHeap           # Custom heap class
from DSAHeapEntry import DSAHeapEntry # Entry wrapper for heap nodes

# Attempt to import HashTable and Patient from Module 2
try:
    from hash_table import HashTable, Patient
except Exception:
    # Fallback in case of different naming
    from DSAHashTable import DSAHashTable as HashTable  # type: ignore
    class Patient:
        pass


class EmergencyScheduler:
    """
    A class that schedules emergency patients using a MAX HEAP.
    The heap always serves the patient with the highest computed priority first.
    """

    def __init__(self, patients: "HashTable"):
        """Initializes the scheduler with a reference to the patient hash table."""
        self._patients = patients
        self._heap = DSAHeap(32)   # Default heap size (32 entries)

    
    #  Priority Computation Formula
    
    @staticmethod
    def compute_priority(urgency: int, minutes: float) -> float:
        """
        Calculates the priority score based on urgency (U) and time (T).
        Formula: Priority = (6 - U) + 1000 / T
        Higher priority means the patient will be treated sooner.
        """
        return (6 - int(urgency)) + (1000.0 / float(minutes))

    
    #  Validate that the patient record exists and is active
    
    def _valid_patient(self, pid: int) -> Tuple[bool, Optional[object]]:
        """
        Checks whether the given patient ID exists and is active.
        Returns (True, record) if valid, or (False, None) if not.
        """
        try:
            rec = self._patients.search(pid)
        except Exception:
            rec = None

        if rec is None:
            print(f"! Invalid PatientID {pid}")
            return False, None

        # Some hash tables store status as text (e.g., "inactive", "discharged")
        status = getattr(rec, 'status',
                         getattr(rec, 'getStatus', lambda: 'active')()) if rec else 'active'

        if isinstance(status, str) and status.strip().lower() in {"inactive", "discharged", "done", "completed"}:
            print(f"! Patient {pid} has inactive status '{status}'")
            return False, None

        return True, rec

   
    #  Add a new emergency request to the heap
    
    def add_request(self, pid: int, expected_minutes: float) -> Optional[DSAHeapEntry]:
        """
        Adds a patient request to the heap with a computed priority.
        """
        ok, rec = self._valid_patient(pid)
        if not ok:
            return None

        # Validation for treatment time
        if expected_minutes is None or expected_minutes <= 0:
            print(f"! Invalid treatment time T={expected_minutes} for pid={pid}")
            return None

        # Retrieve urgency from patient record
        urg = getattr(rec, 'urgency', None)
        if urg is None and hasattr(rec, 'getUrgency'):
            urg = rec.getUrgency()
        if urg is None:
            print(f"! Patient {pid} record has no urgency field")
            return None

        # Compute priority score
        prio = EmergencyScheduler.compute_priority(int(urg), float(expected_minutes))

        # Wrap in a DSAHeapEntry for consistency
        entry = DSAHeapEntry(int(prio * 1000), {  # priority is scaled up for heap comparison
            'pid': pid,
            'U': int(urg),
            'T': float(expected_minutes),
            'P_float': prio,
        })

        # Insert into the heap
        self._heap.add(entry.getPriority(), entry.getValue())

        print(f"ADD pid={pid} U={int(urg)} T={expected_minutes:.1f} -> P={prio:.3f}")
        print("HEAP:", self.heap_as_list())
        return entry

    
    #  View top priority patient (non-destructive)
   
    def peek(self) -> Optional[dict]:
        """Shows the next patient to be treated without removing from heap."""
        try:
            if self._heap._count == 0:
                return None
            top = self._heap._heap[0]
            return top.getValue()
        except Exception:
            return None

    
    #  Extract (serve) the next highest priority patient
   
    def next_patient(self) -> Optional[dict]:
        """Removes and returns the patient with the highest priority."""
        if self._heap._count == 0:
            print("(heap empty)")
            return None

        root = self._heap.remove()
        val = root.getValue() if root else None

        if val is not None:
            print(f"EXTRACT -> pid={val['pid']} P={val['P_float']:.3f} (U={val['U']} T={val['T']:.1f})")

        print("HEAP:", self.heap_as_list())
        return val

    
    #   Show heap contents as list (priority, pid)
   
    def heap_as_list(self):
        """Returns a simplified list of heap entries for printing."""
        out = []
        i = 0
        while i < self._heap._count:
            e = self._heap._heap[i]
            if e is not None:
                v = e.getValue()
                out.append((e.getPriority(), v['pid']))
            i += 1
        return out

    
    #  Update strategy (increase or decrease urgency/time)
    
    def update_request(self, pid: int, new_urgency: Optional[int] = None, new_time: Optional[float] = None):
        """
        Updates a patient's urgency or treatment time.
        Strategy:
          - Update urgency in hash table.
          - Reinsert a new request (since DSAHeap doesn't support key updates).
        """
        if new_urgency is not None:
            try:
                rec = self._patients.search(pid)
                if rec is not None:
                    if hasattr(rec, 'urgency'):
                        rec.urgency = int(new_urgency)
                    elif hasattr(rec, 'setUrgency'):
                        rec.setUrgency(int(new_urgency))
            except Exception:
                pass

        # Reinsert with new or default time (30 mins if not specified)
        t = 30.0 if new_time is None else float(new_time)
        self.add_request(pid, t)
