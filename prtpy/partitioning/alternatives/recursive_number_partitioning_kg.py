"""
Partition the numbers using the recursive number partitioning algorithm

Taken help from:
    "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,

Algorithm number in Paper:
    2.5

Paper link:
    http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132

Author: Kfir Goldfarb
Date: 2022-04-26
Email: kfir.goldfarb@msmail.ariel.ac.il
"""
import itertools
from typing import Callable, List

from prtpy import Bins, BinsKeepingContents
from prtpy.partitioning.alternatives.complete_karmarkar_karp_kg import optimal
from prtpy.utils import all_in, is_all_lists_are_different, get_best_best_k_combination
from prtpy.partitioning.alternatives.trivial import trivial_partition


def rnp(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the recursive number partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> rnp(BinsKeepingContents(2), items=[1, 6, 2, 3, 4, 7]).bins
    [[7, 3, 2], [6, 4, 1]]

    >>> rnp(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).bins
    [[17, 11, 8], [18, 12, 2]]

    >>> list(rnp(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).sums)
    [160.0, 140.0]

    >>> list(rnp(BinsKeepingContents(3), items=[95, 15, 75, 25, 85, 5]).sums)
    [100.0, 100.0, 100.0]

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

    The following test does not work (found by comparing the output of random inputs with integer programming)
    >>> sorted(rnp(BinsKeepingContents(5), items=[3, 16, 22, 24, 24, 29]).sums)
    [19.0, 22.0, 24.0, 24.0, 29.0]
    """
    if trivial_partition(bins, items):
        return bins

    if bins.num == 2:
        return optimal(bins=bins, items=items, valueof=valueof)

    items = sorted(items, reverse=True, key=valueof)

    all_combinations = []
    for i in range(1, len(items) - bins.num + 2):
        all_combinations.extend([list(combination) for combination in itertools.combinations(items, i)])
    all_k_combinations = [list(combination) for combination in itertools.combinations(all_combinations, bins.num) if
                          is_all_lists_are_different(combination) and all_in(combination, items)]
    best_k_combination = get_best_best_k_combination(k_combinations=all_k_combinations)

    for index, combination_items in enumerate(best_k_combination):
        for item in combination_items:
            bins.add_item_to_bin(item=item, bin_index=index)
    return bins


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
