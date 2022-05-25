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


def check_for_dominance(completions: list[list]):
    """
            Test 1:
            >>> check_for_dominance([[3], [2], [1]])
            [[3]]

            Test 2:
            >>> check_for_dominance([[32], [30], [18, 7], [10, 5]])
            [[32], [18, 7]]

            Test 3:
            >>> check_for_dominance([[32], [18, 7], [20, 5]])
            [[32], [18, 7], [20, 5]]

            Test 4:
            >>> check_for_dominance([[30, 20, 10], [29, 19, 9], [28, 21, 10], [4, 8], [5, 7], [2,1]])
            [[30, 20, 10], [28, 21, 10], [4, 8], [5, 7]]
        """

    # if got only 1 completion - it is undominated
    if len(completions) <= 1:
        return completions

    # We are going to collect all the dominated completions and then remove them from the original completion list
    dominated_completions = []

    # We sort the lists be length because we want to compare groups from the same length in a convenient way
    sorted_by_len = sorted(completions, key=len, reverse=True)

    # We go into a double FOR loop for brute-force testing for dominance
    for i in range(len(sorted_by_len) - 1):
        # We check for each 'first_list' if it's dominating another list
        first_list = sorted_by_len[i]

        # If current list is already dominated by a previously tested list - no need to check further.
        # if list1 dominating list2 AND list2 dominating list3 - then list1 dominating list3.
        # that means that all lists dominated by list2 are already in 'dominated_completions'.
        if first_list in dominated_completions:
            continue

        # We go through all lists from 'first_list' to end
        for j in range(i+1, len(sorted_by_len)):
            second_list = sorted_by_len[j]

            # Flag as dominated - until proven otherwise
            dominated = True

            # if we reached a list with a shorter length - no need to check anymore
            if len(first_list) != len(second_list):
                break

            # Since completions was ordered by SUM in descending order,
            # if all items in 'first_list' should be larger than the items in 'second_list' - first dominates second
            # if we found even 1 item from first_list that is smaller - then second_list is not "nested" in first_list.
            # meaning that second_list is not dominated by first_list
            for item1, item2 in zip(first_list, second_list):
                if item1 < item2:
                    dominated = False
                    break

            # Add second_list to the removal candidates
            if dominated:
                dominated_completions.append(second_list)

    # Remove dominated lists from completions and return them ordered by their sum.
    output_list = list_without_items(completions, dominated_completions)
    return sorted(output_list, key=sum, reverse=True)


# Returns a list of the pairs undominated by y (highest element that fits the bin with x).
# See article for details.
def find_undominated_pairs(constant_elements_sum: int, y: int, items: List, binsize: int) -> List:
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
    start = 0
    end = len(items) - 1
    undominated_pairs = []

    while (start < end):
        sum = items[start] + items[end]
        if constant_elements_sum + sum > binsize:
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
        [[19]]

        Test 4:
        >>> find_bin_completions(64, [64,50,44,43,37,32,18,7], 100)
        [[32], [18, 7]]

        Test 5:
        >>> find_bin_completions(50, [44,43,37,18,7], 100)
        [[43, 7], [44]]

        Test 6:
        >>> find_bin_completions(81, [59, 58, 55, 50, 43, 22, 21, 20, 15, 14, 10, 8, 6, 5, 4, 3, 1], 100)
        [[15, 3, 1], [10, 6, 3], [14, 4, 1], [15, 4], [14, 5], [10, 8, 1], [10, 5, 4], [8, 6, 5], [10, 5, 3, 1], [8, 6, 4, 1], [6, 5, 4, 3, 1], [10, 8], [6, 5, 4, 3], [15]]

        Test 7:
        >>> find_bin_completions(85, [5, 4, 3, 2, 1], 100)
        [[5, 4, 3, 2, 1], [5, 4, 3, 2], [5, 4, 3], [5, 4], [5]]
    """
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
            constant_elements_sum = x + sum(fc)
            items_left = list_without_items(items, fc)
            undominated_pairs = find_undominated_pairs(constant_elements_sum, y, items_left, binsize)

            # We add the undominated pairs to possible completions.
            # if none were found - we add the subset fc as a possible completions.
            if undominated_pairs:
                # We unite each pair with the constant elements we found.
                for pair in undominated_pairs:
                    pair.extend(fc)
                    pair.sort(reverse=True)
                    found_completions.append(pair)
                found_completions.extend(undominated_pairs)

            elif fc:
                # If we found a correct completion with no other undominated pairs - we add it to our list
                found_completions.append(list(fc))

    # Create all possible completions without duplicates, sorted in descending order by their sum.
    uniq_lst = unique_list(sorted(found_completions, key=sum, reverse=True))

    # Return the result after checking for dominance between the possible completions
    return check_for_dominance(uniq_lst)


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
