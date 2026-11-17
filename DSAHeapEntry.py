# DSAHeapEntry.py – stores a single heap element (priority + value)

class DSAHeapEntry: #defines a class to hold one heap item
    def __init__(self, priority, value):
        self._priority = int(priority)   # store numeric priority
        self._value = value              # store generic value

    def getPriority(self):
        return self._priority            # return priority

    def setPriority(self, priority):
        self._priority = int(priority)   # update priority

    def getValue(self):
        return self._value               # return value

    def setValue(self, value):
        self._value = value              # update value
