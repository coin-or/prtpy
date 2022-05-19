import copy
import itertools
import logging
from typing import Callable, List, Any
from prtpy import outputtypes as out, Bins, BinsKeepingContents
from prtpy.packing import best_fit
from prtpy.packing.bc_utilities import *
import math
from functools import partial


def bin_completion(
        bins: Bins,
        binsize: float,
        items: List[any],
        valueof: Callable[[Any], float] = lambda x: x
) -> Bins:
    """
    "A New Algorithm for Optimal Bin Packing", by Richard E. Korf (2002) https://www.aaai.org/Papers/AAAI/2002/AAAI02-110.pdf
    Algorithm: Given a set of numbers, and a set of bins of fixed capacity,
    the algorithm finds the minimum number of bins needed to contain all the numbers,
    such that the sum of the numbers assigned to each bin does not exceed the bin capacity.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums

    Example 1: max capacity
    >>> bin_completion(BinsKeepingContents(), binsize=100, items=[100,100,100,100,100,100]).bins
    [[100], [100], [100], [100], [100], [100]]

    Example 2: min capacity
    >>> bin_completion(BinsKeepingContents(), binsize=100, items=[1,2,3,4,5,85]).bins
    [[85, 5, 4, 3, 2, 1]]

    Example 3: Complex input
    >>> bin_completion(BinsKeepingContents(), binsize=100, items=[99,94,79,64,50,44,43,37,32,19,18,7,3]).bins
    [[99], [94, 3], [79, 19], [64, 32], [50, 43, 7], [44, 37, 18]]

    Example 4: Article Example #1
    >>> bin_completion(BinsKeepingContents(), binsize=100, items=[100, 98, 96, 93, 91, 87, 81, 59, 58, 55, 50, 43, 22, 21, 20, 15, 14, 10, 8, 6, 5, 4, 3, 1, 0]).bins
    [[100], [98], [96, 4], [93, 6, 1], [91, 8], [87, 10, 3], [81, 15], [59, 22, 14, 5], [58, 21, 20], [55, 43], [50]]

    Example 5: Article Example #2
    >>> bin_completion(BinsKeepingContents(), binsize=100, items=[6, 12, 15, 40, 43, 82]).bins
    [[82, 12, 6], [43, 40, 15]]

    Example 6: Article Example #3
    >>> bin_completion(BinsKeepingContents(), binsize=100, items=[99, 97, 94, 93, 8, 5, 4, 2]).bins
    [[99], [97, 2], [94, 5], [93, 4], [8]]
    """

    items = list(filter((0).__ne__, items))

    # Find the FFD solution and check if it's optimal using the L2 lower bound
    bfd_solution = best_fit.decreasing(BinsKeepingContents(), binsize, items.copy())
    lb = lower_bound(binsize, items.copy())

    if bfd_solution.num == lb:
        return bfd_solution

    best_solution_so_far = bfd_solution
    sorted_items = sorted(items, reverse=True)

    main_branch = BinBranch(sorted_items, bins, bin_index=0)
    branches = [main_branch]

    while branches:
        # cb = current branch
        cb = branches.pop(0)

        for x in cb.items:
            cb.bins.add_empty_bins()
            cb.bins.add_item_to_bin(x, cb.bin_index)
            updated_list = cb.items[1:]
            # cb.items.remove(x)
            possible_undominated_completions = find_bin_completions(x, updated_list, binsize)

            if len(possible_undominated_completions) == 1:
                # print("before: bin index: ", cb.bin_index, " completion: ", possible_undominated_completions[0], " bins: \n", cb.bins)
                list(map(partial(cb.bins.add_item_to_bin, bin_index=cb.bin_index), possible_undominated_completions[0]))
                # print("after: bin index: ", cb.bin_index, " completion: ", possible_undominated_completions[0], " bins: \n", cb.bins)

                list(map(updated_list.remove, possible_undominated_completions[0]))
            elif len(possible_undominated_completions) > 1:
                for completion in possible_undominated_completions[1:]:
                    new_items = list_without_items(updated_list, completion)
                    new_bins = copy.deepcopy(cb.bins)

                    list(map(partial(new_bins.add_item_to_bin, bin_index=cb.bin_index), completion))

                    branches.append(BinBranch(new_items, new_bins, cb.bin_index+1))

                list(map(partial(cb.bins.add_item_to_bin, bin_index=cb.bin_index), possible_undominated_completions[0]))
                list(map(updated_list.remove, possible_undominated_completions[0]))

            cb.bin_index += 1

            # if cb.bin_index == 4:
            #     return BinsKeepingContents()

            cb.items = updated_list
            partial_lower_bound = cb.bins.num + (sum(updated_list) / binsize)
            if partial_lower_bound >= best_solution_so_far.num:
                logging.info(f"branch pruned. partial lower bound {partial_lower_bound} best lower bound {best_solution_so_far.num}")
                break

            if not cb.items:
                break

        if not cb.items and cb.bins.num < best_solution_so_far.num:
            best_solution_so_far = cb.bins

        if best_solution_so_far.num == lb:
            break


    # fill the bins to find a solution
    # solution, valid = fill_bins(sorted_items, bins, 0, binsize, bfd_solution.num, lb)

    return best_solution_so_far


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
