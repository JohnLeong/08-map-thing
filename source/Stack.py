class Stack:
    def __init__(self):
        self._data = []

    def push(self, value):
        self._data.append(value)

    def pop(self):
        return self._data.pop()

    def peek(self):
        return self._data[len(self._data) - 1]

    def peekAt(self,i):
        if (i < 0 or i > len(self._data) - 1):
          return 0
        return self._data[i]

    def size(self):
        return len(self._data)

    def copyFrom(self, aStack):
        for i in range(aStack.size()):
          self._data.append(aStack.peekAt(i))
