"""
    Partition numbers using dynamic programming.

    >>> from partition import partition
    >>> partition(algorithm=dynamic_programming, numbins=2, values=[1,2,3,3,5,9,9])
    [[9, 5, 2], [9, 3, 3, 1]]
    >>> #partition(algorithm=dynamic_programming, numbins=3, values=[1,2,3,3,5,9,9])
    [[9, 2], [9, 1], [5, 3, 3]]
    >>> #partition(algorithm=dynamic_programming, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'e', 'b'], ['g', 'c', 'd', 'a']]
    >>> #partition(algorithm=dynamic_programming, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
"""

from bins import Bins, add_input_to_bin_sum, add_input_to_bin
from outputtypes import *
from typing import Callable, List, Any
from dynprog.sequential import SequentialDynamicProgram
import dynprog


def dynamic_programming(
    bins: Bins,
    items: List[Any],
    map_item_to_value: Callable[[Any], float],
):
    numbins = bins.num

    class PartitionDP(SequentialDynamicProgram):
        # The states are of the form  (v1, v2, ..., vn) where n is the number of bins.
        # The "vi" is the current sum in bin i.
        def initial_states(self):
            zero_values = numbins * (0,)
            return {zero_values}

        def initial_solution(self):
            empty_bundles = [[] for _ in range(numbins)]
            return empty_bundles

        def transition_functions(self):
            return [
                lambda state, input, bin_index=bin_index: add_input_to_bin_sum(
                    state, bin_index, map_item_to_value(input)
                )
                for bin_index in range(numbins)
            ]

        def construction_functions(self):
            return [
                lambda solution, input, bin_index=bin_index: add_input_to_bin(
                    solution, bin_index, input
                )
                for bin_index in range(numbins)
            ]

        def value_function(self):
            return lambda state: min(state)

    return PartitionDP().max_value(items)


if __name__ == "__main__":
    import doctest, logging

    dynprog.logger.addHandler(logging.StreamHandler())
    dynprog.logger.setLevel(logging.INFO)

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
