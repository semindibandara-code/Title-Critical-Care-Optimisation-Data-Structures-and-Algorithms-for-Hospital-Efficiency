# MODULE 3: Heap-Based Emergency Scheduling

# This module implements:
#   1. A Max-Heap to manage emergency cases by priority
#   2. A Scheduler that ties the heap to patient urgency data

# Priority Formula:
#   Priority = (6 - UrgencyLevel) + (1000 / ExpectedTreatmentTime)
#   → Higher priority value = more urgent / shorter time

# The heap ensures that the next patient served is always the
# one with the highest computed priority.


from typing import Hashable

# Represents one emergency scheduling request
# Each request links a PatientID with expected treatment time
# and a computed priority score.
# ---------------------------------------------------------------
class SchedRequest:
    def __init__(self, pid, expected_minutes):
        self.pid = pid                    # Patient ID
        self.expected = expected_minutes  # Expected treatment time (T)
        self.priority = 0.0               # Computed from urgency + time

    def __repr__(self):
        """Readable representation for printing heap state."""
        return f"Req(pid={self.pid}, T={self.expected}, P={self.priority:.3f})"





