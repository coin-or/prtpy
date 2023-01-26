class MinHeap:
    def __init__(self, lst=[]):
        self.heap = []
        self.heap = self.buildHeap(lst)

    def buildHeap(self, lst):
        mid = (len(lst) - 2) // 2
        while mid >= 0:
            self._siftdown(lst, mid, len(lst) - 1)
            mid -= 1
        return lst

    def _siftdown(self, lst, start, end):
        root = start
        while root * 2 + 1 <= end:
            child = root * 2 + 1
            if child + 1 <= end and sum(lst[child]) > sum(lst[child + 1]):
                child += 1
            if sum(lst[root]) > sum(lst[child]):
                lst[root], lst[child] = lst[child], lst[root]
                root = child
            else:
                return

    def push(self, val):
        self.heap.append(val)
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        minimum = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0, len(self.heap))
        return minimum

    def _bubble_up(self, index):
        parent = (index - 1) // 2
        if index <= 0 or sum(self.heap[parent]) <= sum(self.heap[index]):
            return
        self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
        self._bubble_up(parent)

    def _bubble_down(self, index, end):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        if left < end and sum(self.heap[left]) < sum(self.heap[smallest]):
            smallest = left
        if right < end and sum(self.heap[right]) < sum(self.heap[smallest]):
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._bubble_down(smallest, end)
