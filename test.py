import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []  # Internal list to store elements as a min-heap
        self._index = 0   # Used to handle tie-breaking for elements with same priority

    def put(self, item, priority):
        """
        Inserts an item into the priority queue with a given priority.
        Lower priority values indicate higher priority.
        """
        # We store a tuple: (-priority, index, item)
        # The negative priority ensures min-heap behavior for highest priority items.
        # The index is for stable sorting (FIFO) when priorities are equal.
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def get(self):
        """
        Removes and returns the item with the highest priority.
        """
        if self.is_empty():
            raise IndexError("Cannot get from an empty priority queue.")
        # We only return the actual item, discarding priority and index.
        return heapq.heappop(self._queue)[2]

    def is_empty(self):
        """
        Checks if the priority queue is empty.
        """
        return len(self._queue) == 0

    def size(self):
        """
        Returns the number of items in the priority queue.
        """
        return len(self._queue)

# Example Usage:
if __name__ == "__main__":
    pq = PriorityQueue()

    pq.put([1,2,3], 3)
    pq.put([2,5,4], 1)

    print(f"Priority Queue size: {pq.size()}")

    while not pq.is_empty():
        next_item = pq.get()
        print(f"Processing: {next_item}")

    print(f"Priority Queue empty: {pq.is_empty()}")