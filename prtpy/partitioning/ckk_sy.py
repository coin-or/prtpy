"""
Authors: Jonathan Escojido & Samuel Harroch
Since = 03-2022

Credit: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
        https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning

"""
from typing import Iterator, List, Tuple, Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins, BinsKeepingContents, BinsKeepingSums
import heapq
from itertools import count
import logging, numpy as np


logger = logging.getLogger(__name__)


def _possible_partition_difference_lower_bound(current_heap: List[Tuple[int, int, Bins, List[int]]], numbins: int) -> int:
    """
    This function check if from the current node we can yield to a better partition or not by checking the
    best difference we can reach from this node.
    """
    logger.info("  A heap with %d partitions", len(current_heap))
    sums_flattened = [size for bins in current_heap for size in bins[2].sums]
    max_sums_flattened = max(sums_flattened)
    sum_sums_flattened = sum(sums_flattened)
    lower_bound = -(max_sums_flattened - (sum_sums_flattened - max_sums_flattened) // (numbins - 1))
    logger.info(f"    Max sums = {max_sums_flattened}, sum of all sums = {sum_sums_flattened}, lower_bound = {lower_bound}")
    return lower_bound


# def ckk(bins: Bins,items: List[int],  valueof: Callable=lambda x: x, best:float = -np.inf) -> Iterator[Bins]:
#     """
#     Iterator as mentions in CKK algorithms which return better partition than the one found so far.
#     best:  negative upper bound on the difference.
#             -np.inf (default): yield better partitions than the one found so far.
#            other: yield partitions with upper bound "best" on the difference.

#     >>> from prtpy import partition
#     >>> for part in ckk(BinsKeepingSums(4), items=[1,2,3,3,5,9,9]): part
#     Bin #0: sum=7.0
#     Bin #1: sum=7.0
#     Bin #2: sum=9.0
#     Bin #3: sum=9.0
#     >>> for part in ckk(BinsKeepingContents(4), items=[1, 3, 3, 4, 4, 5, 5, 5]): part.bins
#     [[1, 5], [3, 5], [3, 5], [4, 4]]
#     """
#     stack = [[]]

#     heap_count = count()  # To avoid ambiguity in heaps
#     for item in items:
#         new_bins = bins.clone().add_item_to_bin(item=item, bin_index=(bins.num - 1))

#         heapq.heappush(
#             stack[0], (-valueof(item), next(heap_count), new_bins, new_bins.sums)
#         )

#     logger.info(f"we create the stack - all stack items are possibles branches in the tree (we then combine them in all possible ways). "
#                 f"The stack: {stack}")

#     # best = -np.inf
#     isBest = True if best == -np.inf else False
#     logger.info(f"isBest= {isBest}, "
#                 f"True means we search for the best partition, "
#                 f"False means we search for partitions with bounded difference.")
#     while stack:
#         partitions = stack.pop()

#         # if could lead to better partition - maybe insert here upper bound constraint
#         if _possible_partition_difference_lower_bound(partitions, bins.num) <= best:
#             continue

#         logger.info(f"This partition/s could lead to a better partition found so far: {partitions}")

#         # if could lead to legal partition
#         if len(partitions) == 1:

#             # diff and best are non-positives numbers
#             diff = partitions[0][0]

#             logger.info(f"We arrive to a legal partition. Is it better than the best one found so far?\n"
#                         f"is this partition diff ={-diff} < from the best one = {-best} ?")

#             if diff > best: # consolidate if geq
#                 logger.info("We found a better partition!!! Continue to search for better partitions....")
#                 if isBest:
#                     best = diff
#                 _, _, final_partition, final_sums = partitions[0]
#                 yield final_partition

#                 if diff == 0:
#                     logger.info("Perfect partition is found!!!")
#                     return
#             continue

#         logger.info("Combine between the partitions in order to create legal partition.")
#         # continue create legal part
#         _, _, bin1, bin1_sums = heapq.heappop(partitions)
#         _, _, bin2, bin2_sums = heapq.heappop(partitions)

#         tmp_stack_extension = []

#         for new_bins in bin1.all_combinations(bin2):
#             tmp_partitions = partitions[:]

#             diff = max(new_bins.sums) - min(new_bins.sums)
#             heapq.heappush(
#                 tmp_partitions, (-diff, next(heap_count), new_bins, new_bins.sums)
#             )

#             tmp_stack_extension.append(tmp_partitions)

#         stack.extend(sorted(tmp_stack_extension))


def best_ckk_partition(bins: Bins,items: List[int],  valueof: Callable=lambda x: x) -> Bins:
    """
    Finds a partition in which the largest sum is minimal, using the Complete Greedy algorithm.

    :param objective: represents the function that should be optimized. Default is minimizing the difference between bin sums.
    :param time_limit: determines how much time (in seconds) the function should run before it stops. Default is infinity.

    >>> from prtpy import BinsKeepingContents, BinsKeepingSums, printbins
    >>> print(best_ckk_partition(BinsKeepingContents(2), [4,5,6,7,8]))
    Bin #0: [4, 5, 6], sum=15
    Bin #1: [7, 8], sum=15

    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> print(best_ckk_partition(BinsKeepingContents(3), walter_numbers))
    Bin #0: [16, 39], sum=55
    Bin #1: [13, 46], sum=59
    Bin #2: [10, 26, 27], sum=63

    Partitioning items with names:
    >>> from prtpy import partition, outputtypes as out
    >>> partition(algorithm=best_ckk_partition, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['a', 'g'], ['b', 'f'], ['c', 'd', 'e']]
    >>> partition(algorithm=best_ckk_partition, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    [16.0, 16.0]
    """
    binner = bins.get_binner()
    numitems = len(items)
    logger.info("\nComplete-Karmarkar-Karp Partitioning of %d items into %d parts.", numitems, binner.numbins)
    items = sorted(items, reverse=True, key=binner.valueof)

    stack = []  #: List[List[Tuple[int, int, Bins, List[int]]]]
    first_heap = []
    heap_count = count()  # To avoid ambiguity in heaps
    for item in items:
        new_bins = bins.clone().add_item_to_bin(item=item, bin_index=(bins.num - 1))
        heapq.heappush(            first_heap, (-valueof(item), next(heap_count), new_bins))
    stack.append(first_heap)

    best_difference_so_far = -np.inf  # maybe insert here upper bound constraint : best = upper
    while stack:
        current_heap = stack.pop()

        # if could lead to better partition - maybe insert here upper bound constraint
        lower_bound = _possible_partition_difference_lower_bound(current_heap, binner.numbins) 
        if lower_bound <= best_difference_so_far:
            continue

        # if could lead to complete partition
        if len(current_heap) == 1:
            # diff and best are non-positives numbers
            diff = current_heap[0][0]

            if diff > best_difference_so_far:
                best_difference_so_far = diff
                _, _, best_partition_so_far = current_heap[0]
                if diff == 0:
                    return best_partition_so_far
            continue

        # continue create legal part
        _, _, bins1 = heapq.heappop(current_heap)
        _, _, bins2 = heapq.heappop(current_heap)

        tmp_stack_extension = []

        for new_bins in bins1.all_combinations(bins2):
            tmp_heap = current_heap[:]

            diff = max(new_bins.sums) - min(new_bins.sums)
            heapq.heappush(
                tmp_heap, (-diff, next(heap_count), new_bins)
            )

            tmp_stack_extension.append(tmp_heap)
        tmp_stack_extension.sort(key=lambda heap: heap[0])
        stack.extend(tmp_stack_extension)

    best_partition_so_far.sort_by_ascending_sum()
    return best_partition_so_far


if __name__ == '__main__':
    # import doctest
    # (failures, tests) = doctest.testmod(report=True)
    # print("{} failures, {} tests".format(failures, tests))

    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    from prtpy import BinsKeepingContents, BinsKeepingSums, printbins
    print(best_ckk_partition(BinsKeepingContents(2), [4,5,6,7,8]))
