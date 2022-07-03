"""
Partition the numbers using the Complete Greedy number partitioning algorithm (Korf, 1995):
        https://en.wikipedia.org/wiki/Greedy_number_partitioning

Programmer: Erel Segal-Halevi
Since: 2022-06

Credit: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
        https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning/greedy.py
"""

from typing import List, Tuple, Callable, Iterator, Any
import numpy as np
import logging
from prtpy import objectives as obj, Bins
from copy import deepcopy

logger = logging.getLogger(__name__)

def optimal(
    bins: Bins,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    use_lower_bound: bool = True,
    use_heuristic_3: bool = False
) -> Iterator:
    """
    Finds a partition in which the largest sum is minimal, using the Complete Greedy algorithm.

    :param objective: represents the function that should be optimized. Default is minimizing the difference between bin sums.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> optimal(BinsKeepingContents(2), [4,5,6,7,8], objective=obj.MinimizeDifference)
    Bin #0: [6, 5, 4], sum=15.0
    Bin #1: [8, 7], sum=15.0
    
    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeDifference)
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeLargestSum)
    Bin #0: [27, 26], sum=53.0
    Bin #1: [39, 13, 10], sum=62.0
    Bin #2: [46, 16], sum=62.0
    >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MaximizeSmallestSum)
    Bin #0: [46, 10], sum=56.0
    Bin #1: [27, 16, 13], sum=56.0
    Bin #2: [39, 26], sum=65.0

    Compare results with and without the lower bound:
    >>> random_numbers = np.random.randint(1, 2**16-1, 10, dtype=np.int64)
    >>> objective = obj.MinimizeDifference
    >>> bins1=optimal(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=True)
    >>> bins2=optimal(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=False)
    >>> objective.value_to_minimize(bins1.sums)==objective.value_to_minimize(bins2.sums)
    True
    >>> objective = obj.MinimizeLargestSum
    >>> bins1=optimal(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=True)
    >>> bins2=optimal(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=False)
    >>> objective.value_to_minimize(bins1.sums)==objective.value_to_minimize(bins2.sums)
    True
    >>> objective = obj.MaximizeSmallestSum
    >>> bins1=optimal(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=True)
    >>> bins2=optimal(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=False)
    >>> objective.value_to_minimize(bins1.sums)==objective.value_to_minimize(bins2.sums)
    True

    Compare results with and without the heuristic 3:
    >>> random_numbers = np.random.randint(1, 2**16-1, 10, dtype=np.int64)
    >>> objective = obj.MinimizeLargestSum
    >>> bins1=optimal(BinsKeepingSums(3), random_numbers, objective=objective, use_heuristic_3=True)
    >>> bins2=optimal(BinsKeepingSums(3), random_numbers, objective=objective, use_heuristic_3=False)
    >>> objective.value_to_minimize(bins1.sums)==objective.value_to_minimize(bins2.sums)
    True

    Partitioning items with names:
    >>> from prtpy import partition, outputtypes as out
    >>> partition(algorithm=optimal, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['g', 'a'], ['f', 'b'], ['e', 'c', 'd']]
    >>> partition(algorithm=optimal, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])
    """
    numitems = len(items)
    logger.info("Complete Greedy %s Partitioning of %d items into %d bins.", type(objective).__name__, numitems, bins.num)

    sorted_items = sorted(items, key=valueof, reverse=True)
    sums_of_remaining_items = [sum(map(valueof, sorted_items[i:])) for i in range(numitems)] + [0] # For Heuristic 3
    partitions_checked = 0

    best_bins, best_objective_value = None, np.inf

    # Create a stack whose elements are bins and the current depth.
    # Initially, it contains a single tuple: an empty partition with depth 0.
    stack: List[Tuple[Bins, int]] = [(bins, 0)]
    while len(stack) > 0:
        current_bins, depth = stack.pop()

        # If we have reached the leaves of the DFS tree, check if we have an improvement:
        if depth == numitems:
            partitions_checked += 1
            new_objective_value = objective.value_to_minimize(current_bins.sums)
            if new_objective_value < best_objective_value:
                best_bins, best_objective_value = current_bins, new_objective_value
                logger.info("  Found a better solution: %s, with value %s", best_bins.bins if hasattr(best_bins,'bins') else best_bins.sums, best_objective_value)
            continue

        else:
    
            # Heuristic 3: "If the sum of the remaining unassigned integers plus the smallest current subset sum is <= the largest subset sum, all remaining integers are assigned to the subset with the smallest sum, terminating that branch of the tree."
            # Note that this heuristic is valid only for the objective "minimize largest sum"!
            if use_heuristic_3 and objective==obj.MinimizeLargestSum:
                if sums_of_remaining_items[depth] + current_bins.sums[0] <= current_bins.sums[-1]:
                    new_bins = deepcopy(current_bins)
                    for i in range(depth,numitems):
                        new_bins.add_item_to_bin(sorted_items[i], 0)
                    new_bins.sort()  # by ascending order of sum.
                    new_depth = numitems
                    stack.append((new_bins, new_depth))
                    continue

            next_item = sorted_items[depth]
            sum_of_remaining_items = sums_of_remaining_items[depth+1]

            previous_bin_sum = None
            for bin_index in reversed(range(bins.num)):   # by descending order of sum.

                # Heuristic 1: "If there are two subsets with the same sum, the current number is assigned to only one."
                current_bin_sum = current_bins.sums[bin_index]
                if current_bin_sum == previous_bin_sum:
                    continue   
                previous_bin_sum = current_bin_sum

                # Heuristic 2: lower bound (for the objective "minimize largest sum", it is:
                #    "If an assignment to a subset creates a subset sum that equals or exceeds the largest subset sum in the best complete solution found so far, that branch is pruned from the tree.")
                # if use_lower_bound:
                #     lower_bound = objective.lower_bound(current_bins.sums, valueof(next_item), bin_index, sum_of_remaining_items)
                #     if lower_bound >= best_objective_value:
                #         continue

                # Create the next vertex:
                new_bins = deepcopy(current_bins).add_item_to_bin(next_item, bin_index)
                new_bins.sort()  # by ascending order of sum.
                if use_lower_bound:
                    lower_bound = objective.lower_bound(new_bins.sums, sum_of_remaining_items, are_sums_in_ascending_order=True)
                    if lower_bound >= best_objective_value:
                        continue
                new_depth = depth + 1
                stack.append((new_bins, new_depth))

    logger.info("Checked %d out of %d partitions.", partitions_checked, bins.num**numitems)
    return best_bins


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))


    from prtpy.bins import BinsKeepingContents
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    optimal(BinsKeepingContents(2), [4,5,6,7,8], objective=obj.MinimizeLargestSum)
    
    walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MaximizeSmallestSum)
    optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeLargestSum)

