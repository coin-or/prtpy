"""
Authors: Jonathan Escojido & Samuel Harroch
Since = 03-2022

Credit: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
        https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning

"""
from typing import Iterator, List, Tuple, Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins, Binner, BinsKeepingContents, BinsKeepingSums
import logging, numpy as np

from prtpy.partitioning.karmarkar_karp_sy import BinsSortedByMaxDiff


logger = logging.getLogger(__name__)


def _possible_partition_difference_lower_bound(current_heap: List[Tuple[int, int, Bins, List[int]]], numbins: int) -> int:
    """
    This function check if from the current node we can yield to a better partition or not by checking the
    best difference we can reach from this node.
    """
    logger.info("  A heap with %d partitions", len(current_heap))
    sums_flattened = [size for binsarray in current_heap.iterator() for size in current_heap.binner.sums(binsarray)]
    max_sums_flattened = max(sums_flattened)
    sum_sums_flattened = sum(sums_flattened)
    lower_bound = -(max_sums_flattened - (sum_sums_flattened - max_sums_flattened) // (numbins - 1))
    logger.info(f"    Max sums = {max_sums_flattened}, sum of all sums = {sum_sums_flattened}, lower_bound = {lower_bound}")
    return lower_bound



def optimal(bins: Bins, items: List[int],  valueof: Callable=lambda x: x, binner:Binner=None, numbins:int=None) -> Bins:
    """
    Finds a partition in which the largest sum is minimal, using the Complete Greedy algorithm.

    :param objective: represents the function that should be optimized. Default is minimizing the difference between bin sums.
    :param time_limit: determines how much time (in seconds) the function should run before it stops. Default is infinity.

    >>> from prtpy import BinsKeepingContents, BinsKeepingSums, printbins
    >>> printbins(optimal(BinsKeepingContents(2), [4,5,6,7,8]))
    Bin #0: [4, 5, 6], sum=15.0
    Bin #1: [7, 8], sum=15.0

    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> printbins(optimal(BinsKeepingContents(3), walter_numbers))
    Bin #0: [16, 39], sum=55.0
    Bin #1: [13, 46], sum=59.0
    Bin #2: [10, 26, 27], sum=63.0

    >>> optimal(BinsKeepingSums(5), items=[1, 2, 3, 4, 5])
    [1.0, 2.0, 3.0, 4.0, 5.0]

    >>> optimal(BinsKeepingSums(5), items=[1,9,8,2,3,7,6,5,4])
    [9.0, 9.0, 9.0, 9.0, 9.0]

    Partitioning items with names:
    >>> from prtpy import partition, outputtypes as out
    >>> partition(algorithm=optimal, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['a', 'g'], ['c', 'd', 'e'], ['b', 'f']]
    >>> partition(algorithm=optimal, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    [16.0, 16.0]
    """
    if binner is None: 
        binner = bins.get_binner()
    if numbins is None:
        numbins = binner.numbins

    numitems = len(items)
    logger.info("\nComplete-Karmarkar-Karp Partitioning of %d items into %d parts.", numitems, numbins)
    items = sorted(items, reverse=True, key=binner.valueof)

    stack = []  #: List[List[Tuple[int, int, Bins, List[int]]]]
    first_heap = BinsSortedByMaxDiff(binner)
    for item in items:
        new_bins = binner.add_item_to_bin(binner.new_bins(numbins), item=item, bin_index=numbins-1)
        first_heap.push(new_bins)
    stack.append(first_heap)

    best_difference_so_far = -np.inf  # maybe insert here upper bound constraint : best = upper
    while stack:
        current_heap = stack.pop()

        # if could lead to better partition - maybe insert here upper bound constraint
        lower_bound = _possible_partition_difference_lower_bound(current_heap, numbins) 
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

        # continue create legal part
        bins1 = current_heap.pop()
        bins2 = current_heap.pop()

        tmp_stack_extension = []

        # for new_bins in bins1.all_combinations(bins2):
        for new_bins in binner.all_combinations(bins1, bins2):
            tmp_heap = current_heap.clone()
            tmp_heap.push(new_bins)
            tmp_stack_extension.append(tmp_heap)
        tmp_stack_extension.sort(key=lambda heap: heap.topdiff())
        stack.extend(tmp_stack_extension)

    binner.sort_by_ascending_sum(best_partition_so_far)
    return best_partition_so_far



def generator(bins: Bins, items: List[int],  valueof: Callable=lambda x: x, best_difference_so_far:float = -np.inf, binner:Binner=None) -> Iterator[Bins]:
    """
    Iterator as mentioned in CKK algorithms which return better partition than the one found so far.
    best:  negative upper bound on the difference.
            -np.inf (default): yield better partitions than the one found so far.
           other: yield partitions with upper bound "best" on the difference.

    >>> from prtpy import partition
    >>> for part in generator(BinsKeepingSums(4), items=[1,2,3,3,5,9,9]): part
    [7.0, 7.0, 9.0, 9.0]
    >>> for part in generator(BinsKeepingContents(4), items=[1, 3, 3, 4, 4, 5, 5, 5]): part
    ([6.0, 8.0, 8.0, 8.0], [[1, 5], [4, 4], [3, 5], [3, 5]])
    """
    if binner is None: 
        binner = bins.get_binner()

    numitems = len(items)
    logger.info("\nComplete-Karmarkar-Karp Partitioning of %d items into %d parts.", numitems, binner.numbins)
    items = sorted(items, reverse=True, key=binner.valueof)

    stack = []  #: List[List[Tuple[int, int, Bins, List[int]]]]
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
                f"False means we search for partitions with bounded difference.")
    while stack:
        current_heap = stack.pop()

        # if could lead to better partition - maybe insert here upper bound constraint
        lower_bound = _possible_partition_difference_lower_bound(current_heap, binner.numbins) 
        if lower_bound <= best_difference_so_far:
            continue

        logger.info(f"This partition/s could lead to a better partition found so far: {current_heap}")

        # if could lead to legal partition
        if len(current_heap) == 1:

            # diff and best are non-positives numbers
            diff = current_heap.topdiff()

            logger.info(f"We arrive to a legal partition. Is it better than the best one found so far?\n"
                        f"is this partition diff ={-diff} < from the best one = {-best_difference_so_far} ?")

            if diff > best_difference_so_far: # consolidate if geq
                logger.info("We found a better partition!!! Continue to search for better partitions....")
                if isBest:
                    best_difference_so_far = diff
                best_partition_so_far =  current_heap.top()
                yield best_partition_so_far
                if diff == 0:
                    logger.info("Perfect partition is found!!!")
                    return
            continue

        logger.info("Combine between the partitions in order to create legal partition.")
        # continue create legal part
        bins1 = current_heap.pop()
        bins2 = current_heap.pop()

        tmp_stack_extension = []
        for new_bins in binner.all_combinations(bins1, bins2):
            tmp_heap = current_heap.clone()
            tmp_heap.push(new_bins)
            tmp_stack_extension.append(tmp_heap)
        tmp_stack_extension.sort(key=lambda heap: heap.topdiff())
        stack.extend(tmp_stack_extension)


if __name__ == '__main__':
    import doctest, sys
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    if failures>0: 
        sys.exit(1)

    # logger.setLevel(logging.INFO)
    # logger.addHandler(logging.StreamHandler())
    # from prtpy import BinsKeepingContents, BinsKeepingSums, printbins
    # print(optimal(BinsKeepingContents(2), [4,5,6,7,8]))
