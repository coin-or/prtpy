"""
These functions are being used by the Bin-Completion algorithm for solving the bin packing problem.
See "bin_completion.py" for more details.
"""
import copy
import functools
from typing import List
from prtpy import outputtypes as out, Bins, BinsKeepingContents


def l2_lower_bound(binsize: float, items: List) -> float:
    copy_items = items.copy()

    copy_items.sort(reverse=True)

    total_sum = sum(copy_items)
    estimated_waste = 0
    capacity = binsize

    for x in copy_items:
        r = capacity - x
        smaller_elements = []
        for i in range(len(copy_items) - 1, copy_items.index(x), -1):
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

def find_undominated_pairs(x: int, y: int, items: List, binsize: int) -> List:
    start = 0;
    end = len(items)-1
    undominated_pairs = []

    while (start > end):
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

def generate_undominated_bin_completions(items: List, binsize: int) -> List:
    x = items[0]

    if len(items) == 1 or x + items[-1] > binsize:
        return []
    if len(items) == 2:
        return [[items[1]]]

    y = items[1]
    for i in range(2, len(items) - 1):
        if x + y > binsize:
            y = items[i]
        else:
            break

    items.remove(x)
    items.remove(y)
    undominated_pairs = find_undominated_pairs(x, y, items, binsize)
    if not undominated_pairs:
        return [[y]]
    else:
        return undominated_pairs


# This is a recursive function which fills the bins.
# See comments below.
def fill_bins(items: List, bins: Bins, bin_index: int, binsize: int, bound: int) -> tuple[Bins, bool]:
    # if items is empty, and we finished with fewer bins than the old bound, solution was found
    # if we reached the same amount of bins or more - return false
    if not items:
        if bins.num <= bound:
            return bins, True
        else:
            return bins, False

    # if we are reached the same amount of bins or more - return false
    if bins.num >= bound:
        return bins, False

    bins.add_empty_bins()
    # Add the largest item to the bin and generate possible completions for that bin
    bins.add_item_to_bin(items[0], bin_index)
    possible_bin_completions = generate_undominated_bin_completions(items, binsize)

    # if no possible completions was found - fill the next bin
    if not possible_bin_completions:
        return fill_bins(items, bins, bin_index + 1, binsize, bound)

    if len(possible_bin_completions) == 1:
        new_items = [element for element in items if element not in possible_bin_completions[0]]
        new_bins = copy.deepcopy(bins)
        map(functools.partial(bins.add_item_to_bin, bin_index=bin_index), possible_bin_completions[0])

        return fill_bins(new_items, new_bins, bin_index + 1, binsize, bound)

    # Go through all possible completions,
    # for each option - try to fill the next bins like a branch
    # if the solution found was not valid - move on to the next completion
    for comp in sorted(possible_bin_completions, key=sum, reverse=True):
        new_items = [element for element in items if element not in comp]
        new_bins = copy.deepcopy(bins)
        map(functools.partial(bins.add_item_to_bin, bin_index=bin_index), comp)
        solution, valid = fill_bins(new_items, new_bins, bin_index + 1, binsize, bound)

        if valid:
            return solution, valid

    return bins, False

