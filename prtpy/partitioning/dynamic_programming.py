"""
Optimal number partitioning using dynamic programming.

NOTE: The implementation uses sets of states. 
An alternative implementation would be to use a boolean matrix.
I compared the implementations, and the boolean matrix implementation is about 100x slower on random inputs of 8 bits or more.
This is probably because the boolean matrix is very large and it takes a lot of time to go over it.

Author: Erel Segal-Halevi
Since: 2022-02
"""

from prtpy import outputtypes as out, objectives as obj, Bins, Binner, BinnerKeepingContents, BinnerKeepingSums, printbins
from typing import Callable, List, Any, Tuple
from dataclasses import dataclass
import logging, numpy as np

logger = logging.getLogger(__name__)


def optimal(
    binner: Binner, numbins: int, items: List[any],
    objective: obj.Objective = obj.MinimizeDifference,
    **kwargs
):

    """
    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums
    >>> printbins(optimal(BinnerKeepingContents(), 2, [1,1,1,1,2], objective=obj.MaximizeSmallestSum))
    Bin #0: [1, 1, 1], sum=3.0
    Bin #1: [1, 2], sum=3.0

    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeDifference))
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeLargestSum))
    Bin #0: [46, 16], sum=62.0
    Bin #1: [39, 13, 10], sum=62.0
    Bin #2: [27, 26], sum=53.0
    >>> printbins(optimal(BinnerKeepingSums(), 3, walter_numbers, objective=obj.MaximizeSmallestSum))
    Bin #0: sum=56.0
    Bin #1: sum=56.0
    Bin #2: sum=65.0

    >>> from prtpy import partition
    >>> partition(algorithm=optimal, numbins=3, items={"a":46, "b":39, "c":27, "d":26, "e":16, "f":13, "g":10}, objective=obj.MinimizeDifference, outputtype=out.Partition)
    [['b', 'e'], ['a', 'f'], ['c', 'd', 'g']]
    """
    if isinstance(binner, BinnerKeepingSums):
        # We need the entire partition.
        return _optimal_partition(binner, numbins, items, objective, **kwargs)
    else:
        # We need only the sums - not the entire partition.
        return _optimal_sums(binner, numbins, items, objective, **kwargs)




def _optimal_sums(
    binner: Binner, numbins: int, items: List[any],
    objective: obj.Objective = obj.MinimizeDifference,
):
    """
    A DP that computes only the optimal sums in the bins (not the optimal partition itself).

    The states are of the form  (v1, v2, ..., vn) where n is the number of bins.
    The "vi" is the current sum in bin i.
    """

    logger.info("\nDynamic Programming %s Partitioning of %d items into %d bins.", objective, len(items), numbins)

    first_state = binner.new_bins(numbins)
    num_of_processed_states = 1

    # Construct initial states:
    current_states = {tuple(binner.sums(first_state))}
    for item in items:
        value = binner.valueof(item)

        # Construct next states:
        next_states = set()
        for state in current_states:
            for ibin in range(numbins):
                next_state = binner.add_item_to_bin(binner.clone(state), item, ibin)
                binner.sort_by_ascending_sum(next_state)
                next_states.add(tuple(binner.sums(next_state)))
        states_added = len(next_states)
        logger.info("  Processed item %s and added %d states.", item, states_added)
        num_of_processed_states += states_added
        current_states = next_states

    if len(current_states) == 0:
        raise ValueError("No final states!")
    best_final_state = min(current_states, key=objective.value_to_minimize)
    best_final_state_value = objective.value_to_minimize(best_final_state)
    logger.info("Processed %d states.", num_of_processed_states)
    logger.info("Best final state: %s, value: %s", best_final_state, best_final_state_value)
    return best_final_state


def _optimal_partition(
    binner: Binner, numbins: int, items: List[any],
    objective: obj.Objective = obj.MinimizeDifference,
):
    """
    A DP that computes both the optimal sums and the optimal partition.

    The states are of the form  (v1, v2, ..., vn) where n is the number of bins.
    The "vi" is the current sum in bin i.
    """
    items = list(items)
    # allow to iterate twice. See https://stackoverflow.com/q/70381559/827927
    State = Tuple[float]

    @dataclass
    class StateRecord:
        state: State
        prev: Any  # StateRecord
        ibin: int  # the index of the bin to which the last item was added in order to get to this state.
        def __hash__(self):
            return hash(self.state)
        def __eq__(self, other):
            return self.state == other.state

    # Construct initial states:
    zero_values = numbins * (0,)
    current_state_records = {StateRecord(zero_values, None, None)}
    num_of_processed_states = len(current_state_records)

    for item in items:
        value = binner.valueof(item)

        # Construct next state records:
        next_state_records = set()
        for record in current_state_records:
            for ibin in range(numbins):
                next_state = list(record.state)
                next_state[ibin] += value
                next_state_record = StateRecord(tuple(next_state), record, ibin)
                next_state_records.add(next_state_record)
        logger.info("  Processed item %s and added %d state reccords.", item, len(next_state_records))
        num_of_processed_states += len(next_state_records)
        current_state_records = next_state_records

    logger.info("Processed %d states.", num_of_processed_states)
    if len(current_state_records) == 0:
        raise ValueError("No final states!")
    best_final_record = min(
        current_state_records, key=lambda record: objective.value_to_minimize(record.state)
    )

    # construct path to solution
    path = []
    record = best_final_record
    while record.prev is not None:
        path.insert(0, record.ibin)
        record = record.prev
    logger.info("Path to best solution: %s", path)

    # construct solution
    result_bins = binner.new_bins(numbins)
    for item_index, item in enumerate(items):
        ibin = path[item_index]
        logger.info("  Item %d (%s): bin %d", item_index, item, ibin,)
        binner.add_item_to_bin(result_bins, item, ibin)
    return result_bins


if __name__ == "__main__":
    # DOCTEST
    import doctest, sys
    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print("{} failures, {} tests".format(failures, tests))
    if failures>0:
        sys.exit(1)

    # DEMO
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    from prtpy.bins import BinsKeepingContents, BinsKeepingSums

    optimal(BinnerKeepingSums(), 2, [4,5,6,7,8], objective=obj.MinimizeLargestSum)
    walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    optimal(BinnerKeepingSums(), 3, walter_numbers, objective=obj.MaximizeSmallestSum)
    optimal(BinnerKeepingSums(), 3, walter_numbers, objective=obj.MinimizeLargestSum)
