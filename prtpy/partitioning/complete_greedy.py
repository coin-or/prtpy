"""
    Partition the numbers using the Complete Greedy number partitioning algorithm (Korf, 1995):
           https://en.wikipedia.org/wiki/Greedy_number_partitioning

    Credits: based on code by Søren Fuglede Jørgensen in the numberpartitioning package:
           https://github.com/fuglede/numberpartitioning/blob/master/src/numberpartitioning/greedy.py

    This stackoverflow question:
        https://stackoverflow.com/q/51635177/827927
    explains how to have a set with a custom key.
"""

from typing import List, Tuple, Callable, Iterator, Any
import numpy as np
import logging, time
from prtpy import objectives as obj, Bins, BinsArray

logger = logging.getLogger(__name__)



def anytime(
    bins: Bins,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    use_lower_bound: bool = True,   # Prune branches whose lower bound (= optimistic value) is at least as large as the current minimum.
    use_fast_lower_bound: bool = True,   # A faster lower bound, that does not create the branch at all. Useful for min-max and max-min objectives.
    use_heuristic_3: bool = False,  # An improved stopping condition, applicable for min-max only. Not very useful in experiments.
    use_set_of_seen_states: bool = True, 
    time_limit: float = np.inf,
) -> Iterator:
    """
    Finds a partition in which the largest sum is minimal, using the Complete Greedy algorithm.

    :param objective: represents the function that should be optimized. Default is minimizing the difference between bin sums.
    :param time_limit: determines how much time (in seconds) the function should run before it stops. Default is infinity.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> anytime(BinsKeepingContents(2), [4,5,6,7,8], objective=obj.MinimizeDifference)
    Bin #0: [6, 5, 4], sum=15.0
    Bin #1: [8, 7], sum=15.0

    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> anytime(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeDifference)
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    >>> anytime(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeLargestSum)
    Bin #0: [27, 26], sum=53.0
    Bin #1: [39, 13, 10], sum=62.0
    Bin #2: [46, 16], sum=62.0
    >>> anytime(BinsKeepingContents(3), walter_numbers, objective=obj.MaximizeSmallestSum)
    Bin #0: [46, 10], sum=56.0
    Bin #1: [27, 16, 13], sum=56.0
    Bin #2: [39, 26], sum=65.0

    Compare results with and without the lower bound:
    >>> random_numbers = np.random.randint(1, 2**48-1, 10, dtype=np.int64)
    >>> objective = obj.MinimizeDifference
    >>> bins1=anytime(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=True)
    >>> bins2=anytime(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=False)
    >>> objective.value_to_minimize(bins1.sums)==objective.value_to_minimize(bins2.sums)
    True
    >>> objective = obj.MinimizeLargestSum
    >>> bins1=anytime(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=True)
    >>> bins2=anytime(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=False)
    >>> objective.value_to_minimize(bins1.sums)==objective.value_to_minimize(bins2.sums)
    True
    >>> objective = obj.MaximizeSmallestSum
    >>> bins1=anytime(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=True)
    >>> bins2=anytime(BinsKeepingSums(3), random_numbers, objective=objective, use_lower_bound=False)
    >>> objective.value_to_minimize(bins1.sums)==objective.value_to_minimize(bins2.sums)
    True

    Compare results with and without the heuristic 3:
    >>> random_numbers = np.random.randint(1, 2**48-1, 10, dtype=np.int64)
    >>> objective = obj.MinimizeLargestSum
    >>> bins1=anytime(BinsKeepingSums(3), random_numbers, objective=objective, use_heuristic_3=True)
    >>> bins2=anytime(BinsKeepingSums(3), random_numbers, objective=objective, use_heuristic_3=False)
    >>> objective.value_to_minimize(bins1.sums)==objective.value_to_minimize(bins2.sums)
    True

    Partitioning items with names:
    >>> from prtpy import partition, outputtypes as out
    >>> partition(algorithm=anytime, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['g', 'a'], ['f', 'b'], ['e', 'c', 'd']]
    >>> partition(algorithm=anytime, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    [16.0, 16.0]
    """
    binner = bins.get_binner()

    numitems = len(items)
    start_time = time.perf_counter()
    end_time = start_time + time_limit

    sorted_items = sorted(items, key=valueof, reverse=True)
    sums_of_remaining_items = [sum(map(valueof, sorted_items[i:])) for i in range(numitems)] + [0] # For Heuristic 3
    best_bins, best_objective_value = None, np.inf

    global_lower_bound = objective.lower_bound(np.zeros(binner.numbins), sums_of_remaining_items[0], are_sums_in_ascending_order=True)

    logger.info("\nComplete Greedy %s Partitioning of %d items into %d parts. Lower bound: %s", objective, numitems, binner.numbins, global_lower_bound)

    # Create a stack whose elements are a partition and the current depth.
    # Initially, it contains a single tuple: an empty partition with depth 0.
    first_bins  = binner.new_bins()
    first_vertex = (first_bins, 0)
    stack: List[Tuple[BinsArray, int]] = [first_vertex]
    if use_set_of_seen_states:
        seen_states = set(binner.sums_as_tuple(first_bins))

    # For logging and profiling:
    complete_partitions_checked = 0      
    intermediate_partitions_checked = 1  

    times_fast_lower_bound_activated = 0
    times_lower_bound_activated = 0
    times_heuristic_3_activated = 0
    times_seen_state_skipped = 0

    while len(stack) > 0:
        current_bins, depth = stack.pop()
        current_sums = binner.sums_as_tuple(current_bins)

        # If we have reached the leaves of the DFS tree, check if we have an improvement:
        if depth == numitems:
            complete_partitions_checked += 1
            new_objective_value = objective.value_to_minimize(current_sums)
            if new_objective_value < best_objective_value:
                best_bins, best_objective_value = current_bins, new_objective_value
                logger.info("  Found a better solution: %s, with value %s", current_bins, best_objective_value)
                if new_objective_value<=global_lower_bound:
                    logger.info("    Solution matches global lower bound - stopping")
                    break
            if time.perf_counter() > end_time:
                logger.info("Time-limit of %s reached - stopping", time_limit)
                break
            continue

        # Heuristic 3: "If the sum of the remaining unassigned integers plus the smallest current subset sum is <= the largest subset sum, all remaining integers are assigned to the subset with the smallest sum, terminating that branch of the tree."
        # Note that this heuristic is valid only for the objective "minimize largest sum"!
        if use_heuristic_3 and objective==obj.MinimizeLargestSum:
            if sums_of_remaining_items[depth] + current_sums[0] <= current_sums[-1]:
                new_bins = binner.clone(current_bins)
                for i in range(depth,numitems):
                    binner.add_item_to_bin(new_bins, sorted_items[i], 0)
                binner.sort_by_ascending_sum(new_bins)
                new_depth = numitems
                stack.append((new_bins, new_depth))
                logger.debug("    Heuristic 3 activated")
                times_heuristic_3_activated+=1
                continue

        next_item = sorted_items[depth]
        sum_of_remaining_items = sums_of_remaining_items[depth+1]

        previous_bin_sum = None

        # We want to insert the next item to the bin with the *smallest* sum first.
        # But, since we use a stack, we have to insert it to the bin with the *largest* sum first,
        # so that it is pushed deeper into the stack.
        # Therefore, we process the bins in reverse, by *descending* order of sum.
        for bin_index in reversed(range(binner.numbins)):   

            # Heuristic 1: "If there are two subsets with the same sum, the current number is assigned to only one."
            current_bin_sum = current_sums[bin_index]
            if current_bin_sum == previous_bin_sum:
                continue   
            previous_bin_sum = current_bin_sum

            # Fast-lower-bound heuristic - before creating the new vertex.
            # Currently implemented only for two objectives: min-max and max-min.
            if use_fast_lower_bound:
                if objective==obj.MinimizeLargestSum:
                    # "If an assignment to a subset creates a subset sum that equals or exceeds the largest subset sum in the best complete solution found so far, that branch is pruned from the tree."
                    fast_lower_bound = max(current_bin_sum + valueof(next_item), current_sums[-1])
                elif objective==obj.MaximizeSmallestSum:
                    # An adaptation of the above heuristic to maximizing the smallest sum.
                    if bin_index==0:
                        new_smallest_sum = min(current_sums[0]+valueof(next_item), current_sums[1])
                    else:
                        new_smallest_sum = current_sums[0]
                    fast_lower_bound = -(new_smallest_sum+sum_of_remaining_items)
                else:
                    fast_lower_bound = -np.inf
                if fast_lower_bound >= best_objective_value:
                    times_fast_lower_bound_activated += 1
                    continue

            new_bins = binner.clone(current_bins)
            binner.add_item_to_bin(new_bins, next_item, bin_index)
            binner.sort_by_ascending_sum(new_bins)
            new_sums = binner.sums_as_tuple(new_bins)

            # Lower-bound heuristic. 
            if use_lower_bound:
                lower_bound = objective.lower_bound(new_sums, sum_of_remaining_items, are_sums_in_ascending_order=True)
                if lower_bound >= best_objective_value:
                    logger.debug("    Lower bound %f too large", lower_bound)
                    times_lower_bound_activated += 1
                    continue
            if use_set_of_seen_states: 
                if new_sums in seen_states:
                    logger.debug("    State %s already seen", new_sums)
                    times_seen_state_skipped += 1
                    continue
                seen_states.add(new_sums)   # should be after if use_lower_bound

            new_vertex = (new_bins, depth + 1)
            stack.append(new_vertex)
            intermediate_partitions_checked += 1

    logger.info("Checked %d out of %d complete partitions, and %d intermediate partitions.", complete_partitions_checked, bins.num**numitems, intermediate_partitions_checked)
    logger.info("  Heuristics: fast lower bound = %d, lower bound = %d, seen state = %d, heuristic 3 = %d.", times_fast_lower_bound_activated, times_lower_bound_activated, times_seen_state_skipped, times_heuristic_3_activated)

    return best_bins


if __name__ == "__main__":
    import doctest, sys

    from prtpy.binners import BinnerKeepingContents, BinnerKeepingSums
    from prtpy.bins    import BinsKeepingContents, BinsKeepingSums

    print(anytime(BinsKeepingContents(2), [4,5,6,7,8], objective=obj.MinimizeDifference))
    sys.exit()

    # DOCTEST
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    if failures>0: 
      sys.exit()

    # DEMO
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    from prtpy.bins import BinsKeepingContents, BinsKeepingSums

    # anytime(BinsKeepingContents(2), [4,5,6,7,8], objective=obj.MinimizeLargestSum)

    # walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    # anytime(BinsKeepingContents(3), walter_numbers, objective=obj.MaximizeSmallestSum)
    # anytime(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeLargestSum)

    random_numbers = np.random.randint(1, 2**16-1, 15, dtype=np.int64)
    # anytime(BinsKeepingSums(3), random_numbers, objective=obj.MinimizeLargestSum, use_fast_lower_bound=False, use_lower_bound=False, use_set_of_seen_states=False, use_heuristic_3=True)
    # anytime(BinsKeepingSums(3), random_numbers, objective=obj.MinimizeLargestSum, use_fast_lower_bound=False, use_lower_bound=False, use_set_of_seen_states=True, use_heuristic_3=False)
    # anytime(BinsKeepingSums(3), random_numbers, objective=obj.MinimizeLargestSum, use_fast_lower_bound=False, use_lower_bound=True, use_set_of_seen_states=False, use_heuristic_3=False)
    # anytime(BinsKeepingSums(3), random_numbers, objective=obj.MinimizeLargestSum, use_fast_lower_bound=True, use_lower_bound=False, use_set_of_seen_states=False, use_heuristic_3=False)
    # anytime(BinsKeepingSums(3), random_numbers, objective=obj.MinimizeLargestSum, use_fast_lower_bound=True, use_lower_bound=False, use_set_of_seen_states=False, use_heuristic_3=True)
    # anytime(BinsKeepingSums(3), random_numbers, objective=obj.MaximizeSmallestSum)
    # anytime(BinsKeepingSums(3), random_numbers, objective=obj.MinimizeLargestSum)
    # anytime(BinsKeepingSums(3), random_numbers, objective=obj.MinimizeDifference)
    # anytime(BinsKeepingSums(3), random_numbers, objective=obj.MaximizeSmallestSum, use_lower_bound=False)


    def compare_ways_to_add_items():
        current_bins = BinsKeepingSums(3)
        current_bins.add_item_to_bin(10, 1).add_item_to_bin(20,2).add_item_to_bin(30,0).sort_by_ascending_sum()
        print(current_bins)
        times = 100000

        start = time.perf_counter()
        for _ in range(times):
            new_sums = list(current_bins.sums)
            new_sums[0] += current_bins.valueof(5)
            new_sums.sort()
        print("list: ",time.perf_counter()-start)
        
        start = time.perf_counter()
        for _ in range(times):
            current_bins.clone().add_item_to_bin(5, 0).sort_by_ascending_sum() 
        print("bins: ",time.perf_counter()-start)  # 1.5-2 times slower. (deepcopy is 10 times slower; __deepcopy__ is 3-4 times slower).
    compare_ways_to_add_items()
