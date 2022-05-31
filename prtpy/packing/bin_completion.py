"""
    Pack the numbers using the Bin-Completion algorithm by Richard E. Korf (2002):
        https://www.aaai.org/Papers/AAAI/2002/AAAI02-110.pdf:

    Authors: Avshalom Avraham & Tehila Ben-Kalifa
    Since: 05-2022
"""

from typing import Callable, Any
from prtpy.packing import best_fit
from prtpy.packing.bc_utilities import *
from functools import partial
import copy
from prtpy.bins import BinsKeepingContents

def bin_completion(
        bins: Bins,
        binsize: float,
        items: List[any],
        valueof: Callable[[Any], float] = lambda x: x
) -> Bins:
    """
    "A New Algorithm for Optimal Bin Packing", by Richard E. Korf (2002).
    Given a set of numbers, and a set of bins of fixed capacity,
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
    # Test if there is an item which is not a number OR larger than binsize.
    for item in items:
        if not isinstance(item, int) or item > binsize:
            raise ValueError(f"Item {item} is not valid.")

    # Remove zeros from items as they are irrelevant.
    items = list(filter((0).__ne__, items))

    # Find the BFD solution and check if it's optimal using the lower bound calculation.
    bfd_solution = best_fit.decreasing(BinsKeepingContents(), binsize, items.copy())
    lb = lower_bound(binsize, items)

    # If the BFD solution is optimal - return it.
    if bfd_solution.num == lb:
        logging.info(f"BFD has returned an optimal solution with {lb} bins.")
        bins = bfd_solution
        return bfd_solution

    # We keep the BFD solution as the best solution so far and sort the items in descending order.
    best_solution_so_far = bfd_solution
    sorted_items = sorted(items, reverse=True)

    # We create our main branch which will be the first arrangement with empty bins and index 0.
    # Every branch will be a certain state of bin arrangements and items left to arrange.
    # If we finished working on a branch, and we didn't get a good solution, we move on to the next branch.
    main_branch = BinBranch(sorted_items, bins, bin_index=0)
    branches = [main_branch]

    while branches:
        # cb = current branch
        cb = branches.pop(0)

        for x in cb.items:
            # Add a new bin and add x to that bin
            cb.bins.add_empty_bins()
            cb.bins.add_item_to_bin(x, cb.bin_index)

            # Now we consider all items except for x.
            # We generate all possible completions for the bin containing x, sorted by their sum in descending order.
            updated_list = cb.items[1:]
            possible_undominated_completions = find_bin_completions(x, updated_list, binsize)

            # If we found only 1 possible completion - we add it to the bin and remove it from the updated item list.
            if len(possible_undominated_completions) == 1:
                for item in possible_undominated_completions[0]:
                    cb.bins.add_item_to_bin(item, cb.bin_index)
                    updated_list.remove(item)

            # If we found more than 1 possible completion:
            elif len(possible_undominated_completions) > 1:
                # We add all the completions from index 1 to end as branches for later.
                # We create a new copy of bins and items left according to that specific completion.
                # Then we add that copies to a new branches.
                for completion in possible_undominated_completions[1:]:
                    new_items = list_without_items(updated_list, completion)
                    new_bins = copy.deepcopy(cb.bins)

                    # list(map(partial(new_bins.add_item_to_bin, bin_index=new_bins.bin_index), completion))
                    for item in completion:
                        new_bins.add_item_to_bin(item, cb.bin_index)

                    # We can calculate the partial lower bound in O(1) and pass on the branch if we are working on
                    # a solution that is worse than our best solution so far.
                    partial_lower_bound = new_bins.num + (sum(new_items) / binsize)
                    if partial_lower_bound >= best_solution_so_far.num:
                        logging.info(
                            f"Redundant branch. partial lower bound - {partial_lower_bound}, exceeds or equals best lower "
                            f"bound found so far -  {best_solution_so_far.num}.")
                    else:
                        branches.append(BinBranch(new_items, new_bins, cb.bin_index + 1))

                # We add the first completions (with the largest sum) to our current branch.
                for item in possible_undominated_completions[0]:
                    cb.bins.add_item_to_bin(item, cb.bin_index)
                    updated_list.remove(item)

            # We finished with the current bin, and we move on to the next bin.
            cb.bin_index += 1

            # We need to update the current branch items
            cb.items = updated_list

            # We can calculate the partial lower bound in O(1) and prune the branch if we are working on a solution that
            # is worse than our best solution so far.
            partial_lower_bound = cb.bins.num + (sum(updated_list) / binsize)
            if partial_lower_bound >= best_solution_so_far.num:
                logging.info(
                    f"branch pruned. partial lower bound - {partial_lower_bound}, exceeds or equals best lower "
                    f"bound found so far -  {best_solution_so_far.num}.")
                break

            # If we have to items to arrange we are done with this branch.
            if not cb.items:
                break

        # If we completed an arrangement successfully, and it's better than the best solution we had - update it.
        if not cb.items and cb.bins.num < best_solution_so_far.num:
            logging.info(f"Updated best solution from {best_solution_so_far.num} bins to {cb.bins.num} bins.")
            best_solution_so_far = cb.bins

        # If we found a solution with number of bins that equals the lower bound - it's optimal! Hurray!
        if best_solution_so_far.num == lb:
            logging.info(f"found and optimal solution with {lb} bins.")
            break

    return best_solution_so_far


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
