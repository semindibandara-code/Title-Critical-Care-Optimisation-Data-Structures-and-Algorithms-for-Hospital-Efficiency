
# MODULE 2: Hash-Based Patient Lookup

# This module stores and retrieves patient records efficiently
# using a custom-built hash table .
#
# Hashing technique: Open Addressing (Linear Probing)
#   - Uses modulo-based hash function
#   - Handles collisions by checking next index
#   - Resizes (rehash) when load > 0.7
#
# Each patient record includes:
#   ID, Name, Age, Department, UrgencyLevel (1–5), TreatmentStatus


# PATIENT CLASS

class Patient:
    def __init__(self, pid, name, age, dept, urgency, status):
        """
        Initializes a patient record with validation checks
        according to assignment requirements.
        """
        # Basic data validation
        if not isinstance(pid, int):
            raise TypeError("PatientID must be an integer")
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non-empty string")
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer")
        if not isinstance(dept, str) or dept.strip() == "":
            raise ValueError("Department must be a non-empty string")
        if not isinstance(urgency, int) or not (1 <= urgency <= 5):
            raise ValueError("UrgencyLevel must be an integer between 1–5")
        if not isinstance(status, str) or status.strip() == "":
            raise ValueError("TreatmentStatus must be a non-empty string")

        # Assign validated values
        self.pid = pid
        self.name = name.strip()
        self.age = age
        self.dept = dept.strip()
        self.urgency = urgency
        self.status = status.strip()

    def __repr__(self):
        """
        String representation of the patient record.
        Example:
            Patient(1001, John, 30, ICU, U=2, waiting)
        """
        return f"Patient({self.pid},{self.name},{self.age},{self.dept},U={self.urgency},{self.status})"



# HASH TABLE CLASS

class HashTable:
    # Special marker for deleted entries (tombstone)
    _TOMBSTONE = object()

    def __init__(self, capacity=53):
        """
        Initialize hash table with a prime-sized array.
        :param capacity: initial table size (prime number recommended)
        """
        self._cap = capacity if capacity > 2 else 3
        self._count = 0
        self._table = [None] * self._cap   # stores Patient objects
        self._last_probe = []              # keeps track of probe sequence
        self._resize_events = []           # stores info when table resizes

    
    # HASH FUNCTION

    def _hash(self, key):
        """
        Simple modulo-based hash function.
        Key = integer patient ID.
        """
        return int(key) % self._cap

    
    # INSERT OPERATION
    
    def insert(self, record: Patient):
        """
        Inserts or updates a patient record.
        Handles collisions using linear probing.
        Rehashes if load factor > 0.7.
        """
        # Check for rehash need
        if self._count + 1 > int(0.7 * self._cap):
            self._rehash(self._next_prime(self._cap * 2))

        idx = self._hash(record.pid)
        first_tomb = -1
        steps = 0
        self._last_probe = [idx]  # track probing sequence for debugging

        while True:
            slot = self._table[idx]
            if slot is None:
                # Empty slot → insert here or in first tombstone
                target = first_tomb if first_tomb != -1 else idx
                if target != idx:
                    self._last_probe.append(target)
                self._table[target] = record
                self._count += 1
                return "inserted"
            elif slot is HashTable._TOMBSTONE:
                # Found a deleted slot, remember for possible reuse
                if first_tomb == -1:
                    first_tomb = idx
                idx = (idx + 1) % self._cap
                self._last_probe.append(idx)
            else:
                # Collision → check if same key, otherwise probe next
                if slot.pid == record.pid:
                    self._table[idx] = record
                    return "updated"
                idx = (idx + 1) % self._cap
                self._last_probe.append(idx)

            steps += 1
            if steps > self._cap:
                # If full cycle completed, force rehash
                self._rehash(self._next_prime(self._cap * 2))
                return self.insert(record)

    
    # SEARCH OPERATION
    
    def search(self, pid):
        """
        Searches for a patient by PatientID.
        Returns the patient record or None if not found.
        """
        idx = self._hash(pid)
        steps = 0
        self._last_probe = [idx]
        while steps < self._cap:
            slot = self._table[idx]
            if slot is None:
                return None  # Stop if empty slot found
            if slot is not HashTable._TOMBSTONE and slot.pid == pid:
                return slot  # Found!
            idx = (idx + 1) % self._cap
            self._last_probe.append(idx)
            steps += 1
        return None

  
    # DELETE OPERATION
  
    def delete(self, pid):
        """
        Deletes a patient record (by PatientID).
        Replaces slot with tombstone to preserve probing chain.
        """
        idx = self._hash(pid)
        steps = 0
        self._last_probe = [idx]
        while steps < self._cap:
            slot = self._table[idx]
            if slot is None:
                return False  # Not found
            if slot is not HashTable._TOMBSTONE and slot.pid == pid:
                self._table[idx] = HashTable._TOMBSTONE
                self._count -= 1
                return True
            idx = (idx + 1) % self._cap
            self._last_probe.append(idx)
            steps += 1
        return False

    
    # RESIZING (REHASH)
    
    def _rehash(self, new_cap):
        """
        Resizes the table when load factor exceeds 0.7.
        Reinserts all active (non-tombstone) records.
        """
        old_cap = self._cap
        old = self._table
        self._cap = int(new_cap)
        self._table = [None] * self._cap
        self._count = 0
        self._resize_events.append((old_cap, self._cap))

        for slot in old:
            if slot is not None and slot is not HashTable._TOMBSTONE:
                self.insert(slot)

    
    # PRIME GENERATOR
    
    @staticmethod
    def _next_prime(start_val):
        """
        Returns the next prime number greater than or equal to start_val.
        Used to ensure better hash distribution after resizing.
        """
        if start_val <= 2:
            return 3
        candidate = int(start_val)
        if candidate % 2 == 0:
            candidate += 1
        while True:
            i = 3
            is_prime = True
            while i * i <= candidate:
                if candidate % i == 0:
                    is_prime = False
                    break
                i += 2
            if is_prime:
                return candidate
            candidate += 2

    
    # DEBUG HELPERS
    
    def debug_last_probe(self):
        """Returns the list of indices visited during last insert/search."""
        return list(self._last_probe)

    def debug_resize_events(self):
        """Returns a log of resize events (old size → new size)."""
        return list(self._resize_events)
