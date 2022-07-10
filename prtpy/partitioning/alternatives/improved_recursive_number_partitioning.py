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
import itertools
from typing import Callable, List
from prtpy import Bins
from prtpy.bins import BinsKeepingContents
from prtpy.partitioning.alternatives.recursive_number_partitioning_kg import rnp
from prtpy.utils import is_all_lists_are_different, all_in, get_best_best_k_combination, \
    get_sum_of_max_subset, get_largest_number
from prtpy.partitioning.trivial import trivial_partition


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

    >>> list(irnp(BinsKeepingContents(3), items=[95, 15, 75, 25, 85, 5]).sums)
    [100.0, 100.0, 100.0]

    >>> irnp(BinsKeepingContents(2), items=[1, 6, 2, 3, 4, 7]).bins
    [[7, 4], [6, 3, 2, 1]]

    >>> irnp(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).bins
    [[18, 17], [12, 11, 8, 2]]

    >>> list(irnp(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).sums)
    [160.0, 140.0]

    >>> irnp(BinsKeepingContents(4), items=[3, 6, 13, 20, 30, 40, 73]).bins
    [[73], [40], [30], [20, 13, 6, 3]]

    >>> irnp(BinsKeepingContents(3), items=[1, 2, 3, 4, 5, 6]).bins
    [[6, 1], [5, 2], [4, 3]]

    >>> list(irnp(BinsKeepingContents(3), items=[1, 2, 3, 4, 5, 6]).sums)
    [7.0, 7.0, 7.0]

    >>> irnp(BinsKeepingContents(5), items=[1, 2, 3, 4, 5]).bins
    [[1], [2], [3], [4], [5]]

    >>> rnp(BinsKeepingContents(2), items=[1, 2]).bins
    [[1], [2]]

    >>> irnp(BinsKeepingContents(1), items=[1, 6, 2, 3, 4, 7]).bins
    [[1, 6, 2, 3, 4, 7]]

    >>> irnp(BinsKeepingContents(0), items=[number for number in range(10)]).bins
    []

    The following test does not work (found by comparing the output of random inputs with integer programming)
    >>> sorted(irnp(BinsKeepingContents(5), items=[3, 16, 22, 24, 24, 29]).sums)
    [19.0, 22.0, 24.0, 24.0, 29.0]

    """
    if trivial_partition(bins, items):
        return bins

    items.sort(reverse=True, key=valueof)

    all_combinations = []
    for i in range(1, len(items) - bins.num + 2):
        all_combinations.extend([list(combination) for combination in itertools.combinations(items, i)])

    flag = False
    best_k_combination = []
    all_k_combinations = []
    for combination in itertools.combinations(all_combinations, bins.num):
        if is_all_lists_are_different(combination) and all_in(combination, items):
            all_k_combinations.append(list(combination))

            # found a optimal partition or maximum subset sum equals to largest number
            if _calculate_diff(combination) == 0 or get_sum_of_max_subset(combination) == get_largest_number(
                    combination):
                best_k_combination = combination
                flag = True
                break

    # working as irnp by taking the not optimal k combination
    if not flag:
        best_k_combination = get_best_best_k_combination(k_combinations=all_k_combinations)

    # add solution to bins
    for index, combination_items in enumerate(best_k_combination):
        for item in combination_items:
            bins.add_item_to_bin(item=item, bin_index=index)
    return bins


def _calculate_diff(items):
    """
    This function get list of lists and return the different sum error between all the sub-lists

    >>> _calculate_diff(items=([18, 11, 8], [17, 12, 2]))
    6

    >>> _calculate_diff(items=([95], [85, 75, 25, 15, 5]))
    110

    >>> _calculate_diff(items=([95, 15, 5], [85, 75, 25]))
    70

    >>> _calculate_diff(items=([8], [7, 4], [6, 5]))
    6

    >>> _calculate_diff(items=([4], [8, 5], [7, 6]))
    18

    >>> _calculate_diff(items=([95, 5], [85, 15], [75, 25]))
    0

    >>> _calculate_diff(items=([7, 2, 1], [6, 4, 3]))
    3

    >>> _calculate_diff(items=([18], [17, 12, 11, 8, 2]))
    32

    >>> _calculate_diff(items=([4], [6, 3], [5, 2, 1]))
    10

    >>> _calculate_diff(items=([6, 1], [5, 2], [4, 3]))
    0

    """
    diff_sum = 0
    for combination in itertools.combinations(items, 2):
        if len(combination[0]) == 0 or len(combination[1]) == 0:
            break
        else:
            diff_sum += abs(sum(combination[0]) - sum(combination[1]))
    return diff_sum


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
