"""
The generic partition function.
"""

from outputs import (
    OutputFormat,
    Sums,
    LargestSum,
    SmallestSum,
    EntirePartition,
)
from typing import Callable


def partition(
    algorithm: Callable,
    num_of_bins: int,
    items: any = None,
    values: list[int] = None,
    output: OutputFormat = EntirePartition,
) -> list[list[int]]:
    """
    Partition the numbers using the greedy number partitioning algorithm.
    >>> from greedy import greedy
    >>> import numpy as np
    >>> partition(algorithm=greedy, num_of_bins=2, values=[1,2,3,3,5,9,9])
    [[9, 5, 2], [9, 3, 3, 1]]
    >>> partition(algorithm=greedy, num_of_bins=3, values=[1,2,3,3,5,9,9])
    [[9, 2], [9, 1], [5, 3, 3]]
    >>> partition(algorithm=greedy, num_of_bins=3, values=[1,2,3,3,5,9,9], output=LargestSum)
    11.0
    >>> partition(algorithm=greedy, num_of_bins=2, values=np.array([1,2,3,3,5,9,9]), output=Sums)
    array([16., 16.])
    >>> partition(algorithm=greedy, num_of_bins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'e', 'b'], ['g', 'c', 'd', 'a']]
    >>> partition(algorithm=greedy, num_of_bins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
    """
    if values is not None:
        map_item_to_value = lambda item: item
        item_names = values
    elif items is not None:
        map_item_to_value = lambda item: items[item]
        item_names = items.keys()
    else:
        raise ValueError("Either items or sizes must be given as an input")
    bins = output.get_empty_bins(num_of_bins)
    algorithm(bins, item_names, map_item_to_value)
    return output.get_output(bins)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
