# DSAHeap.py – heap class with instance operations and static in-place sort
from DSAHeapEntry import DSAHeapEntry   # import entry class

class DSAHeap:
    def __init__(self, capacity=10):
        self._heap = [None] * capacity   # create empty list of fixed size capacity O(1)
        self._count = 0                  # track number of items holds dsaheapentry and counts track how many spots are actualy used.

    def _resize(self): #O(n) when full
        new_capacity = len(self._heap) * 2                # double array size
        new_array = [None] * new_capacity                 # create bigger list
        ii = 0
        while ii < self._count:                           # copy uused element from the oldlist
            new_array[ii] = self._heap[ii]      #into the new list with a loop swaps the reference so the heap points to the larger list
            ii = ii + 1
        self._heap = new_array                            # replace heap list

    def add(self, priority, value): #O(log n) -average, O(n) if resize happens
        if self._count == len(self._heap):                # if the heap array full
            self._resize() #calls resize
        self._heap[self._count] = DSAHeapEntry(priority, value)  # put new entry at the next free index 
        self._trickleUp(self._count)                   #then calls trickleup on that index to restore heap order by swapping upward
        self._count = self._count + 1                     # increase count

    def remove(self): #O(log n)
        if self._count == 0:                              # if empty
            raise Exception("Heap is empty")              # stop otherwise saves the root item to return
        root = self._heap[0]                              # moves the last item into index 0, clears the slot
        last_index = self._count - 1                      # find last index
        self._heap[0] = self._heap[last_index]            # move last to root
        self._heap[last_index] = None                     # clear last spot
        self._count = last_index                          # reduce count
        if self._count > 0:                               # if still not empty
            self._trickleDown(0, self._count)             # fix order
        return root                                       # return removed root

    def display(self):
        ii = 0
        parts = []                                        # collect items as strings
        while ii < self._count:
            e = self._heap[ii]
            if e is not None:
                parts.append("(" + str(e.getPriority()) + ", " + str(e.getValue()) + ")")
            ii = ii + 1
        print(" ".join(parts))                            # print heap as one line

    # used when adding new items
    def _trickleUp(self, index): #moves a new node upward to keep the heap property
        curIdx = index                                    # current node index
        parentIdx = (curIdx - 1) // 2                     # parent index
        cond = curIdx > 0 #compares the node with its parent                                       
        while cond and self._heap[curIdx].getPriority() > self._heap[parentIdx].getPriority(): #if the child prority is higher they swap
            tmp = self._heap[parentIdx]                   # swaps the two
            self._heap[parentIdx] = self._heap[curIdx] 
            self._heap[curIdx] = tmp
            curIdx = parentIdx                            # move up. #after each swap, movrs cur ind to par ind
            parentIdx = (curIdx - 1) // 2
            cond = curIdx > 0                             # repeat until the node reaches the root or when the parent is equal or larger
#used when removing items
    def _trickleDown(self, index, numItems=None): #moves a node downward to restore heap after removing the root
        if numItems is None: #uses numitem
            numItems = self._count                        # use full heap
        curIdx = index
        lChildIdx = curIdx * 2 + 1
        rChildIdx = lChildIdx + 1
        keepGoing = True #lets the loop continue running while swaps are still needed.
        while keepGoing and lChildIdx < numItems: #while left child exists picks the larger child
            keepGoing = False
            largeIdx = lChildIdx
            if rChildIdx < numItems:  #finds the larger of the two children
                left = self._heap[lChildIdx]
                right = self._heap[rChildIdx] #if that child has a higher priority, swaps with parent
                if left is not None and right is not None:
                    if left.getPriority() < right.getPriority(): #if the child has high priority it swaps and. moves down to the child
                        largeIdx = rChildIdx
            child = self._heap[largeIdx]
            curr = self._heap[curIdx]
            if child is not None and curr is not None:
                if child.getPriority() > curr.getPriority():
                    tmp = self._heap[largeIdx]
                    self._heap[largeIdx] = self._heap[curIdx]
                    self._heap[curIdx] = tmp
                    curIdx = largeIdx
                    lChildIdx = curIdx * 2 + 1
                    rChildIdx = lChildIdx + 1
                    keepGoing = True                       # continue swapping
                else:
                    keepGoing = False #keeps moving down until the heap property is fixed
            else:
                keepGoing = False

    # same idea as trickledown
    @staticmethod
    def _trickleDownArray(arr, curIdx, limit): #works directly on an array instead of heap
        lChildIdx = curIdx * 2 + 1                        # left child
        rChildIdx = lChildIdx + 1                         # right child
        keepGoing = True
        while keepGoing and lChildIdx < limit: #used inside heapsortarray and heapify to fix heap order while sorting
            keepGoing = False
            largeIdx = lChildIdx
            if rChildIdx < limit:
                if arr[lChildIdx].getPriority() < arr[rChildIdx].getPriority():
                    largeIdx = rChildIdx
            if arr[largeIdx].getPriority() > arr[curIdx].getPriority():
                tmp = arr[largeIdx]
                arr[largeIdx] = arr[curIdx]
                arr[curIdx] = tmp
                curIdx = largeIdx
                lChildIdx = curIdx * 2 + 1
                rChildIdx = lChildIdx + 1
                keepGoing = True
            else:
                keepGoing = False
#builds valid max heap from unsorted heap
    @staticmethod
    def heapifyArray(arr):
        n = len(arr)                                      # number of items
        ii = (n // 2) - 1                                 # start from last parent
        while ii >= 0: #calls trckledown on each parent moving
            DSAHeap._trickleDownArray(arr, ii, n)         # heapify down each node
            ii = ii - 1

    @staticmethod
    def heapSortArray(arr):
        DSAHeap.heapifyArray(arr)                         # first build max heap
        n = len(arr)
        ii = n - 1
        while ii >= 1:
            tmp = arr[0]                                  # swap root and last
            arr[0] = arr[ii]
            arr[ii] = tmp
            DSAHeap._trickleDownArray(arr, 0, ii)         # fix heap below limit
            ii = ii - 1
#by the end every parent is arger than its children