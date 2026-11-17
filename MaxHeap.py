# Array-based implementation of a binary max heap.
# - Each node has higher priority than its children.
# - Used to always extract the highest-priority patient first.

class MaxHeap:
    def __init__(self, capacity=16):
        self._a = [None] * capacity   # internal array to store heap items
        self._n = 0                   # current number of elements

    def _resize(self):
        """Doubles the heap’s capacity when full."""
        new_a = [None] * (len(self._a) * 2)
        i = 0
        while i < self._n:
            new_a[i] = self._a[i]
            i += 1
        self._a = new_a

    def insert(self, item):
        """
        Adds a new request to the heap and restores heap order
        using the trickle-up process.
        """
        if self._n == len(self._a):    # expand array if needed
            self._resize()
        self._a[self._n] = item        # place item at next free spot
        self._trickle_up(self._n)      # move up if priority is higher
        self._n += 1

    def peek(self):
        """Returns (but does not remove) the highest-priority item."""
        if self._n == 0:
            return None
        return self._a[0]

    def extract_priority(self):
        """
        Removes and returns the highest-priority request.
        Then reorders the heap using trickle-down.
        """
        if self._n == 0:
            return None
        top = self._a[0]
        self._n -= 1
        self._a[0] = self._a[self._n]  # Move last item to root
        self._a[self._n] = None        # Clear old position
        self._trickle_down(0)
        return top

    def _trickle_up(self, idx):
        """
        Moves an element up the heap until it is in the correct position.
        Used when inserting a new item.
        """
        while idx > 0:
            parent = (idx - 1) // 2
            if self._a[parent].priority < self._a[idx].priority:
                # Swap child with parent if child has higher priority
                self._a[parent], self._a[idx] = self._a[idx], self._a[parent]
                idx = parent
            else:
                # If already in correct order, stop
                idx = 0

    def _trickle_down(self, idx):
        """
        Moves an element down the heap to restore heap order.
        Used when extracting the top item.
        """
        n = self._n
        while True:
            left = idx * 2 + 1
            if left >= n:  # no children → stop
                return
            right = left + 1
            # Select the larger child
            largest = left
            if right < n and self._a[right].priority > self._a[left].priority:
                largest = right
            # If child has higher priority, swap and continue
            if self._a[largest].priority > self._a[idx].priority:
                self._a[largest], self._a[idx] = self._a[idx], self._a[largest]
                idx = largest
            else:
                return

    def as_list(self):
        """
        Returns a Python list representation of the current heap contents.
        Useful for tracing/logging heap states after operations.
        """
        out = []
        i = 0
        while i < self._n:
            out.append(self._a[i])
            i += 1
        return out