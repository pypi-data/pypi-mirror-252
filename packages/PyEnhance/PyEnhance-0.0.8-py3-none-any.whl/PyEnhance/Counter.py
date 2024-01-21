class Counter:

    def __init__(self):
        global Count
        self.Count = 0

    def Add(self):
        global Count
        self.Count += 1

Counter = Counter()

"""

=== Examples ===

Counter = Counter()

for i in range(10):
    Counter.Add()
print(Counter.Count)

"""
