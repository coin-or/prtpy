"""
These functions are being used by the Bin-Completion algorithm for solving the bin packing problem.
See "bin_completion.py" for more details.

Authors: Avshalom Avraham & Tehila Ben-Kalifa
Since: 05-2022
"""
import math
from itertools import combinations
from typing import List, Iterable
import logging
from prtpy.bins import Bins



# A simple class to store a state of bins arrangement.
# We keep the current bin arrangement and index of the next bin, as well as the items left to arrange in those bins.
class BinBranch:
    def __init__(self, items: list, bins: Bins, bin_index: int):
        self.items = items
        self.bins = bins
        self.bin_index = bin_index


# Returns a new list which is a copy of 'original' but without the items in 'to_remove' if they existed.
def list_without_items(original: list, to_remove: Iterable) -> list:
    output = original.copy()
    for obj in to_remove:
        if obj in output:
            output.remove(obj)

    return output


# Returns a new list which is a copy of 'lst' but without duplicate items.
def unique_list(lst: list) -> list:
    output = []
    for element in lst:
        if element not in output:
            output.append(element)
    return output


# Calculates the lower bound of bins for bin packing problem.
def lower_bound(binsize: float, items: List) -> float:
    return math.ceil(sum(items) / binsize)


# Calculates the L2 lower bound using Martello and Toth algorithm.
# See article for details.
def l2_lower_bound(binsize: float, items: List) -> float:
    copy_items = items.copy()

    copy_items.sort(reverse=True)

    total_sum = sum(copy_items)
    estimated_waste = 0
    capacity = binsize

    for x in copy_items:
        # 'r' is the residual capacity in a bin.
        r = capacity - x

        # We need to find all the items smaller than r
        smaller_elements = []

        # We go through the items from end to beginning because they are sorted.
        for i in range(len(copy_items) - 1, 0, -1):
            if copy_items[i] > r:
                break
            smaller_elements.append(copy_items[i])

        # See article for details about conditions
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


# Calculates the L3 lower bound using Martello and Toth algorithm.
# See article for details.
def l3_lower_bound(binsize: float, items: List) -> float:
    copy_items = items.copy()
    best_lower_bound = l2_lower_bound(binsize, copy_items)

    # We successively prune the smallest element and calculate L2 lower bound each time.
    # At the end we return the highest lower bound.
    for i in range(len(items)):
        copy_items.remove(min(copy_items))
        new_l2 = l2_lower_bound(binsize, copy_items)
        if new_l2 > best_lower_bound:
            best_lower_bound = new_l2

    return best_lower_bound


# Returns a list of the pairs undominated by y (highest element that fits the bin with x).
# See article for details.
def find_undominated_pairs(x: int, y: int, items: List, binsize: int) -> List:
    """
            Test 1:
            >>> find_undominated_pairs(94, 3, [79,64,50,44,43,37,32,19,18,7,3], 100)
            []

            Test 2:
            >>> find_undominated_pairs(79, 19, [79,64,50,44,43,37,32,19,18,7,3], 100)
            [[18, 3]]

            Test 3:
            >>> find_undominated_pairs(64, 32, [50,44,43,37,32,19,18,7], 100)
            []

            Test 4:
            >>> find_undominated_pairs(50, 44, [44,43,37,32,18,7], 100)
            [[43, 7], [32, 18]]

            Test 5:
            >>> find_undominated_pairs(44, 43, [43,37,18,7], 100)
            [[43, 7], [37, 18]]
        """
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


# Returns all the possible completions of undominated items for the bin containing x.
# See article for details.
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
    if x > binsize:
        raise ValueError(f"Item 'x' has size {x} which is larger than the bin size {binsize}.")

    # No more items to add.
    if not items:
        logging.info(f"Items list is empty.")
        return []

    # We find the largest element y for which (x+y) <= binsize.
    y = next((item for item in items if x + item <= binsize), 0)

    # No element fits the bin with x.
    if y == 0:
        logging.info(f"No other element fits with {x}.")
        return []

    # The largest element is always undominated because no other element can contain it.
    found_completions = [[y]]

    # We go through all combinations of items subsets of all sizes, that fits the bin containing x.
    for i in range(len(items) + 1):
        feasible_completions = filter(lambda s: x + sum(s) <= binsize, combinations(items, i))

        # For every subset that fits the bin containing x, we find undominated pair of items to add to our completions.
        # When we take subset of size 1 and find a pair, it's like finding a triplet.
        # When we take subset of size 2 and find a pair, it's like finding a quadruple etc.
        for fc in feasible_completions:
            constant_elements = x + sum(fc)
            items_left = list_without_items(items, fc)
            undominated_pairs = find_undominated_pairs(constant_elements, y, items_left, binsize)

            # We add the undominated pairs to possible completions.
            # if none were found - we add the subset fc as a possible completions.
            if undominated_pairs:
                found_completions.extend(undominated_pairs)
            elif fc:
                found_completions.append(list(fc))

    # Return the possible completions without duplicated, sorted in descending order by their sum.
    return unique_list(sorted(found_completions, key=sum, reverse=True))


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
