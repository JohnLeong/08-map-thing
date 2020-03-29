class Queue:
    def __init__(self):
        self._data = collections.deque([])

    def enqueue(self, value):
        self._data.append(value)

    def dequeue(self):
        return self._data.popleft()

    def isEmpty(self):
        return (len(self._data) == 0)

    def size(self):
        return len(self._data)
