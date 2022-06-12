"""
    Implementations of Improved bin completion algorithm:
        https://www.ijcai.org/Proceedings/13/Papers/103.pdf

    Ethan L. Schreiber and Richard E. Korf "Improved Bin Completion for Optimal Bin Packing and Number Partitioning" 2013
    
    Author Ishay Trattner
    Since: 05-2022
"""

from typing import Callable, Any
from prtpy.packing import best_fit
from prtpy.packing.bc_utilities import *
from prtpy.bins import BinsKeepingContents
from prtpy.packing.ibc_util import ImprovedBinBranch, Stack, undominated_generator, hn_wrapper
import copy
from queue import PriorityQueue


def improved_bin_completion(
    bins: Bins,
    binsize: int,
    items: List[Any],
    valueof: Callable[[Any], float] = lambda x: x,
    chunk_size: int = 50,
    LDS: bool = False  # Limited Discrepancy Search
) -> Bins:
    """
    Pack the given items into bins sized binsize using the Improved Bin Comletion algorithm.
    The IBC algorithm pack the items to the fewest number of bins sized binsize.

    >>> from prtpy.bins import BinsKeepingContents
    >>> improved_bin_completion(BinsKeepingContents(), binsize=9, items=[1,2,3,3,5,9,9]).bins
    [[9], [9], [5, 3, 1], [3, 2]]
    >>> improved_bin_completion(BinsKeepingContents(), binsize=18, items=[1,2,3,3,5,9,9]).bins
    [[9, 9], [5, 3, 3, 2, 1]]
    >>> list(improved_bin_completion(BinsKeepingContents(), binsize=9, items=[1,2,3,3,5,9,9]).sums)
    [9.0, 9.0, 9.0, 5.0]
    """
   # Test if there is an item which is not a number OR larger than binsize.
    for item in items:
        if not isinstance(item, int) or item > binsize:
            raise ValueError(f"Item {item} is not valid.")

    # Remove zeros from items as they are irrelevant.
    items = list(filter((0).__ne__, items))

    # Find the BFD solution and check if it's optimal using the lower bound calculation.
    bfd_solution = best_fit.decreasing(
        BinsKeepingContents(), binsize, items.copy())
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
    main_branch = ImprovedBinBranch(sorted_items, bins, bin_index=0, last_out_bin_size=binsize, generator=hn_wrapper(
        undominated_generator(bin_size=binsize, numbers=sorted_items, b_chunks_size=chunk_size)))

    # -- lazy DFS
    if LDS:
        branches = PriorityQueue()
        branches.put((1, main_branch))
    else:
        branches = Stack()
        branches.put((1, main_branch))

    while not branches.empty():
        # cb = current branch
        cb: ImprovedBinBranch
        cb_priority: int
        cb_priority, cb = branches.get()

        # if he has next then add the next child
        if cb.generator.has_next():
            num_for_bin = next(cb.generator)
            branches.put((cb_priority, cb))
            child_bins: Bins = copy.deepcopy(cb.bins)
            child_bins.add_empty_bins()

            priority = cb_priority
            if LDS:
                last_sum = cb.last_out_bin_size
                now_sum = sum(num_for_bin)
                priority += (1 if last_sum > now_sum else 0)
                cb.last_out_bin_size = now_sum

            for item in num_for_bin:
                child_bins.add_item_to_bin(item, cb.bin_index)

            # create numbers for the child and removing the bin numbers
            child_items = cb.items.copy()
            for num in num_for_bin:
                child_items.remove(num)

            child = ImprovedBinBranch(child_items, child_bins, bin_index=cb.bin_index + 1, last_out_bin_size=binsize, generator=hn_wrapper(
                undominated_generator(bin_size=binsize, numbers=child_items, b_chunks_size=chunk_size)))

            branches.put((priority, child))

            continue
    # -- lazy DFS

        # If we completed an arrangement successfully, and it's better than the best solution we had - update it.
        if not cb.items and cb.bins.num < best_solution_so_far.num:
            logging.info(
                f"Updated best solution from {best_solution_so_far.num} bins to {cb.bins.num} bins.")
            best_solution_so_far = cb.bins

        # If we found a solution with number of bins that equals the lower bound - it's optimal! Hurray!
        if best_solution_so_far.num == lb:
            logging.info(f"found and optimal solution with {lb} bins.")
            break

    return best_solution_so_far


# For bulding - delete this
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from prtpy.bins import BinsKeepingContents

    print(list(improved_bin_completion(BinsKeepingContents(),
          binsize=9, items=[1, 2, 3, 3, 5, 9, 9]).sums))
    print(improved_bin_completion(BinsKeepingContents(), binsize=9, items=[9]))
    print(improved_bin_completion(
        BinsKeepingContents(), binsize=9, items=[1, 2, 3]))
    print(improved_bin_completion(BinsKeepingContents(), binsize=9, items=[
          7, 2, 3, 8, 1, 1]))  # Example that the algo improve
    print()
    print(improved_bin_completion(BinsKeepingContents(), binsize=9, items=[
          8, 5, 2, 4, 5, 6, 2, 4, 6, 8, 2, 1]))  # Example that the algo improve

    from bin_completion import bin_completion
    from time import time
    from random import seed
    from random import randint

    seed(1)
    arr = [randint(1, 100) for _ in range(15)]
    print(arr)

    start = time()
    for _ in range(1):
        print(bin_completion(BinsKeepingContents(), binsize=100, items=arr))
    end = time()
    print(f"not my elapsed: {end - start}")

    start = time()
    for _ in range(1):
        print(improved_bin_completion(
            BinsKeepingContents(), binsize=100, items=arr))
    end = time()
    print(f"my elapsed: {end - start}")

    start = time()
    for _ in range(1):
        print(improved_bin_completion(
            BinsKeepingContents(), binsize=100, items=arr, LDS=True))
    end = time()
    print(f"my elapsed LDS: {end - start}")
