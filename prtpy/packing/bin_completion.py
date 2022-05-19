import itertools
from typing import Callable, List, Any
from prtpy import outputtypes as out, Bins, BinsKeepingContents
from prtpy.packing import best_fit
from prtpy.packing.bc_utilities import *
import math


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
    [[99], [94,3], [79,18], [64,32], [50,43,7], [44,37,19]]

    Example 4: Article Example #1
    >>> bin_completion(BinsKeepingContents(), binsize=100, items=[100, 98, 96, 93, 91, 87, 81, 59, 58, 55, 50, 43, 22, 21, 20, 15, 14, 10, 8, 6, 5, 4, 3, 1, 0]).bins
    [[100], [98, 1], [96, 4], [93, 6], [91, 8], [87, 10, 3], [81, 14, 5], [59, 21, 20], [58, 22, 15], [55, 43], [50]]

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
    print("bfd.num: ", bfd_solution.num, ", lower bound: ", lb, " returning bfd solution:\n", bfd_solution)

    # if bfd_solution.num == lb:
    #     return bfd_solution

    sorted_items = sorted(items, reverse=True)

    # fill the bins to find a solution
    solution, valid = fill_bins(sorted_items, bins, 0, binsize, bfd_solution.num, lb)

    return solution


if __name__ == "__main__":
    import doctest

    # items = [99, 97, 94, 93, 8, 5, 4, 2]
    # s = sum(items)
    # print(l2_lower_bound(100, items))
    # print("sum ", s)
    # print("sum+98 ", (98 + sum(items)))
    # print("Should be ", ((98 + sum(items)) / 100))
    #
    # from prtpy.packing import first_fit as ff
    #
    # items = [100, 100, 100, 100, 100, 100]
    # print(ff.decreasing(BinsKeepingContents(), binsize=100, items=[99, 94, 79, 64, 50, 44, 43, 37, 32, 19, 18, 7, 3]))
    # print()
    # print(bin_completion(BinsKeepingContents(), binsize=100, items=[99, 94, 79, 64, 50, 44, 43, 37, 32, 19, 18, 7, 3]))
    #
    # def f(x, y):
    #     return x+y
    #
    #
    # m = map(functools.partial(f, y=10), items)
    #
    # print(list(m))
    #
    # binstest = ff.decreasing(BinsKeepingContents(), binsize=100, items=[99, 94, 79, 64, 50, 44, 43, 37, 32, 19, 18, 7, 3])
    #
    # print("TEST")
    # print()
    # items = [99,94,79,64,50,44,43,37,32,19,18,7,3]
    # comb = list(itertools.combinations(items, 2))
    # print(sum(comb[0]))
    # print(type(BinsKeepingContents().bins))
    print(doctest.testmod())
