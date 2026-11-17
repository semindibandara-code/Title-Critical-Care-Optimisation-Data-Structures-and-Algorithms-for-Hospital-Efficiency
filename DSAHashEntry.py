# DSAHashEntry.py holder for key,value and state

class DSAHashEntry:
    def __init__(self, key=None, value=None):   # constructor, key/value optional
        self.key = key                          # store the key (string)
        self.value = value                      # store the value (object)
        if key is None:                         # if no key provided
            self.state = 0                      # state 0 = never used
        else:                                   # otherwise
            self.state = 1                      # state 1 = used (occupied) -1 removed

    def __repr__(self):                         # string for debugging
        return f"Entry(key={self.key!r}, value={self.value!r}, state={self.state})"
