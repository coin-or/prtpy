"""
Authors: Jonathan Escojido & Samuel Harroch
Since = 03-2022

Credit: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
        https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning

"""
from math import inf
from time import time
from typing import Iterator, List, Tuple, Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins, BinsKeepingContents, BinsKeepingSums
import heapq
from itertools import count
import logging
from copy import deepcopy


logger = logging.getLogger(__name__)


def _possible_partition_difference_lower_bound(node: List[Tuple[int, int, Bins, List[int]]], numBins: int) -> int:
    """
    This function check if from the current node we can yield to a better partition or not by checking the
    best difference we can reach from this node.
    """
    logger.info("the current node: ", node)

    sums_flattened = [size for partition in node for size in partition[3]]
    max_sums_flattened = max(sums_flattened)
    logger.info(f"max sums sizes = {max_sums_flattened}, sum of all sums = {sum(sums_flattened)}")

    return -(max_sums_flattened - (sum(sums_flattened) - max_sums_flattened) // (numBins - 1))


def ckk(bins: Bins,items: List[int],  valueof: Callable=lambda x: x, best:float = -inf) -> Iterator[Bins]:
    """
    Iterator as mentions in CKK algorithms which return better partition than the one found so far.
    best:  negative upper bound on the difference.
            -inf (default): yield better partitions than the one found so far.
           other: yield partitions with upper bound "best" on the difference.

    >>> from prtpy import partition
    >>> for part in ckk(BinsKeepingSums(4), items=[1,2,3,3,5,9,9]): part
    Bin #0: sum=7.0
    Bin #1: sum=7.0
    Bin #2: sum=9.0
    Bin #3: sum=9.0
    >>> for part in ckk(BinsKeepingContents(4), items=[1, 3, 3, 4, 4, 5, 5, 5]): part.bins
    [[1, 5], [3, 5], [3, 5], [4, 4]]
    """
    stack = [[]]

    heap_count = count()  # To avoid ambiguity in heaps
    for item in items:
        new_bins = deepcopy(bins).add_item_to_bin(item=item, bin_index=(bins.num - 1))

        heapq.heappush(
            stack[0], (-valueof(item), next(heap_count), new_bins, new_bins.sums)
        )

    logger.info(f"we create the stack - all stack items are possibles branches in the tree (we then combine them in all possible ways). "
                f"The stack: {stack}")

    # best = -inf
    isBest = True if best == -inf else False
    logger.info(f"isBest= {isBest}, "
                f"True means we search for the best partition, "
                f"False means we search for partitions with bounded difference.")
    while stack:
        partitions = stack.pop()

        # if could lead to better partition - maybe insert here upper bound constraint
        if _possible_partition_difference_lower_bound(partitions, bins.num) <= best:
            continue

        logger.info(f"This partition/s could lead to a better partition found so far: {partitions}")

        # if could lead to legal partition
        if len(partitions) == 1:

            # diff and best are non-positives numbers
            diff = partitions[0][0]

            logger.info(f"We arrive to a legal partition. Is it better than the best one found so far?\n"
                        f"is this partition diff ={-diff} < from the best one = {-best} ?")

            if diff > best: # consolidate if geq
                logger.info("We found a better partition!!! Continue to search for better partitions....")
                if isBest:
                    best = diff
                _, _, final_partition, final_sums = partitions[0]
                yield final_partition

                if diff == 0:
                    logger.info("Perfect partition is found!!!")
                    return
            continue

        logger.info("Combine between the partitions in order to create legal partition.")
        # continue create legal part
        _, _, bin1, bin1_sums = heapq.heappop(partitions)
        _, _, bin2, bin2_sums = heapq.heappop(partitions)

        tmp_stack_extension = []

        for new_bins in bin1.combinations(bin2):
            tmp_partitions = partitions[:]

            diff = max(new_bins.sums) - min(new_bins.sums)
            heapq.heappush(
                tmp_partitions, (-diff, next(heap_count), new_bins, new_bins.sums)
            )

            tmp_stack_extension.append(tmp_partitions)

        stack.extend(sorted(tmp_stack_extension))


def best_ckk_partition(bins: Bins,items: List[int],  valueof: Callable=lambda x: x) -> Bins:
    stack = [[]]  #: List[List[Tuple[int, int, Bins, List[int]]]]

    heap_count = count()  # To avoid ambiguity in heaps
    for item in items:
        new_bins = deepcopy(bins).add_item_to_bin(item=item, bin_index=(bins.num - 1))

        heapq.heappush(
            stack[0], (-valueof(item), next(heap_count), new_bins, new_bins.sums)
        )
    # maybe insert here upper bound constraint : best = upper
    best = -inf
    while stack:
        partitions = stack.pop()

        # if could lead to better partition - maybe insert here upper bound constraint
        if _possible_partition_difference_lower_bound(partitions, bins.num) <= best:
            continue

        # if could lead to legal partition
        if len(partitions) == 1:
            # diff and best are non-positives numbers
            diff = partitions[0][0]

            if diff > best:
                best = diff
                _, _, final_partition, final_sums = partitions[0]
                best_partition =  final_partition

                if diff == 0:
                    return best_partition
            continue

        # continue create legal part
        _, _, bin1, bin1_sums = heapq.heappop(partitions)
        _, _, bin2, bin2_sums = heapq.heappop(partitions)

        tmp_stack_extension = []

        for new_bins in bin1.combinations(bin2):
            tmp_partitions = partitions[:]

            diff = max(new_bins.sums) - min(new_bins.sums)
            heapq.heappush(
                tmp_partitions, (-diff, next(heap_count), new_bins, new_bins.sums)
            )

            tmp_stack_extension.append(tmp_partitions)

        stack.extend(sorted(tmp_stack_extension))

    return best_partition


if __name__ == '__main__':

    # logger.setLevel(logging.INFO)
    # logger.addHandler(logging.StreamHandler())

    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
