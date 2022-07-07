"""
Karmarkar-Karp number partitioning algorithm, for any number of bins.

Authors: Jonathan Escojido & Samuel Harroch
Since = 03-2022
Credit: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
           https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning
"""
from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins, Binner, BinsArray, printbins
import heapq, logging
from itertools import count

logger = logging.getLogger(__name__)

class BinsSortedByMaxDiff:
    """
    A data-structure that stores a collection of bin-arrays, that should be popped in descending order of the difference between the largest and smallest sum.
    Used by the multiway Karmarkar-Karp algorithm.
    Uses Python's heap library, where the sorting key is minus the difference (since it is a min-heap).
    """
    def __init__(self, binner:Binner):
        self.bins_heap = []
        self.heap_count = count()       # To avoid ambiguity in heap
        self.binner = binner

    def push(self, bins: BinsArray):
        self.binner.sort_by_ascending_sum(bins)
        bins_sums = self.binner.sums(bins)
        bins_diff = bins_sums[-1] - bins_sums[0]     # To sort by descending difference
        new_state = (-bins_diff, next(self.heap_count), bins)
        logger.debug("  New state: %s", new_state)
        heapq.heappush(self.bins_heap, new_state)

    def pop(self)->BinsArray:
        _, _, bins = heapq.heappop(self.bins_heap) 
        return bins

    def top(self)->BinsArray:
        _, _, bins = self.bins_heap[0]
        return bins

    def iterator(self):
        """ Iterate over all bins-arrays in the heap. """
        for _, _, bins in self.bins_heap:
            yield bins

    def topdiff(self)->float:
        diff, _, _ = self.bins_heap[0]
        return diff

    def clone(self):
        the_clone = BinsSortedByMaxDiff(self.binner)
        the_clone.bins_heap = self.bins_heap
        the_clone.heap_count = self.heap_count
        return the_clone

    def __len__(self):
        return len(self.bins_heap)



def kk(bins: Bins, items: List[any], valueof: Callable = lambda x: x) -> Bins:
    """
    Karmarkar-Karp number partitioning algorithm, for any number of bins.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> printbins(kk(BinsKeepingContents(2), items=[1, 6, 2, 3, 7, 4, 5, 8]))
    Bin #0: [7, 6, 4, 1], sum=18.0
    Bin #1: [8, 5, 3, 2], sum=18.0

    >>> printbins(kk(BinsKeepingContents(2), [1, 2, 3, 4, 5, 6]))
    Bin #0: [1, 6, 3], sum=10.0
    Bin #1: [2, 5, 4], sum=11.0

    >>> printbins(kk(BinsKeepingContents(2), items=[4, 5, 6, 7, 8]))
    Bin #0: [8, 6], sum=14.0
    Bin #1: [4, 7, 5], sum=16.0

    >>> printbins(kk(BinsKeepingSums(2), items=[18, 17, 12, 11, 8, 2]))
    Bin #0: sum=32.0
    Bin #1: sum=36.0

    >>> printbins(kk(BinsKeepingSums(4), items=[1,2,3,3,5,9,9]))
    Bin #0: sum=7.0
    Bin #1: sum=7.0
    Bin #2: sum=9.0
    Bin #3: sum=9.0

    >>> printbins(kk(BinsKeepingContents(4), items=[1, 3, 3, 4, 4, 5, 5, 5]))
    Bin #0: [1, 5], sum=6.0
    Bin #1: [3, 5], sum=8.0
    Bin #2: [3, 5], sum=8.0
    Bin #3: [4, 4], sum=8.0

    >>> from prtpy import partition
    >>> partition(algorithm=kk, numbins=5, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['c', 'a'], ['d', 'b'], ['e'], ['g'], ['f']]
    >>> partition(algorithm=kk, numbins=4, items=[1,2,3,3,5,9,9])
    [[3, 3, 1], [5, 2], [9], [9]]
    """
    binner = bins.get_binner()
    numitems = len(items)
    logger.info("\nKarmarkar-Karp Partitioning of %d items into %d parts.", numitems, binner.numbins)
    items = sorted(items, reverse=True, key=binner.valueof)

    bins_heap = BinsSortedByMaxDiff(binner)

    # Explanation from Wikipedia: https://en.wikipedia.org/wiki/Largest_differencing_method#Multi-way_partitioning
    # 1. "Initially, for each number i in S, construct a k-tuple of subsets, in which one subset is {i} and the other k-1 subsets are empty.
    for item in items:
        new_bins = binner.add_item_to_bin(binner.new_bins(), item=item, bin_index=binner.numbins-1)
        bins_heap.push(new_bins)

    # 2. "In each iteration, select two k-tuples A and B in which the difference between the maximum and minimum sum is largest, 
    #    "   and combine them in reverse order of sizes, i.e.: smallest subset in A with largest subset in B, second-smallest in A with second-largest in B, etc."
    #    "   Proceed in this way until a single partition remains."
    for _ in range(numitems - 1):
        # "-- select two k-tuples A and B in which the difference between the maximum and minimum sum is largest":
        bins1 = bins_heap.pop()
        bins2 = bins_heap.pop()

        # "-- combine them in reverse order of sizes":
        for i in range(binner.numbins):
            binner.combine_bins(bins1, binner.numbins-i-1, bins2, i)
        bins_heap.push(bins1)

    return bins_heap.top()


if __name__ == '__main__':
    import doctest, sys
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    if failures>0: 
        sys.exit()

    # DEMO
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    from prtpy import BinsKeepingContents, BinsKeepingSums
    # kk(BinsKeepingSums(2), [4,5,6,7,8])
    # kk(BinsKeepingContents(2), [4,5,6,7,8])
    kk(BinsKeepingSums(4), [1,2,3,3,5,9,9])
    kk(BinsKeepingContents(4), [1,2,3,3,5,9,9])
