"""
    Partition the numbers using the Complete Greedy number partitioning algorithm (Korf, 1995):
           https://en.wikipedia.org/wiki/Greedy_number_partitioning

    Credit: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
           https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning/greedy.py
"""

from typing import List, Tuple, Callable, Iterator, Any
import numpy as np
import logging, time
from prtpy import objectives as obj, Bins, partitioning

logger = logging.getLogger(__name__)


# def optimal(
#     bins: Bins,
#     items: List[any],
#     valueof: Callable[[Any], float] = lambda x: x,
#     objective: obj.Objective = obj.MinimizeDifference,
# ):
#     """
#     Returns the optimal partition - the partition that minimizes the objective.

#     To find the optimal partition it generates all partitions using the order from the greedy algorithm, and returns the optimal result.

#     The following examples are based on:
#         Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
#     >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
#     >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
#     >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeDifference)
#     Bin #0: [27, 26, 10], sum=63.0
#     Bin #1: [39, 16], sum=55.0
#     Bin #2: [46, 13], sum=59.0
#     >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeLargestSum)
#     Bin #0: [27, 26], sum=53.0
#     Bin #1: [39, 13, 10], sum=62.0
#     Bin #2: [46, 16], sum=62.0
#     >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MaximizeSmallestSum)
#     Bin #0: [27, 16, 13], sum=56.0
#     Bin #1: [39, 26], sum=65.0
#     Bin #2: [46, 10], sum=56.0

#     >>> from prtpy import partition, outputtypes as out
#     >>> partition(algorithm=optimal, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
#     [['e', 'c', 'd'], ['g', 'a'], ['f', 'b']]
#     >>> partition(algorithm=optimal, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
#     array([16., 16.])
#     """
#     for result in generator(bins, items, valueof, objective):
#         logger.info("Improved result: %s", result.sums)
#     return result


def anytime(
    bins: Bins,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    time_in_seconds: float = np.inf,
) -> Iterator:
    """
    An anytime algorithm for finding a partition using the Complete Greedy algorithm.

    It generates partitions using the order from the greedy algorithm.
    Concretely, it searches through all combinations by following the strategy that
    adds to each part the largest number not yet added to any part, so that smaller
    parts are prioritized. This is done depth-first, meaning that the smallest of the
    input numbers are shuffled between different parts before larger input numbers are.

    It stops when the optimal partition is found, OR when the time runs out.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> anytime(BinsKeepingContents(2), [4,5,6,7,8], objective=obj.MinimizeDifference, time_in_seconds=1)
    Bin #0: [6, 5, 4], sum=15.0
    Bin #1: [8, 7], sum=15.0
    
    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> anytime(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeDifference, time_in_seconds=1)
    Bin #0: [27, 26, 10], sum=63.0
    Bin #1: [39, 16], sum=55.0
    Bin #2: [46, 13], sum=59.0
    >>> anytime(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeLargestSum, time_in_seconds=1)
    Bin #0: [27, 26], sum=53.0
    Bin #1: [39, 13, 10], sum=62.0
    Bin #2: [46, 16], sum=62.0
    >>> anytime(BinsKeepingContents(3), walter_numbers, objective=obj.MaximizeSmallestSum, time_in_seconds=1)
    Bin #0: [27, 16, 13], sum=56.0
    Bin #1: [39, 26], sum=65.0
    Bin #2: [46, 10], sum=56.0

    >>> from prtpy import partition, outputtypes as out
    >>> partition(algorithm=anytime, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['e', 'c', 'd'], ['g', 'a'], ['f', 'b']]
    >>> partition(algorithm=anytime, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])

    :param objective: represents the function that should be optimized. Default is minimizing the difference between bin sums.
    :param time_in_seconds: determines how much time the function should run before it stops. Default is infinity.
    """
    sorted_items = sorted(items, key=valueof, reverse=True)
    max_depth = len(items)
    start_time = time.perf_counter()

    # Create a stack whose elements are bins and the current depth.
    # Initially, it contains a single tuple: an empty partition with depth 0.
    to_visit: List[Tuple[Bins, int]] = [(bins, 0)]
    best_objective_value = np.inf
    best_bins = bins
    while len(to_visit) > 0:
        bins, depth = to_visit.pop()
        # If we have reached the leaves of the DFS tree, check if we have an improvement, and yield if we do.
        if depth == max_depth:
            new_objective_value = objective.get_value_to_minimize(bins.sums)
            if new_objective_value < best_objective_value:
                best_objective_value = new_objective_value
                best_bins = bins
            if time.perf_counter() - start_time > time_in_seconds:
                break
        else:
            item = sorted_items[depth]
            # Order bins by decreasing sum, so bin with smallest sum ends up on top of stack.
            for bin_index in sorted(range(bins.num), key=lambda i: bins.sums[i], reverse=True):
                # Create the next vertex.
                new_bins = bins.add_item_to_bin(
                    item, bin_index, inplace=False
                )
                new_depth = depth + 1
                to_visit.append((new_bins, new_depth))
    return best_bins


if __name__ == "__main__":
    # logger.setLevel(logging.INFO)
    # logger.addHandler(logging.StreamHandler())

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
