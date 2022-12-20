import doctest
import math
import operator
import time
from numbers import Number
from typing import List
from prtpy import partition, Binner, BinnerKeepingContents, BinsArray, printbins
from prtpy.partitioning.greedy import greedy
import logging

LOG_FORMAT = "%(levelname)s, time: %(asctime)s ,in: %(funcName)s , line: %(lineno)d: %(message)s "
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def rnp(binner: Binner, numbins: int, items: List[any]) -> BinsArray:
    """
    Based on "Search Strategies for Optimal Multi-Way Number Partitioning", Michael D. Moffitt, 2013
    https://www.ijcai.org/Proceedings/13/Papers/099.pdf

    find optimal partition of the items into numbins bins, such that the maximum sum is minimized.
    uses full branch and bound search with recursive calls.

    >>> printbins(rnp(BinnerKeepingContents(), 2, items=[1,12,8]))
    Bin #0: [12], sum=12.0
    Bin #1: [8, 1], sum=9.0

    >>> printbins(rnp(BinnerKeepingContents(), 2, items=[1,7,9,2]))
    Bin #0: [9, 1], sum=10.0
    Bin #1: [7, 2], sum=9.0

    >>> printbins(rnp(BinnerKeepingContents(), 3, items=[12,8]))
    Bin #0: [12], sum=12.0
    Bin #1: [8], sum=8.0
    Bin #2: [], sum=0.0

    >>> printbins(rnp(BinnerKeepingContents(), 1, items=[2,2]))
    Bin #0: [2, 2], sum=4.0

    >>> sorted(partition(algorithm=rnp, numbins=4, items={"a":1, "b":1, "c":1, "d":1}))
    [['a'], ['b'], ['c'], ['d']]

    >>> partition(algorithm=rnp, numbins=1, items=[6])
    [[6]]
    """

    logger.info(f'rnp with {items=}, {numbins=}')

    # no items
    if len(items) == 0:
        return binner.new_bins(numbins)

    # only one bin
    if numbins == 1:
        all_in_first_bin = binner.new_bins(numbins)
        for item in items:
            binner.add_item_to_bin(all_in_first_bin, item, 0)
        return all_in_first_bin

    # initial partition
    initial_partition = greedy(binner, numbins, items)

    # call the recursive function to calculate the best partitions
    _, _, best_partition = _rnp_recursive(binner.new_bins(numbins), binner, items, 0,
                                          max(map(binner.valueof, items)),
                                          max(binner.sums(initial_partition)), initial_partition)
    return best_partition


def _rnp_recursive(bins: BinsArray, binner: Binner, items: List[any], current_bin: int, min_sum: Number,
                   best_sum: Number, best_partition: BinsArray) -> (BinsArray, Number, BinsArray):
    """
    The main recursive function for rnp. uses some help arguments.
    The second value returned is the best partition of the items.
    The first value returned is a temporary value for the recursive calculations.
    """

    logger.info(f'rnp recursive call with {bins=}, {items=}, {current_bin=}')
    logger.debug(f'{best_sum=}, {min_sum=}, {best_sum=}, {best_partition=}')

    # last bin
    if current_bin == binner.numbins(bins) - 1:
        for item in items:
            binner.add_item_to_bin(bins, item, current_bin)
        current_sum = max(binner.sums(bins))
        if current_sum < best_sum:
            best_sum = current_sum
            best_partition = binner.copy_bins(bins)
        return bins, best_sum, best_partition

    # only one item
    if len(items) == 1:
        binner.add_item_to_bin(bins, *items, current_bin)
        current_sum = max(binner.sums(bins))
        if current_sum < best_sum:
            best_sum = current_sum
            best_partition = binner.copy_bins(bins)
        return bins, best_sum, best_partition

    # empty bins array or no more items
    if current_bin == binner.numbins(bins) or len(items) == 0:
        return bins, best_sum, best_partition

    # sort item - save 1/2 of the checks
    items = sorted(items, key=binner.valueof, reverse=True)

    resulting_partition = bins
    # iterate all options of what numbers to put in the current group
    for binary_partition_number in range(2 ** (len(items) - 1) - 1, -1, -1):
        binary_partition = f'{binary_partition_number:0{len(items) - 1}b}'

        # add items to the current group based on the binary partition
        current_group = [item for label, item in zip(binary_partition, items[1:]) if label == '1'] + [items[0]]
        rest_of_items = [item for label, item in zip(binary_partition, items[1:]) if label == '0']

        # pruning
        current_group_sum = sum([binner.valueof(item) for item in current_group])
        rest_of_items_sum = sum([binner.valueof(item) for item in rest_of_items])
        if current_group_sum > best_sum or \
                rest_of_items_sum > best_sum * (binner.numbins(bins) - current_bin - 1) or \
                any([current_group_sum + binner.valueof(item) <= min_sum for item in rest_of_items]):
            continue

        # add items to the current group based on the binary partition
        bins_copy = binner.copy_bins(bins)
        for item in sorted(current_group, key=binner.valueof, reverse=True):
            binner.add_item_to_bin(bins_copy, item, current_bin)

        # partition the rest of the items to the rst of the bins
        resulting_partition, best_sum, best_partition = _rnp_recursive(bins_copy, binner, rest_of_items,
                                                                       current_bin + 1,
                                                                       current_group_sum, best_sum, best_partition)

        # update, if needed, the best partition and best sum so far
        current_sum = max(binner.sums(resulting_partition))
        if current_sum < best_sum:
            best_sum = current_sum
            best_partition = binner.copy_bins(resulting_partition)

    # return the found partition
    return resulting_partition, best_sum, best_partition


if __name__ == '__main__':
    doctest.testmod()