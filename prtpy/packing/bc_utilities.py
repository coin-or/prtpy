"""
These functions are being used by the Bin-Completion algorithm for solving the bin packing problem.
See "bin_completion.py" for more details.

Authors: Avshalom Avraham & Tehila Ben-Kalifa
Since: 05-2022
"""
import math
from itertools import combinations, product
from typing import List, Iterable
import logging
from prtpy.bins import Bins, BinsKeepingContents


# A simple class to store a state of bins arrangement.
# We keep the current bin arrangement and index of the next bin, as well as the items left to arrange in those bins.
class BinBranch:
    def __init__(self, items: List, bins: Bins, bin_index: int):
        self.items = items
        self.bins = bins
        self.bin_index = bin_index


# Returns a new list which is a copy of 'original' but without the items in 'to_remove' if they existed.
def list_without_items(original: List, to_remove: Iterable) -> List:
    output = original.copy()
    for obj in to_remove:
        if obj in output:
            output.remove(obj)

    return output


# Returns a new list which is a copy of 'lst' but without duplicate items.
def unique_list(lst: List) -> List:
    output = []
    for element in lst:
        if element not in output:
            output.append(element)
    return output


# Calculates the lower bound of bins for bin packing problem.
def lower_bound(binsize: float, items: List) -> float:
    if binsize == 0:
        return 0
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


# A function that creates all possible arrangements of items in 'num_of_sublists' lists.
# For example: find_all_bin_arrangements(range(2), 2) => [[0,1],[]], [[0],[1]], [[1], [0]], etc......
def find_all_bin_arrangements(items: List, num_of_sublists: int):
    for locs in product(range(num_of_sublists), repeat=len(items)):
        output = [[] for _ in range(num_of_sublists)]
        for elem, loc in zip(items, locs):
            output[loc].append(elem)
        yield output


# A function that gets a list of 'n' numbers and an arrangement in length 'n',
# and checks if each list in the arrangement fits the corresponding item in the same index
def check_fits(items: List[int], arrangement: List[List]):
    if len(items) != len(arrangement):
        raise ValueError(f"items list ({len(items)}) and arrangement ({len(arrangement)}) are not in the same size")

    for i in range(len(items)):
        if sum(arrangement[i]) > items[i]:
            return False

    # Return true if each of the lists in the arrangement fits the size of the item in the same index
    return True


def is_dominant(list1: List, list2: List):
    """
            Test 1:
            >>> is_dominant([10], [])
            True

            Test 2:
            >>> is_dominant([], [10])
            False

            Test 3:
            >>> is_dominant([10], [9])
            True

            Test 4:
            >>> is_dominant([9], [10])
            False

            Test 5:
            >>> is_dominant([10,5,2], [5,2])
            True

            Test 6:
            >>> is_dominant([10,5,2], [9,4])
            True

            Test 7:
            >>> is_dominant([10,8,6,4,2], [9,7,3,1])
            True

            Test 8:
            >>> is_dominant([9,7,3,1], [10,8,6,4,2])
            False
        """

    # If list2 is empty - everything dominates it. return True.
    # If list2 is NOT empty and list1 IS empty - list1 can't dominate list2. return False.
    if not list2:
        return True
    elif not list1:
        return False

    # If list2 is a sublist of list1
    if all(x in list1 for x in list2):
        return True

    # If the largest item in list2 does not fit the largest item in list1 - list1 can't dominate list2
    if list1[0] < list2[0]:
        return False

    # Create all possible arrangements of list2 in len(list1) 'bins'.
    # If found an arrangement that can be fitted perfectly in list1 items (assuming each item is a bin) - return True
    for arrangement in find_all_bin_arrangements(list2, len(list1)):
        if check_fits(list1, arrangement):
            return True

    return False



def check_for_dominance(completions: List[List]):
    """
            Test 1:
            >>> check_for_dominance([[3], [2], [1]])
            [[3]]

            Test 2:
            >>> check_for_dominance([[32], [30], [18, 7], [10, 5]])
            [[32]]

            Test 3:
            >>> check_for_dominance([[32], [18, 7], [20, 5]])
            [[32]]

            Test 4:
            >>> check_for_dominance([[30, 20, 10], [29, 19, 9], [28, 21, 10], [4, 8], [5, 7], [2,1]])
            [[30, 20, 10], [28, 21, 10]]
        """

    # if got only 1 completion - it is undominated
    if len(completions) <= 1:
        return completions

    # We are going to collect all the dominated completions and then remove them from the original completion list
    dominated_completions = []

    for i in range(len(completions) - 1):
        list1 = completions[i]
        if list1 in dominated_completions:
            continue

        for j in range(i+1, len(completions)):
            list2 = completions[j]
            if list2 in dominated_completions:
                continue

            # If list1 dominates list2 - append list2 to the dominated completions and continue to the next iteration
            if is_dominant(list1, list2):
                dominated_completions.append(list2)
                continue

            # Else - if list2 dominates list1 - append list1 to the dominated completions and break (for a new list1)
            if is_dominant(list2, list1):
                dominated_completions.append(list1)
                break

            # If list1 nor list1 is dominated - continue for the next list2 without doing anything

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
def find_bin_completions(x: int, items: List, binsize: int):
    """
        Test 1:
        >>> find_bin_completions(99, [94,79,64,50,44,43,37,32,19,18,7,3], 100)
        []

        Test 2:
        >>> find_bin_completions(94, [79,64,50,44,43,37,32,19,18,7,3], 100)
        [[3]]

        Test 3:
        >>> find_bin_completions(79, [64,50,44,43,37,32,19,18,7,3], 100)
        [[18, 3], [19]]

        Test 4:
        >>> find_bin_completions(64, [64,50,44,43,37,32,18,7], 100)
        [[32]]

        Test 5:
        >>> find_bin_completions(50, [44,43,37,18,7], 100)
        [[43, 7], [44]]

        Test 6:
        >>> find_bin_completions(81, [59, 58, 55, 50, 43, 22, 21, 20, 15, 14, 10, 8, 6, 5, 4, 3, 1], 100)
        [[10, 6, 3], [15, 4], [14, 5], [10, 8, 1]]

        Test 7:
        >>> find_bin_completions(85, [5, 4, 3, 2, 1], 100)
        [[5, 4, 3, 2, 1]]
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
