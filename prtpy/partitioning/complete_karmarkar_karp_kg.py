"""
    Partition the items using the complete Karmarkar-Karp Heuristic partitioning algorithm

    Taken help from:
        "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
        By Richard E. Korf

    Algorithm number in Paper:
        2.3

    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132

    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""
import heapq
import numpy as np
from typing import Callable, List
from itertools import count, permutations
from prtpy import Bins, printbins
from prtpy.partitioning.trivial import trivial_partition


def ckk(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the items using the complete Karmarkar-Karp Heuristic partitioning algorithm.
    Finds a partition that minimizes the difference between the largest and smallest sum.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> ckk(BinsKeepingContents(1), items=[1, 6, 2, 3, 4, 7]).bins
    [[1, 6, 2, 3, 4, 7]]

    >>> ckk(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).bins
    [[85, 75], [95, 25, 15, 5]]

    >>> ckk(bins=BinsKeepingContents(2), items=[5, 8, 6, 4, 7]).bins
    [[7, 5, 4], [8, 6]]

    >>> list(ckk(BinsKeepingContents(2), items=[1, 6, 2, 3, 4, 7]).sums)
    [12.0, 11.0]

    >>> ckk(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).bins
    [[85, 75], [95, 25, 15, 5]]

    >>> list(ckk(BinsKeepingContents(3), items=[8, 7, 6, 5, 4]).bins)
    [[7, 4], [6, 5], [8]]

    >>> list(ckk(BinsKeepingContents(3), items=[95, 15, 75, 25, 85, 5]).bins)
    [[95, 5], [85, 15], [75, 25]]

    >>> ckk(BinsKeepingContents(5), items=[1, 2, 3, 4, 5]).bins
    [[1], [2], [3], [4], [5]]

    >>> ckk(BinsKeepingContents(5), items=[1,9,8,2,3,7,6,5,4]).bins
    [[8, 1], [7, 2], [6, 3], [5, 4], [9]]

    >>> ckk(BinsKeepingContents(5), items=[1,9,8,2,3,7,6,5,4]).sums
    array([9., 9., 9., 9., 9.])

    >>> ckk(BinsKeepingContents(2), items=[1, 2]).bins
    [[1], [2]]

    >>> ckk(BinsKeepingContents(0), items=[number for number in range(10)]).bins
    []

    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> ckk(BinsKeepingContents(3), walter_numbers).sort_by_ascending_sum()  # objective=obj.MinimizeDifference
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    """
    if trivial_partition(bins, items):
        return bins

    sorted_items = sorted(items, key=valueof, reverse=True)
    partition = ckk_heuristic(sorted_items, bins.num)
    result = [p[0] for p in partition]

    for index, p in enumerate(sorted(result[0], key=sum, reverse=True)):
        for n in sorted(p, reverse=True):
            bins.add_item_to_bin(item=n, bin_index=index)
    return bins


def ckk_heuristic(items: List[any], k: int = 2):
    """
    This function returns a heuristic of items list for k >= 2

    For any k ≥ 2, the algorithm can be generalized in the following way:
        1. Initially, for each number i in S, construct a k-tuple of subsets, in which one subset is {i} and the other k-1 subsets are empty.
        2. In each iteration, select two k-tuples A and B in which the difference between the maximum and minimum sum is largest, and combine them in reverse order of sizes, i.e.: smallest subset in A with largest subset in B, second-smallest in A with second-largest in B, etc.
        3. Proceed in this way until a single partition remains.

    >>> [i for i in ckk_heuristic(items=[1, 2])]
    [([[1], [2]], [1, 2])]

    >>> [i for i in ckk_heuristic(items=[4, 5, 6, 7, 8])]
    [([[4, 5, 7], [6, 8]], [16, 14]), ([[4, 5, 6], [7, 8]], [15, 15])]

    >>> [i for i in ckk_heuristic(items=[1, 2, 3, 4, 5, 6])]
    [([[1, 4, 5], [2, 3, 6]], [10, 11])]

    """
    stack = [[]]
    heap_count = count()
    for number in items:
        l: List[List[int]] = [[] for _ in range(k - 1)]
        r: List[List[int]] = [[number]]
        this_partition = l + r
        this_sizes: List[int] = [0] * (k - 1) + [number]
        heapq.heappush(stack[0], (-number, next(heap_count), this_partition, this_sizes))
    best = -np.inf
    while stack:
        partitions = stack.pop()
        if _possible_partition_difference_lower_bound(partitions, k) <= best:
            continue
        if len(partitions) == 1:
            num = partitions[0][0]
            if num > best:
                best = num
                _, _, final_partition, final_sums = partitions[0]
                yield final_partition, final_sums
            continue
        _, _, p1, p1_sum = heapq.heappop(partitions)
        _, _, p2, p2_sum = heapq.heappop(partitions)
        tmp_stack_extension = []
        for new_partition, new_sizes in _combine_partitions(p1, p2):
            tmp_partitions = partitions[:]
            diff = max(new_sizes) - min(new_sizes)
            heapq.heappush(tmp_partitions, (-diff, next(heap_count), new_partition, new_sizes))
            tmp_stack_extension.append(tmp_partitions)
        stack.extend(sorted(tmp_stack_extension))


def _combine_partitions(partition_1, partition_2):
    """
    This function return a combination between two partitions
    """
    yielded = set()
    for permutation in permutations(partition_1, len(partition_1)):
        out = sorted(sorted(p + l) for p, l in zip(permutation, partition_2))
        out_ = tuple(tuple(el) for el in out)
        if out_ not in yielded:
            yielded.add(out_)
            yield out, [sum(x) for x in out]


def _possible_partition_difference_lower_bound(node, k: int) -> int:
    """
    This function return the possible partition difference lower bound of a node with size k
    """
    sizes_flattened = [size for partition in node for size in partition[3]]
    max_sizes_flattened = max(sizes_flattened)
    return -(max_sizes_flattened - (sum(sizes_flattened) - max_sizes_flattened) // (k - 1))


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

