"""
Optimal number partitioning using dynamic programming.
Uses a Boolean matrix to store the states. Very inefficient - do not use.

Author: Erel Segal-Halevi
Since: 2022-06
"""

from prtpy import outputtypes as out, objectives as obj, Bins
from typing import Callable, List, Any, Tuple
from dataclasses import dataclass
import logging, numpy as np

logger = logging.getLogger(__name__)


def optimal(
    bins: Bins,
    items: List[Any],
    valueof: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    **kwargs
):

    """
    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> optimal(BinsKeepingContents(2), [1,1,1,1,2], objective=obj.MaximizeSmallestSum).sums
    array([3., 3.])

    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> optimal(BinsKeepingSums(3), walter_numbers, objective=obj.MinimizeDifference)
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    >>> optimal(BinsKeepingSums(3), walter_numbers, objective=obj.MinimizeLargestSum)
    Bin #0: [46, 16], sum=62.0
    Bin #1: [39, 13, 10], sum=62.0
    Bin #2: [27, 26], sum=53.0
    >>> optimal(BinsKeepingSums(3), walter_numbers, objective=obj.MaximizeSmallestSum)
    Bin #0: sum=56
    Bin #1: sum=56
    Bin #2: sum=65

    >>> from prtpy import partition
    >>> partition(algorithm=optimal, numbins=3, items={"a":46, "b":39, "c":27, "d":26, "e":16, "f":13, "g":10}, objective=obj.MinimizeDifference, outputtype=out.Partition)
    [['b', 'e'], ['a', 'f'], ['c', 'd', 'g']]
    """
    if hasattr(bins, 'bins'):
        # We need the entire partition.
        raise NotImplementedError()
    else:
        # We need only the sums - not the entire partition.
        _optimal_sums(bins, items, valueof, objective, **kwargs)
    return bins




def _optimal_sums(
    bins: Bins,
    items: List[Any],
    valueof: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
):
    """
    A DP that computes only the optimal sums in the bins (not the optimal partition itself).

    The states are of the form  (v1, v2, ..., vn) where n is the number of bins.
    The "vi" is the current sum in bin i.
    """

    logger.info("\nDynamic Programming %s Partitioning of %d items into %d bins.", objective, len(items), bins.num)

    first_state = bins.num * (0,)
    num_of_processed_states = 1

    max_val = sum(map(valueof, items))
    matrix_dimensions = bins.num*(max_val+1,)
    possible_partitions_matrix = np.full(matrix_dimensions, False)
    possible_partitions_matrix[first_state] = True

    for item in items:
        value = valueof(item)

        # Construct next possible-partitions matrix
        new_possible_partitions_matrix = np.full(matrix_dimensions, False)
        it = np.nditer(possible_partitions_matrix, flags=['multi_index'])
        states_added = 0
        for element in it:
            if element:  # a possible partition
                current_index = it.multi_index
                # is_sorted = all(current_index[i] <= current_index[i+1] for i in range(bins.num - 1))
                # if not is_sorted: # to save time, process only sorted states.
                #     continue
                for ibin in range(bins.num):
                    new_index = list(current_index)
                    new_index[ibin] += value
                    new_index = tuple(sorted(new_index))
                    if not new_possible_partitions_matrix[new_index]:
                        states_added+=1
                        new_possible_partitions_matrix[new_index] = True
        logger.info("  Processed item %s and added %d states.", item, states_added)
        num_of_processed_states += states_added
        possible_partitions_matrix = new_possible_partitions_matrix

    # Find all feasible partitions:
    current_states = set()
    it = np.nditer(possible_partitions_matrix, flags=['multi_index'])
    for element in it:
        if element:  # a possible partition
            current_states.add(tuple(it.multi_index))
    if len(current_states) == 0:
        raise ValueError("No final states!")
    best_final_state = min(current_states, key=objective.value_to_minimize)
    best_final_state_value = objective.value_to_minimize(best_final_state)
    logger.info("Processed %d states.", num_of_processed_states)
    logger.info("Best final state: %s, value: %s", best_final_state, best_final_state_value)
    bins.sums = best_final_state



if __name__ == "__main__":
    # DOCTEST
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

    # DEMO
    # logger.setLevel(logging.INFO)
    # logger.addHandler(logging.StreamHandler())

    # from prtpy.bins import BinsKeepingContents, BinsKeepingSums

    # optimal(BinsKeepingSums(2), [4,5,6,7,8], objective=obj.MinimizeLargestSum)
    # walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    # optimal(BinsKeepingSums(3), walter_numbers, objective=obj.MaximizeSmallestSum)
    # optimal(BinsKeepingSums(3), walter_numbers, objective=obj.MinimizeLargestSum)

    # random_numbers = np.random.randint(1, 2**8-1, 15, dtype=np.int64)
    # optimal(BinsKeepingSums(3), random_numbers, objective=obj.MaximizeSmallestSum)
    # optimal(BinsKeepingSums(3), random_numbers, objective=obj.MinimizeLargestSum)
    # optimal(BinsKeepingSums(3), random_numbers, objective=obj.MinimizeDifference)
