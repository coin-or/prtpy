"""
These functions are being used by the Bin-Completion algorithm for solving the bin packing problem.
See "bin_completion.py" for more details.
"""
import copy
import functools
import math
from itertools import combinations
from typing import List, Iterable
from prtpy import outputtypes as out, Bins, BinsKeepingContents


def list_without_items(original: list, to_remove: Iterable) -> list:
    output = original.copy()
    for obj in to_remove:
        if obj in output:
            output.remove(obj)

    return output


def unique_list(lst: list):
    output = []
    for element in lst:
        if element not in output:
            output.append(element)
    return output


def lower_bound(binsize: float, items: List) -> float:
    return math.ceil(sum(items)/binsize)


def l2_lower_bound(binsize: float, items: List) -> float:
    copy_items = items.copy()

    copy_items.sort(reverse=True)

    total_sum = sum(copy_items)
    estimated_waste = 0
    capacity = binsize

    for x in copy_items:
        r = capacity - x
        smaller_elements = []
        for i in range(len(copy_items) - 1, 0, -1):
            if copy_items[i] > r:
                break
            smaller_elements.append(copy_items[i])

        s = sum(smaller_elements)
        if s == r:
            for element in smaller_elements:
                copy_items.remove(element)
            capacity = binsize
        elif s < r:
            estimated_waste += r - s
            for element in smaller_elements:
                copy_items.remove(element)
            capacity = binsize
        else:
            for element in smaller_elements:
                copy_items.remove(element)
            capacity = binsize - (s - r)

    return (estimated_waste + total_sum) / binsize


def l3_lower_bound(binsize: float, items: List) -> float:
    copy_items = items.copy()
    best_lower_bound = l2_lower_bound(binsize, copy_items)
    for i in range(len(items)):
        copy_items.remove(min(copy_items))
        new_l2 = l2_lower_bound(binsize, copy_items)
        if new_l2 > best_lower_bound:
            best_lower_bound = new_l2

    return best_lower_bound

def find_undominated_pairs(x: int, y: int, items: List, binsize: int) -> List:
    start = 0;
    end = len(items) - 1
    undominated_pairs = []

    while (start < end):
        sum = items[start] + items[end]
        if x + sum > binsize:
            start += 1
        elif sum <= y:
            end -= 1
        else:
            undominated_pairs.append([items[start], items[end]])
            start += 1
            end -= 1

    return undominated_pairs


class BinBranch:
    def __init__(self, items: list, bins: Bins, bin_index: int):
        self.items = items
        self.bins = bins
        self.bin_index = bin_index

def find_bin_completions(x: int, items: list, binsize: int):
    """
        Test 1:
        >>> find_bin_completions(99, [94,79,64,50,44,43,37,32,19,18,7,3], 100)
        []

        Test 2:
        >>> find_bin_completions(94, [79,64,50,44,43,37,32,19,18,7,3], 100)
        [[3]]

        Test 3:
        >>> find_bin_completions(79, [64,50,44,43,37,32,19,18,7], 100)
        [[19], [18], [7]]

        Test 4:
        >>> find_bin_completions(64, [64,50,44,43,37,32,18,7], 100)
        [[32], [18, 7], [18], [7]]

        Test 5:
        >>> find_bin_completions(50, [44,43,37,18,7], 100)
        [[43, 7], [44], [37, 7], [43], [37], [18, 7], [18], [7]]
    """
    if not items:
        return []

    y = next((item for item in items if x + item <= binsize), 0)

    if y == 0:
        return []

    found_completions = [[y]]

    for i in range(len(items)+1):
        feasible_completions = filter(lambda s: x + sum(s) <= binsize, combinations(items, i))
        for fc in feasible_completions:
            constant_elements = x + sum(fc)
            items_left = list_without_items(items, fc)
            undominated_pairs = find_undominated_pairs(constant_elements, y, items_left, binsize)
            if undominated_pairs:
                found_completions.extend(undominated_pairs)
            elif fc:
                found_completions.append(list(fc))


    return unique_list(sorted(found_completions, key=sum, reverse=True))


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())