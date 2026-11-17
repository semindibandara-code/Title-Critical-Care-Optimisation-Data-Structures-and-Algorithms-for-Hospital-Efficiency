# DSAHashTable.py
from DSAHashEntry import DSAHashEntry   # import entry class
import math                             # used for square root in prime testing

class DSAHashTable:
    def __init__(self, table_size=101, probing="double"):  # constructor
        self._size = self._next_prime(table_size)          # resize to next prime
        self._array = [DSAHashEntry() for _ in range(self._size)]  # make empty entries
        self._count = 0                                    # sets the count of items to 0
        self._probing = probing                            # "linear" or "double"
        self._upper_lf = 0.70                              # resize up threshold load factor to grow
        self._lower_lf = 0.30                              # resize down threshold load factor to shrink

    
    def put(self, inKey: str, inValue):          # insert new key/value
        if not isinstance(inKey, str):           # only allow string keys
            raise TypeError("Key must be a string")
        if self.hasKey(inKey):                   # check for duplicates
            raise ValueError(f"Duplicate key: {inKey}")
        idx = self._find_slot_for_insert(inKey)  # find empty slot
        self._array[idx] = DSAHashEntry(inKey, inValue)  # place entry
        self._count += 1                         # increment count updates item count for load factor/resizing
        self._maybe_resize()                     # resize if needed

    def get(self, inKey: str):                   # retrieve value by key using probing
        idx = self._find_slot_for_search(inKey)  # search for slot
        if idx == -1:                            # not found key not found -> raise error
            raise KeyError(inKey)                # raise error
        return self._array[idx].value            # return the value stre at the slot

    def remove(self, inKey: str):                # remove a key
        idx = self._find_slot_for_search(inKey)  # search for the key 
        if idx == -1:                            # not found
            raise KeyError(inKey)                # raise error
        self._array[idx].key = None              # clear key
        self._array[idx].value = None            # clear value
        self._array[idx].state = -1              # mark as deleted (tombstone) mark as tombstone so probing still works
        self._count -= 1                         # decrement count  reduce active item count for load factor
        self._maybe_resize()                     # resize if needed

    def hasKey(self, inKey: str) -> bool:        # check existence
        return self._find_slot_for_search(inKey) != -1 #key missing

    def getLoadFactor(self) -> float:            # load factor
        return self._count / self._size
#goes through the array 
    def keys(self):                              # return all keys
        for e in self._array:
            if e.state == 1:                     # only live entries
                yield e.key

    def items(self):                             # return all pairs (the key and the value)
        for e in self._array:
            if e.state == 1:
                yield (e.key, e.value)

    #File I/0
    #a method just to write the table into a file 
    def export(self, path: str):                 # save alias
        self.save_csv(path) 

    def save_csv(self, path: str):               # save to CSV opens,write a header row 
        import csv
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["key", "value"])         # write header
            for k, v in self.items():            # loop items
                w.writerow([k, v])               # write row

    def load_csv(self, path: str, key_col=0, value_col=1, skip_header=True):
        import csv
        added = 0
        dupes = 0
        with open(path, newline="", encoding="utf-8") as f:
            r = csv.reader(f)
            first = True                         # track header
            for row in r:
                if not row:                      # skip empty rows
                    dummy = 0
                else:
                    if first and skip_header:    # skip first row if header
                        first = False
                        dummy = 0
                    else:
                        try:
                            key = str(row[key_col]).strip()
                            val = row[value_col] if value_col < len(row) else ""
                            self.put(key, val)   # insert
                            added += 1
                        except ValueError:       # duplicate found
                            dupes += 1
        return added, dupes                      # return stats

    # Internal helpers
    def _hash(self, inKey: str) -> int:          # primary hash
        hashIdx = 0
        ii = 0
        while ii < len(inKey):                   # go through chars
            #multiplies the running total by 31 and adds the character value.
            hashIdx = (31 * hashIdx + ord(inKey[ii])) & 0x7FFFFFFF #gets the ASCII (numeric) value of the character.
            ii += 1
        return hashIdx % self._size              # fit inside table

    def _stepHash(self, inKey: str) -> int:      # secondary hash for double hashing 
        max_step = 5 if self._size < 50 else 13  # choose small prime to calculate step size  
        raw = 0 #makes a raw hash
        jj = 0
        while jj < len(inKey):                   # raw hash loop
            raw = (31 * raw + ord(inKey[jj])) & 0x7FFFFFFF
            jj += 1
        step = max_step - (raw % max_step)       # compute step
        if step == 0:                            # avoid 0
            step = 1#change to 1 so that the probing moves
        return step
#chooses the step for probing
    def _probe_step(self, inKey: str, attempt: int) -> int:
        if self._probing == "linear":            # linear probing
            return 1
        return self._stepHash(inKey)             # double hashing calls the second hash
#finds where a new key should go
    def _find_slot_for_insert(self, inKey: str) -> int:
        hashIdx = self._hash(inKey)              # start index
        origIdx = hashIdx                        # remember start
        found = False
        giveUp = False
        firstTomb = -1
        while (not found) and (not giveUp):      # loop until result
            e = self._array[hashIdx]             # entry at index
            if e.state == 0:                     # never used
                if firstTomb != -1:              # reuse tombstone
                    hashIdx = firstTomb
                found = True
            elif e.state == -1:                  # tombstone
                if firstTomb == -1:              # save first tomb
                    firstTomb = hashIdx
                step = self._probe_step(inKey, 0)
                hashIdx = (hashIdx + step) % self._size
                if hashIdx == origIdx:           # full loop
                    giveUp = True
            else:                                # state == 1
                if e.key == inKey:               # duplicate
                    raise ValueError(f"Duplicate key: {inKey}")
                step = self._probe_step(inKey, 0)
                hashIdx = (hashIdx + step) % self._size
                if hashIdx == origIdx:           # full loop
                    giveUp = True
        if not found and giveUp:                 # no slot found
            raise RuntimeError("Hash table is full")
        return hashIdx
#finds where the key is stored 
    def _find_slot_for_search(self, inKey: str) -> int:
        hashIdx = self._hash(inKey)              # start index
        origIdx = hashIdx
        found = False   #probes until it finds the key
        giveUp = False
        result = -1
        while (not found) and (not giveUp):      # loop
            e = self._array[hashIdx]
            if e.state == 0:                     # hits never used slotor comes back to start it stops
                giveUp = True                    #returns the index if found otherwise -1
            elif e.state == 1 and e.key == inKey: # found match
                result = hashIdx
                found = True
            else:
                step = self._probe_step(inKey, 0)
                hashIdx = (hashIdx + step) % self._size
                if hashIdx == origIdx:           # full loop
                    giveUp = True
        return result

    def _maybe_resize(self):
        lf = self.getLoadFactor()                # current LF
        if lf > self._upper_lf:                  # too full #above 0.7 table doubles 
            self._resize(self._size * 2)         # grow
        elif self._size > 101 and lf < self._lower_lf:  # too empty below 0.3 and bigger than the base size it shrinks
            self._resize(self._size // 2)        # shrink
#changes the table capacity 
    def _resize(self, new_size):
        newCap = self._next_prime(new_size)      # get prime size
        oldItems = list(self.items())            # copy old items (makes a new empty array)
        self._size = newCap
        self._array = [DSAHashEntry() for _ in range(self._size)]
        self._count = 0
        ii = 0
        while ii < len(oldItems):                # reinsert
            k, v = oldItems[ii]
            idx = self._find_slot_for_insert(k)
            self._array[idx] = DSAHashEntry(k, v)
            self._count += 1
            ii += 1
#finds the next prime number 
#thats equal or bigger than the given start size
    def _next_prime(self, startVal: int) -> int:
        if startVal % 2 == 0:                    # make odd checks for odd numbers 
            primeVal = startVal + 1
        else:
            primeVal = startVal
        isPrime = False
        while not isPrime:                       # loop until prime it finds one that isnt divisble by any. small factor
            ii = 3
            isPrime = True
            rootVal = int(math.isqrt(primeVal))
            if primeVal == 2:                    # 2 is prime
                isPrime = True
            elif primeVal % 2 == 0:              # even not prime
                isPrime = False
            else:
                while (ii <= rootVal) and isPrime: # test factors
                    if primeVal % ii == 0:       # divisible
                        isPrime = False
                    else:
                        ii += 2
            if not isPrime:                      # try next odd
                primeVal += 2
        return primeVal
