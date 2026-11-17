# Integrates the MaxHeap with the HashTable of patients.
# Looks up urgency (U) from patient records and computes priority.

from typing import Hashable
from DSAHeap import DSAHeap
from MaxHeap import MaxHeap
from SchedRequest import SchedRequest


class EmergencyScheduler:
    def __init__(self, patients: "Hashable"):
        """
        patients → reference to HashTable from Module 2.
        Stores urgency and other details used for scheduling.
        """
        self._patients = patients
        self._heap = MaxHeap()

    @staticmethod
    def compute_priority(U, T):
        """
        Calculates priority based on the given formula:
            P = (6 - U) + (1000 / T)
        Where:
            U = urgency level (1 = highest, 5 = lowest)
            T = expected treatment time (minutes)
        """
        return (6 - U) + (1000.0 / T)

    def add_request(self, pid, expected_minutes):
        """
        Adds a new emergency request to the heap.
        Fetches urgency from patient records and logs heap state.
        """
        rec = self._patients.search(pid)
        if rec is None:
            print(f"! Invalid patient id {pid}")
            return
        if expected_minutes <= 0:
            print(f"! Invalid time {expected_minutes}")
            return

        # Create a scheduling request and compute its priority
        req = SchedRequest(pid, expected_minutes)
        req.priority = EmergencyScheduler.compute_priority(rec.urgency, expected_minutes)

        # Insert into heap and display heap state
        self._heap.insert(req)
        print("HEAP AFTER INSERT:", self._heap.as_list())

    def next_patient(self):
        """
        Extracts and returns the next highest-priority patient.
        Prints the heap state after extraction.
        """
        item = self._heap.extract_priority()
        print("HEAP AFTER EXTRACT:", self._heap.as_list())
        return item
