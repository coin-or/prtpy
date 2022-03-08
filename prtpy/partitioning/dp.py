"""
Optimal number partitioning using dynamic programming.

Author: Erel Segal-Halevi
Since: 2022-02
"""

from prtpy import outputtypes as out, objectives as obj
from typing import Callable, List, Any, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


def optimal(
    numbins: int,
    items: List[Any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    outputtype: out.OutputType = out.Partition,
):

    """
    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> optimal(3, walter_numbers, objective=obj.MinimizeDifference, outputtype=out.Partition)
    [[39, 16], [46, 13], [27, 26, 10]]
    >>> optimal(3, walter_numbers, objective=obj.MinimizeLargestSum, outputtype=out.PartitionAndSums)
    Bin #0: [46, 16], sum=62.0
    Bin #1: [39, 13, 10], sum=62.0
    Bin #2: [27, 26], sum=53.0
    >>> optimal(3, walter_numbers, objective=obj.MaximizeSmallestSum, outputtype=out.Sums)
    (56, 56, 65)
    >>> optimal(3, walter_numbers, objective=obj.MaximizeSmallestSum, outputtype=out.SmallestSum)
    56
    """
    if hasattr(outputtype, 'extract_output_from_sums'):
        # We need only the sums - not the entire partition.
        return _optimal_sums(numbins, items, map_item_to_value, objective, outputtype)
    else:
        # We need the entire partition.
        return _optimal_partition(numbins, items, map_item_to_value, objective, outputtype)




def _optimal_sums(
    numbins: int,
    items: List[Any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    outputtype: out.OutputType = out.Sums,
):
    """
    A DP that computes only the optimal sums in the bins (not the optimal partition itself).

    The states are of the form  (v1, v2, ..., vn) where n is the number of bins.
    The "vi" is the current sum in bin i.
    """

    # Construct initial states:
    zero_values = numbins * (0,)
    current_states = {zero_values}
    num_of_processed_states = len(current_states)

    for item in items:
        value = map_item_to_value(item)

        # Construct next states:
        next_states = set()
        for state in current_states:
            for ibin in range(numbins):
                next_state = list(state)
                next_state[ibin] += value
                next_states.add(tuple(next_state))
        logger.info(
            "  Processed item %s and added %d states.",
            input,
            len(next_states),
        )
        num_of_processed_states += len(next_states)
        current_states = next_states

    logger.info("Processed %d states.", num_of_processed_states)
    if len(current_states) == 0:
        raise ValueError("No final states!")
    best_final_state = min(
        current_states, key=objective.get_value_to_minimize
    )
    best_final_state_value = objective.get_value_to_minimize(best_final_state)
    logger.info(
        "Best final state: %s, value: %s",
        best_final_state,
        best_final_state_value,
    )
    return outputtype.extract_output_from_sums(best_final_state)


def _optimal_partition(
    numbins: int,
    items: List[Any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    outputtype: out.OutputType = out.Partition,
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
        value = map_item_to_value(item)

        # Construct next state records:
        next_state_records = set()
        for record in current_state_records:
            for ibin in range(numbins):
                next_state = list(record.state)
                next_state[ibin] += value
                next_state_record = StateRecord(tuple(next_state), record, ibin)
                next_state_records.add(next_state_record)
        logger.info(
            "  Processed item %s and added %d state reccords.",
            input,
            len(next_state_records),
        )
        num_of_processed_states += len(next_state_records)
        current_state_records = next_state_records

    logger.info("Processed %d states.", num_of_processed_states)
    if len(current_state_records) == 0:
        raise ValueError("No final states!")
    best_final_record = min(
        current_state_records, key=lambda record: objective.get_value_to_minimize(record.state)
    )

    # construct path to solution
    path = []
    record = best_final_record
    while record.prev is not None:
        path.insert(0, record.ibin)
        record = record.prev
    logger.info("Path to best solution: %s", path)

    # construct solution
    bins = outputtype.create_empty_bins(numbins)
    for item_index, item in enumerate(items):
        ibin = path[item_index]
        logger.info("  Item %d (%s): bin %d", item_index, item, ibin,)
        bins.add_item_to_bin(item, map_item_to_value(item), ibin, inplace=True)
    return outputtype.extract_output_from_bins(bins)



if __name__ == "__main__":
    import doctest, logging

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
