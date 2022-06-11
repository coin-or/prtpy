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
from prtpy import Bins
from prtpy.bins import BinsKeepingContents
from prtpy.partitioning.ckk import ckk
from prtpy.partitioning.rnp import rnp
from prtpy.utils import base_check_bins, is_all_lists_are_different, all_in, get_best_best_k_combination, max_largest, \
    get_best_partition, calculate_diff, get_sum_of_max_subset, get_largest_number


def irnp(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the improved recursive number partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> list(irnp(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).sums)
    [35.0, 33.0]

    >>> irnp(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).bins
    [[85, 75], [95, 25, 15, 5]]

    >>> irnp(BinsKeepingContents(3), items=[5, 8, 6, 4, 7]).bins
    [[8], [7, 4], [6, 5]]

    >>> list(rnp(BinsKeepingContents(3), items=[95, 15, 75, 25, 85, 5]).sums)
    [100.0, 100.0, 100.0]

    >>> rnp(BinsKeepingContents(2), items=[1, 6, 2, 3, 4, 7]).bins
    [[7, 3, 2], [6, 4, 1]]

    >>> rnp(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).bins
    [[17, 11, 8], [18, 12, 2]]

    >>> list(rnp(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).sums)
    [160.0, 140.0]

    >>> rnp(BinsKeepingContents(4), items=[3, 6, 13, 20, 30, 40, 73]).bins
    [[73], [40], [30, 6], [20, 13, 3]]

    >>> rnp(BinsKeepingContents(5), items=[1, 2, 3, 4, 5]).bins
    [[1], [2], [3], [4], [5]]

    >>> rnp(BinsKeepingContents(2), items=[1, 2]).bins
    [[1], [2]]

    >>> rnp(BinsKeepingContents(1), items=[1, 6, 2, 3, 4, 7]).bins
    [[1, 6, 2, 3, 4, 7]]

    >>> rnp(BinsKeepingContents(0), items=[number for number in range(10)]).bins
    []

    """
    k = bins.num
    bins, flag = base_check_bins(bins=bins, items=items, valueof=valueof)
    if flag:
        return bins
    items.sort(reverse=True, key=valueof)

    all_combinations = []
    for i in range(1, len(items) - k + 2):
        all_combinations.extend([list(combination) for combination in itertools.combinations(items, i)])

    flag = False
    best_k_combination = []
    all_k_combinations = []
    for combination in itertools.combinations(all_combinations, k):
        if is_all_lists_are_different(combination) and all_in(combination, items):
            all_k_combinations.append(list(combination))

            # found a optimal partition or maximum subset sum equals to largest number
            if calculate_diff(combination) == 0 or get_sum_of_max_subset(combination) == get_largest_number(
                    combination):
                best_k_combination = combination
                flag = True
                break

    # working as irnp by take the optimal k combination
    if not flag:
        best_k_combination = get_best_best_k_combination(k_combinations=all_k_combinations)

    for index, combination_items in enumerate(best_k_combination):
        for item in combination_items:
            bins.add_item_to_bin(item=item, bin_index=index)
    return bins


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
