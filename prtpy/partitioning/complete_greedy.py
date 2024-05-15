"""
    Partition the numbers using the Complete Greedy number partitioning algorithm (Korf, 1995):
           https://en.wikipedia.org/wiki/Greedy_number_partitioning

    Credits: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
           https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning/greedy.py

    This stackoverflow question:
        https://stackoverflow.com/q/51635177/827927
    explains how to have a set with a custom key.

    Programmer: Erel Segal-Halevi
    Eitan Lichtman added Minimize Distance from Avg Objective
"""
import math
from typing import List, Tuple, Callable, Iterator, Any
import numpy as np
import logging, time

from prtpy import objectives as obj, Binner, BinsArray

logger = logging.getLogger(__name__)


def anytime(
    binner: Binner, numbins: int, items: List[any], relative_value: List[any] = None,
    objective: obj.Objective = obj.MinimizeDifference,
    use_lower_bound: bool = True,
    # Prune branches whose lower bound (= optimistic value) is at least as large as the current minimum.
    use_fast_lower_bound: bool = True,
    # A faster lower bound, that does not create the branch at all. Useful for min-max max-min and min-dist-avg objectives.
    use_heuristic_3: bool = False,
    # An improved stopping condition, applicable for min-max only. Not very useful in experiments.
    use_set_of_seen_states: bool = True,
    time_limit: float = np.inf,
) -> Iterator:
    """
    Finds a partition in which the largest sum is minimal, using the Complete Greedy algorithm.

    :param objective: represents the function that should be optimized. Default is minimizing the difference between bin sums.
    :param time_limit: determines how much time (in seconds) the function should run before it stops. Default is infinity.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums, printbins
    >>> printbins(anytime(BinnerKeepingContents(), 2, [4,5,6,7,8], objective=obj.MinimizeDifference))
    Bin #0: [6, 5, 4], sum=15.0
    Bin #1: [8, 7], sum=15.0

    >>> printbins(anytime(BinnerKeepingContents(), 2, [4,5,6,7,8], [0.3,0.7], objective=obj.MinimizeDistAvg))
    Bin #0: [5, 4], sum=9.0
    Bin #1: [8, 7, 6], sum=21.0

    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> printbins(anytime(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeDifference))
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    >>> printbins(anytime(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeLargestSum))
    Bin #0: [27, 26], sum=53.0
    Bin #1: [39, 13, 10], sum=62.0
    Bin #2: [46, 16], sum=62.0
    >>> printbins(anytime(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MaximizeSmallestSum))
    Bin #0: [46, 10], sum=56.0
    Bin #1: [27, 16, 13], sum=56.0
    Bin #2: [39, 26], sum=65.0
    >>> printbins(anytime(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeDistAvg))
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    >>> printbins(anytime(BinnerKeepingContents(), 3, walter_numbers,[0.2,0.4,0.4], objective=obj.MinimizeDistAvg))
    Bin #0: [27, 10], sum=37.0
    Bin #1: [39, 16, 13], sum=68.0
    Bin #2: [46, 26], sum=72.0

    >>> printbins(anytime(BinnerKeepingContents(), 5, [460000000, 390000000, 270000000, 260000000, 160000000, 130000000, 100000000],[0.2,0.4,0.1,0.15,0.15], objective=obj.MinimizeDistAvg))
    Bin #0: [390000000], sum=390000000.0
    Bin #1: [460000000, 130000000, 100000000], sum=690000000.0
    Bin #2: [160000000], sum=160000000.0
    Bin #3: [260000000], sum=260000000.0
    Bin #4: [270000000], sum=270000000.0


    >>> printbins(anytime(BinnerKeepingContents(), 10, [115268834, 22638149, 35260669, 68111031, 13376625, 20835125, 179398684, 69888000, 94462800, 5100340, 27184906, 305371, 272847, 545681, 1680746, 763835, 763835], [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1], objective=obj.MinimizeDistAvg))
    Bin #0: [13376625, 5100340, 1680746, 763835, 763835, 545681, 305371, 272847], sum=22809280.0
    Bin #1: [20835125], sum=20835125.0
    Bin #2: [22638149], sum=22638149.0
    Bin #3: [27184906], sum=27184906.0
    Bin #4: [35260669], sum=35260669.0
    Bin #5: [68111031], sum=68111031.0
    Bin #6: [69888000], sum=69888000.0
    Bin #7: [94462800], sum=94462800.0
    Bin #8: [115268834], sum=115268834.0
    Bin #9: [179398684], sum=179398684.0


    >>> printbins(anytime(BinnerKeepingContents(), 3, walter_numbers,[0.1,0.9,0], objective=obj.MinimizeDistAvg))
    Bin #0: [16], sum=16.0
    Bin #1: [46, 39, 27, 26, 13, 10], sum=161.0
    Bin #2: [], sum=0.0


    >>> printbins(anytime(BinnerKeepingContents(), 5, [2,2,5,5,5,5,9], objective=obj.MinimizeDistAvg))
    Bin #0: [5], sum=5.0
    Bin #1: [5], sum=5.0
    Bin #2: [5, 2], sum=7.0
    Bin #3: [5, 2], sum=7.0
    Bin #4: [9], sum=9.0
    >>> printbins(anytime(BinnerKeepingContents(), 3, [1,1,1,1], objective=obj.MinimizeDistAvg))
    Bin #0: [1], sum=1.0
    Bin #1: [1], sum=1.0
    Bin #2: [1, 1], sum=2.0
    >>> printbins(anytime(BinnerKeepingContents(), 3, [1,1,1,1,1], objective=obj.MinimizeDistAvg))
    Bin #0: [1], sum=1.0
    Bin #1: [1, 1], sum=2.0
    Bin #2: [1, 1], sum=2.0

    Compare results with and without the lower bound:
    >>> random_numbers = np.random.randint(1, 2**48-1, 10, dtype=np.int64)
    >>> objective = obj.MinimizeDifference
    >>> bins1=anytime(BinnerKeepingSums(), 3, random_numbers, objective=objective, use_lower_bound=True)
    >>> bins2=anytime(BinnerKeepingSums(), 3, random_numbers, objective=objective, use_lower_bound=False)
    >>> objective.value_to_minimize(bins1)==objective.value_to_minimize(bins2)
    True
    >>> objective = obj.MinimizeLargestSum
    >>> bins1=anytime(BinnerKeepingSums(), 3, random_numbers, objective=objective, use_lower_bound=True)
    >>> bins2=anytime(BinnerKeepingSums(), 3, random_numbers, objective=objective, use_lower_bound=False)
    >>> objective.value_to_minimize(bins1)==objective.value_to_minimize(bins2)
    True
    >>> objective = obj.MaximizeSmallestSum
    >>> bins1=anytime(BinnerKeepingSums(), 3, random_numbers, objective=objective, use_lower_bound=True)
    >>> bins2=anytime(BinnerKeepingSums(), 3, random_numbers, objective=objective, use_lower_bound=False)
    >>> objective.value_to_minimize(bins1)==objective.value_to_minimize(bins2)
    True

    Compare results with and without the heuristic 3:
    >>> random_numbers = np.random.randint(1, 2**48-1, 10, dtype=np.int64)
    >>> objective = obj.MinimizeLargestSum
    >>> bins1=anytime(BinnerKeepingSums(), 3, random_numbers, objective=objective, use_heuristic_3=True)
    >>> bins2=anytime(BinnerKeepingSums(), 3, random_numbers, objective=objective, use_heuristic_3=False)
    >>> objective.value_to_minimize(bins1)==objective.value_to_minimize(bins2)
    True

    Partitioning items with names:
    >>> from prtpy import partition, outputtypes as out
    >>> partition(algorithm=anytime, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['g', 'a'], ['f', 'b'], ['e', 'c', 'd']]
    >>> partition(algorithm=anytime, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    [16.0, 16.0]
    """
    numitems = len(items)
    start_time = time.perf_counter()
    end_time = start_time + time_limit

    sorted_items = sorted(items, key=binner.valueof, reverse=True)
    sums_of_remaining_items = [sum(map(binner.valueof, sorted_items[i:])) for i in range(numitems)] + [
        0]  # For Heuristic 3
    from prtpy import BinnerKeepingContents, BinnerKeepingSums, printbins
    best_bins, best_objective_value = None, np.inf


    global_lower_bound = objective.lower_bound(np.zeros(numbins), sums_of_remaining_items[0],
                                               are_sums_in_ascending_order=True)

    logger.info("\nComplete Greedy %s Partitioning of %d items into %d parts. Lower bound: %s", objective, numitems,
                numbins, global_lower_bound)

    # Create a stack whose elements are a partition and the current depth.
    # Initially, it contains a single tuple: an empty partition with depth 0.
    # If the input has relative values for each bin -
    # we add a sum to each bin in order to equal them out to the bin with the highest relative value
    # (at the end of the algorithm we will remove these sums).
    first_bins = binner.new_bins(numbins)
    if (relative_value):
        for i in range(numbins):
            binner.add_item_to_bin(first_bins, (max(relative_value) * sum(items) - relative_value[i] * sum(items)), i)
    first_vertex = (first_bins, 0)
    stack: List[Tuple[BinsArray, int]] = [first_vertex]
    if use_set_of_seen_states:
        seen_states = set(tuple(binner.sums(first_bins)))
    # For logging and profiling:
    complete_partitions_checked = 0
    intermediate_partitions_checked = 1

    times_fast_lower_bound_activated = 0
    times_lower_bound_activated = 0
    times_heuristic_3_activated = 0
    times_seen_state_skipped = 0

    while len(stack) > 0:
        if time.perf_counter() > end_time:
            logger.info("Time-limit of %s reached - stopping", time_limit)
            break

        current_bins, depth = stack.pop()
        current_sums = tuple(binner.sums(current_bins))

        # If we have reached the leaves of the DFS tree, check if we have an improvement:
        if depth == numitems:
            complete_partitions_checked += 1
            new_objective_value = objective.value_to_minimize(current_sums)
            if new_objective_value < best_objective_value:
                best_bins, best_objective_value = current_bins, new_objective_value
                logger.info("  Found a better solution: %s, with value %s", current_bins, best_objective_value)
                if new_objective_value <= global_lower_bound:
                    logger.info("    Solution matches global lower bound - stopping")
                    break
            continue
        # Heuristic 3: "If the sum of the remaining unassigned integers plus the smallest current subset sum is <= the largest subset sum, all remaining integers are assigned to the subset with the smallest sum, terminating that branch of the tree."
        # Note that this heuristic is valid only for the objective "minimize largest sum"!
        if use_heuristic_3 and objective == obj.MinimizeLargestSum:
            if sums_of_remaining_items[depth] + current_sums[0] <= current_sums[-1]:
                new_bins = binner.copy_bins(current_bins)
                for i in range(depth, numitems):
                    binner.add_item_to_bin(new_bins, sorted_items[i], 0)
                    binner.sort_by_ascending_sum(new_bins)
                new_depth = numitems
                stack.append((new_bins, new_depth))
                logger.debug("    Heuristic 3 activated")
                times_heuristic_3_activated += 1
                continue
        next_item = sorted_items[depth]
        sum_of_remaining_items = sums_of_remaining_items[depth + 1]

        previous_bin_sum = None

        # We want to insert the next item to the bin with the *smallest* sum first.
        # But, since we use a stack, we have to insert it to the bin with the *largest* sum first,
        # so that it is pushed deeper into the stack.
        # Therefore, we proceed in reverse, by *descending* order of sum.
        for bin_index in reversed(range(numbins)):

            # Heuristic 1: "If there are two subsets with the same sum, the current number is assigned to only one."
            current_bin_sum = current_sums[bin_index]
            if current_bin_sum == previous_bin_sum:
                continue
            previous_bin_sum = current_bin_sum

            # Fast-lower-bound heuristic - before creating the new vertex.
            # Currently implemented only for two objectives: min-max, max-min and min-dist-avg
            if use_fast_lower_bound:
                if objective == obj.MinimizeLargestSum:
                    # "If an assignment to a subset creates a subset sum that equals or exceeds the largest subset sum in the best complete solution found so far, that branch is pruned from the tree."
                    fast_lower_bound = max(current_bin_sum + binner.valueof(next_item), current_sums[-1])
                elif objective == obj.MaximizeSmallestSum:
                    # An adaptation of the above heuristic to maximizing the smallest sum.
                    if bin_index == 0:
                        new_smallest_sum = min(current_sums[0] + binner.valueof(next_item), current_sums[1])
                    else:
                        new_smallest_sum = current_sums[0]
                    fast_lower_bound = -(new_smallest_sum + sum_of_remaining_items)
                elif objective == obj.MinimizeDistAvg:
                    if relative_value:
                        fast_lower_bound = 0
                        for i in range (numbins):
                            # For each bin: we take off the sum that we added in the beginning of the algorithm (max(relative_value) * sum(items) - relative_value[i] * sum(items))
                            # Then we check if the difference between the bin's sum and the relative AVG for bin i: (sum(items)*relative_value[i])
                            # is positive and contributes to our final difference or negative and we will not add anything to our difference.
                            fast_lower_bound = fast_lower_bound + max((current_sums[i]-(max(relative_value) * sum(items) - relative_value[i] * sum(items)))-sum(items)*relative_value[i],0)
                    else:
                        fast_lower_bound = 0
                        avg = sum(items) / numbins
                        for i in range (numbins):
                            fast_lower_bound = fast_lower_bound + max(current_sums[i]-avg,0)
                else:
                    fast_lower_bound = -np.inf
                if fast_lower_bound >= best_objective_value:
                    times_fast_lower_bound_activated += 1
                    continue

            new_bins = binner.add_item_to_bin(binner.copy_bins(current_bins), next_item, bin_index)
            if not relative_value:
                binner.sort_by_ascending_sum(new_bins)
            new_sums = tuple(binner.sums(new_bins))

            # Lower-bound heuristic. 
            if use_lower_bound:
                lower_bound = objective.lower_bound(new_sums, sum_of_remaining_items, are_sums_in_ascending_order=False)
                if lower_bound >= best_objective_value:
                    logger.debug("    Lower bound %f too large", lower_bound)
                    times_lower_bound_activated += 1
                    continue
            if use_set_of_seen_states:
                if new_sums in seen_states:
                    logger.debug("    State %s already seen", new_sums)
                    times_seen_state_skipped += 1
                    continue
                seen_states.add(new_sums)  # should be after if use_lower_bound

            new_vertex = (new_bins, depth + 1)
            stack.append(new_vertex)
            intermediate_partitions_checked += 1

    logger.info("Checked %d out of %d complete partitions, and %d intermediate partitions.",
                complete_partitions_checked, numbins ** numitems, intermediate_partitions_checked)
    logger.info("  Heuristics: fast lower bound = %d, lower bound = %d, seen state = %d, heuristic 3 = %d.",
                times_fast_lower_bound_activated, times_lower_bound_activated, times_seen_state_skipped,
                times_heuristic_3_activated)


    if (relative_value):
        # For each bin we remove the value that we added in the beginning of the algorithm.
        for i in range(numbins):
            binner.remove_item_from_bin(best_bins, i, 0)

    for i in range(numbins):
        binner.sums(best_bins)[i] = math.floor(binner.sums(best_bins)[i])
    return best_bins


if __name__ == "__main__":
    import doctest, sys

    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print("{} failures, {} tests".format(failures, tests))
    if failures > 0:
        sys.exit()
    
    # DEMO
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    from prtpy import BinnerKeepingContents, BinnerKeepingSums

    anytime(BinnerKeepingContents(), 2, [4, 5, 6, 7, 8], objective=obj.MinimizeLargestSum)

    walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    anytime(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MaximizeSmallestSum)
    anytime(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeLargestSum)

    random_numbers = np.random.randint(1, 2 ** 16 - 1, 15, dtype=np.int64)
    anytime(BinnerKeepingSums(), 3, random_numbers, objective=obj.MaximizeSmallestSum)
    anytime(BinnerKeepingSums(), 3, random_numbers, objective=obj.MinimizeLargestSum)
    anytime(BinnerKeepingSums(), 3, random_numbers, objective=obj.MinimizeDifference)
