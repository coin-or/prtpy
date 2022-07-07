"""
Authors: Jonathan Escojido & Samuel Harroch
Since = 03-2022

Credit: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
        https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning

"""
import numpy as np
from typing import Iterator, List, Tuple, Callable, List
from prtpy import outputtypes as out, objectives as obj, Bins, Binner, BinnerKeepingContents, BinnerKeepingSums, printbins, BinsKeepingContents, BinsKeepingSums
import heapq
from itertools import count
import logging

from prtpy.partitioning.karmarkar_karp_sy import BinsSortedByMaxDiff

logger = logging.getLogger(__name__)

def _possible_partition_difference_lower_bound(current_heap: BinsSortedByMaxDiff, numbins: int) -> int:
    """
    This function checks if from the current node we can get to a better partition or not.
    It checks the best difference we can reach from this node.
    """
    logger.info("The current heap: %s", current_heap)
    sums_flattened = [size for bins in current_heap.iterator() for size in current_heap.binner.sums(bins)]
    max_sums_flattened = max(sums_flattened)
    sum_sums_flattened = sum(sums_flattened)
    logger.info(f"max sums sizes = {max_sums_flattened}, sum of all sums = {sum_sums_flattened}")
    return -(max_sums_flattened - (sum_sums_flattened - max_sums_flattened) // (numbins - 1))


def ckk(bins: Bins,items: List[int],  valueof: Callable=lambda x: x, best_difference_so_far:float = -np.inf) -> Iterator[Bins]:
    """
    Iterator as mentioned in CKK algorithms which return better partition than the one found so far.
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
    binner = bins.get_binner()
    numitems = len(items)
    logger.info("\nComplete-Karmarkar-Karp Partitioning of %d items into %d parts.", numitems, binner.numbins)
    items = sorted(items, reverse=True, key=binner.valueof)

    stack = []  #: List[BinsSortedByMaxDiff]
    first_heap = BinsSortedByMaxDiff(binner)
    for item in items:
        new_bins = binner.add_item_to_bin(binner.new_bins(), item=item, bin_index=binner.numbins-1)
        first_heap.push(new_bins)
    stack.append(first_heap)

    logger.info(f"we create the stack - all stack items are possibles branches in the tree (we then combine them in all possible ways). "
                f"The stack: {stack}")

    isBest = True if best_difference_so_far == -np.inf else False
    logger.info(f"isBest= {isBest}, "
                f"True means we search for the best partition, "
                f"False means we search for partitions with a bounded difference.")

    while stack:
        current_heap = stack.pop()

        # if could lead to better partition - maybe insert here upper bound constraint
        lower_bound = _possible_partition_difference_lower_bound(current_heap, binner.numbins) 
        if lower_bound <= best_difference_so_far:
            continue

        logger.info(f"This heap could lead to a better partition than found so far: {current_heap}")

        # if could lead to a complete partition
        if len(current_heap) == 1:
            # diff and best are non-positives numbers
            diff = current_heap.topdiff()

            logger.info(f"We arrive to a legal partition. Is it better than the best one found so far?\n"
                        f"is this partition diff ={-diff} < from the best one = {-best_difference_so_far} ?")

            if diff > best_difference_so_far: # consolidate if geq
                logger.info("We found a better partition!!! Continue to search for better partitions....")
                if isBest:
                    best_difference_so_far = diff
                complete_partition = current_heap.top()
                yield complete_partition
                if diff == 0:
                    logger.info("Perfect partition is found!!!")
                    return
            continue

        logger.info("Combine between the partitions in order to create complete partitions.")

        bins1 = current_heap.pop()
        bins2 = current_heap.pop()

        tmp_stack_extension = []
        for new_bins in binner.all_combinations(bins1, bins2):
            tmp_heap = current_heap.clone()
            tmp_heap.push(new_bins)
            tmp_stack_extension.append(tmp_heap)
        tmp_stack_extension.sort(key=lambda heap: heap.topdiff())
        stack.extend(tmp_stack_extension)



def best_ckk_partition(bins: Bins,items: List[int],  valueof: Callable=lambda x: x) -> Bins:
    binner = bins.get_binner()
    numitems = len(items)
    logger.info("\nComplete-Karmarkar-Karp Partitioning of %d items into %d parts.", numitems, binner.numbins)
    items = sorted(items, reverse=True, key=binner.valueof)

    stack = []  #: List[BinsSortedByMaxDiff]
    first_heap = BinsSortedByMaxDiff(binner)
    for item in items:
        new_bins = binner.add_item_to_bin(binner.new_bins(), item=item, bin_index=binner.numbins-1)
        first_heap.push(new_bins)
    stack.append(first_heap)

    # maybe insert here upper bound constraint : best = upper
    best_difference_so_far = -np.inf
    while stack:
        current_heap = stack.pop()

        # if could lead to better partition - maybe insert here upper bound constraint
        lower_bound = _possible_partition_difference_lower_bound(current_heap, binner.numbins) 
        if lower_bound <= best_difference_so_far:
            continue

        # if could lead to complete partition
        if len(current_heap) == 1:
            # diff and best are non-positives numbers
            diff = current_heap.topdiff()

            if diff > best_difference_so_far:
                best_difference_so_far = diff
                best_partition_so_far =  current_heap.top()
                if diff == 0:
                    return best_partition_so_far
            continue

        # continue creating the complete partition
        bins1 = current_heap.pop()
        bins2 = current_heap.pop()

        tmp_stack_extension = []

        for new_bins in binner.all_combinations(bins1, bins2):
            tmp_heap = current_heap.clone()
            tmp_heap.push(new_bins)
            tmp_stack_extension.append(tmp_heap)
        tmp_stack_extension.sort(key=lambda heap: heap.topdiff())
        stack.extend(tmp_stack_extension)

    return best_partition_so_far


if __name__ == '__main__':
    # import doctest
    # (failures, tests) = doctest.testmod(report=True)
    # print("{} failures, {} tests".format(failures, tests))

    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    from prtpy import BinsKeepingContents, BinsKeepingSums, printbins
    printbins(best_ckk_partition(BinsKeepingContents(2), [4,5,6,7,8]))
