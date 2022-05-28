"""
    Partition the numbers using the improved recursive number partitioning algorithm
    Taken help from:

    Taken from the "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,
    Algorithm number in Paper: 3.0
    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132
    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""
import copy
import itertools
from typing import Callable, List

import numpy as np

from prtpy import Bins
from prtpy.bins import BinsKeepingContents
from prtpy.objectives import get_complementary
from prtpy.partitioning.rnp import rnp


def irnp(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the improved recursive number partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> list(irnp(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).sums)
    [32.0, 36.0]

    >>> irnp(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).bins
    [[95, 15, 25], [75, 85, 5]]

    >>> irnp(BinsKeepingContents(3), items=[5, 8, 6, 4, 7]).bins
    [[4, 7], [5, 6], [8]]

    >>> list(rnp(BinsKeepingContents(3), items=[95, 15, 75, 25, 85, 5]).sums)  # need to debug
    [163.0, 140.0]

    """
    k = bins.num
    if k == 0:
        return bins
    elif k == 1:
        return [bins.add_item_to_bin(item=item, bin_index=0) for item in items]

    rnp_bins = list(rnp(bins, items, valueof="list"))
    optimal_number_separately = get_best_partition_with_number_separately(items)
    best_partition = min(rnp_bins, optimal_number_separately, key=diff_sums)

    for index, partition in enumerate(best_partition):
        for item in partition:
            bins.add_item_to_bin(item=item, bin_index=index)
    return bins


def diff_sums(items: list) -> int:
    sum_diff = 0
    min_diff = np.inf
    for item in items:
        sum_diff += sum(item)
        if min_diff > sum(item):
            min_diff = sum(item)
    return (sum_diff - min_diff) / len(items)


def get_best_partition_with_number_separately(items: list):
    differences = {}
    for item in items:
        temp_items = copy.copy(items)
        temp_items.remove(item)
        diff = abs(sum(temp_items) - item)
        differences[item] = diff
    best_item = min(differences, key=differences.get)
    return [[best_item], get_complementary(items=items, sub_items=[best_item])]


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
