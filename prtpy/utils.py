import itertools
from copy import deepcopy
from typing import List, Callable
import random
import numpy as np

from prtpy import Bins, BinsKeepingContents


def base_check_bins(bins: Bins, items: List[any], valueof: Callable = lambda x: x) -> (Bins, bool):
    flag = False
    k = bins.num
    if k == 0:
        flag = True
    elif k == 1:
        for item in items:
            bins.add_item_to_bin(item=item, bin_index=0)
        flag = True

    if len(items) == k:
        for index, item in enumerate(items):
            bins.add_item_to_bin(item=item, bin_index=index)
        flag = True

    return bins, flag


def calculate_diff(items):
    diff_sum = 0
    for combination in itertools.combinations(items, 2):
        if len(combination[0]) == 0 or len(combination[1]) == 0:
            break
        else:
            diff_sum += abs(sum(combination[0]) - sum(combination[1]))
    return diff_sum


def get_best_best_k_combination(k_combinations):
    best_combination = []
    minimum_diff = np.inf
    flag = True
    for k_combination in k_combinations:
        diff_sum = 0
        for combinations in itertools.combinations(k_combination, 2):
            if len(combinations[0]) == 0 or len(combinations[1]) == 0:
                flag = False
                break
            else:
                flag = True
            diff_sum += abs(sum(combinations[0]) - sum(combinations[1]))
        if flag and diff_sum < minimum_diff:
            minimum_diff = diff_sum
            best_combination = k_combination
    return best_combination


def get_sum_of_max_subset(combination):
    """
    >>> get_sum_of_max_subset(combination=[[5, 6], [1, 3], [2, 20]])
    22
    """
    if len(combination) == 0:
        return 0
    max_subset = combination[0]
    max_sum = 0
    for combination_set in combination:
        if sum(combination_set) > max_sum:
            max_sum = sum(combination_set)
            max_subset = combination_set
    return sum(max_subset)


def get_largest_number(combination):
    """
    >>> get_largest_number(combination=[[5, 6], [1, 3], [2, 20]])
    20
    """
    if len(combination) == 0:
        return 0
    max_number = 0
    for combination_set in combination:
        if max(combination_set) > max_number:
            max_number = max(combination_set)
    return max_number


def all_in(sub_items: list, items) -> bool:
    """
    >>> all_in(sub_items=[[1],[2],[3]], items=[1,2,3])
    True

    >>> all_in(sub_items=[[1],[2]], items=[1,2,3])
    False

    """
    copy_items = deepcopy(items)
    for items in sub_items:
        for item in items:
            copy_items.remove(item)
    return len(copy_items) == 0


def is_all_lists_are_different(list_of_lists) -> bool:
    """
    >>> is_all_lists_are_different([[1, 2], [2, 3]])
    False

    >>> is_all_lists_are_different([[1, 2], [3, 4]])
    True

    >>> is_all_lists_are_different([[1, 2], [3, 4], [5, 6]])
    True

    >>> is_all_lists_are_different([[1, 2], [3, 4], [5, 6], [7, 8]])
    True

    >>> is_all_lists_are_different([[1, 2], [3, 4], [5, 6, 1]])
    False

    >>> is_all_lists_are_different([[1, 2, 6], [3, 4, 6], [5, 6]])
    False

    >>> is_all_lists_are_different([[1], [9, 5, 1, 2], [3, 4, 5, 7, 8, 9, 9, 9, 9, 9, 1], [2, 2, 2, 2, 9, 1, 5, 5, 5, 5]])
    False

    >>> is_all_lists_are_different([[number for number in range(3)] for _ in range(random.randint(50, 100))])
    False

    >>> is_all_lists_are_different([[number for number in range(4)] for _ in range(random.randint(50, 100))])
    False

    >>> is_all_lists_are_different([[number for number in range(5)] for _ in range(random.randint(50, 100))])
    False

    """
    flag = True
    for combinations in itertools.combinations(list_of_lists, 2):
        flag = set.isdisjoint(set(combinations[0]), set(combinations[1]))
        if not flag:
            return False
    return flag


def get_best_partition(bins, k: int):
    best_bins = BinsKeepingContents(k)
    all_bins = []
    for in_bin in bins:
        all_bins.append(in_bin.bins)
    for index, items in enumerate(get_best_best_k_combination(all_bins)):
        for item in items:
            best_bins.add_item_to_bin(item=item, bin_index=index)
    return best_bins


def max_largest(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    maximum_subset_equals_largest_number
    """
    k = bins.num
    all_combinations = []
    for i in range(1, len(items) - k + 1):
        all_combinations.extend([list(combination) for combination in itertools.combinations(items, i)])
    all_k_combinations = [list(combination) for combination in itertools.combinations(all_combinations, k) if
                          is_all_lists_are_different(combination) and all_in(combination, items)]
    for k_combination in all_k_combinations:
        if max(k_combination, key=sum) == largest_number(k_combination):
            for index, items in enumerate(k_combination):
                for item in items:
                    bins.add_item_to_bin(item=item, bin_index=index)
            break
    return bins


def largest_number(combination) -> int:
    max_number = 0
    for items in combination:
        for item in items:
            if max_number < item:
                max_number = item
    return max_number


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
