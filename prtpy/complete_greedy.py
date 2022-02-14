"""
    Partition the numbers using the Complete Greedy number partitioning algorithm (Korf, 1995):
           https://en.wikipedia.org/wiki/Greedy_number_partitioning

    Credit: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
           https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning/greedy.py
"""

from typing import List, Tuple, Callable, Iterator, Any
import numpy as np
import logging
from prtpy import outputtypes as out, objectives as obj

logger = logging.getLogger(__name__)


def optimal(
    numbins: int,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    outputtype: out.OutputType = out.Partition,
):
    """
    Returns the optimal partition - the partition that minimizes the objective.

    To find the optimal partition it generates all partitions using the order from the greedy algorithm, and returns the optimal result.

    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> optimal(3, walter_numbers, objective=obj.MinimizeDifference, outputtype=out.PartitionAndSums)
    Bin #0: [27, 26, 10], sum=63.0
    Bin #1: [39, 16], sum=55.0
    Bin #2: [46, 13], sum=59.0
    >>> optimal(3, walter_numbers, objective=obj.MinimizeLargestSum, outputtype=out.PartitionAndSums)
    Bin #0: [27, 26], sum=53.0
    Bin #1: [39, 13, 10], sum=62.0
    Bin #2: [46, 16], sum=62.0
    >>> optimal(3, walter_numbers, objective=obj.MaximizeSmallestSum, outputtype=out.PartitionAndSums)
    Bin #0: [27, 16, 13], sum=56.0
    Bin #1: [39, 26], sum=65.0
    Bin #2: [46, 10], sum=56.0
    >>> optimal(3, walter_numbers, objective=obj.MaximizeSmallestSum, outputtype=out.SmallestSum)
    56.0

    >>> from prtpy.partition import partition
    >>> partition(algorithm=optimal, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['e', 'c', 'd'], ['g', 'a'], ['f', 'b']]
    >>> partition(algorithm=optimal, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])
    """
    for result in generator(numbins, items, map_item_to_value, objective, outputtype):
        logger.info("Improved result: %s", result)
    return result


def generator(
    numbins: int,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    outputtype: out.OutputType = out.Partition,
) -> Iterator:
    """
    Generate partitions using the order from the greedy algorithm.
    Concretely, it searches through all combinations by following the strategy that
    adds to each part the largest number not yet added to any part, so that smaller
    parts are prioritized. This is done depth-first, meaning that the smallest of the
    input numbers are shuffled between different parts before larger input numbers are.

    New partitions are yielded whenever an improvement is found, according to an
    optional objective function.
    """
    sorted_items = sorted(items, key=map_item_to_value, reverse=True)
    max_depth = len(items)

    # Create a stack whose elements are bins and the current depth.
    # Initially, it contains a single tuple: an empty partition with depth 0.
    to_visit: List[Tuple[Bins, int]] = [(outputtype.create_empty_bins(numbins), 0)]
    best_objective_value = np.inf
    while len(to_visit) > 0:
        bins, depth = to_visit.pop()
        # If we have reached the leaves of the DFS tree, check if we have an improvement, and yield if we do.
        if depth == max_depth:
            new_objective_value = objective.get_value_to_minimize(bins.sums)
            if new_objective_value < best_objective_value:
                best_objective_value = new_objective_value
                yield outputtype.extract_output_from_bins(bins)
        else:
            item = sorted_items[depth]
            # Order bins by decreasing sum, so bin with smallest sum ends up on top of stack.
            for bin_index in sorted(range(numbins), key=lambda i: bins.sums[i], reverse=True):
                # Create the next vertex.
                new_bins = bins.add_item_to_bin(
                    item, map_item_to_value(item), bin_index, inplace=False
                )
                new_depth = depth + 1
                to_visit.append((new_bins, new_depth))


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
