import heapq

class SearchableHeap:
    def __init__(self):
        self._heap = []
        self._set = set()

    def push(self, item):
        # if item in self._set:
        #     print("ADDING DUPE")
        #     # return
        heapq.heappush(self._heap, item)
        self._set.add(item)

    def pop(self):
        item = heapq.heappop(self._heap)
        # print("popping:", item)
        self._set.remove(item)
        return item

    def search(self, item):
        # print("searching for", item)
        # print(item in self._set)
        return item in self._set

    def update(self, old_value, new_value):
        try:
            index = self._heap.index(old_value)
        except ValueError:
            raise ValueError(f"Value {old_value} not found in heap")

        self._set.remove(old_value)

        self._heap[index] = new_value

        self._set.add(new_value)

        if new_value[0] < old_value[0]:
            heapq._siftdown(self._heap, 0, index)
        else:
            heapq._siftup(self._heap, index)

    def __len__(self):
        return len(self._heap)

    def __str__(self):
        return f"{self._heap}"

    def is_empty(self):
        return len(self._heap) == 0
