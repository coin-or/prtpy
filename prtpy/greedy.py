"""
    Partition the numbers using the greedy number partitioning algorithm
    (also known as "Longest Processing Time First" or LPT):
       https://en.wikipedia.org/wiki/Greedy_number_partitioning

    Credit: Code review by FMc at https://codereview.stackexchange.com/a/273975/20684.
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj


def greedy(
    numbins: int,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = None,  # Not used
    outputtype: out.OutputType = out.Partition,
):
    """
    Partition the given items using the greedy number partitioning algorithm.

    >>> greedy(numbins=2, items=[1,2,3,3,5,9,9], outputtype=out.Partition)
    [[9, 5, 2], [9, 3, 3, 1]]
    >>> greedy(numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.Partition)
    [[9, 2], [9, 1], [5, 3, 3]]
    >>> list(greedy(numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.Sums))
    [11.0, 10.0, 11.0]
    >>> greedy(numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.LargestSum)
    11.0

    >>> from prtpy.partitioning import partition
    >>> partition(algorithm=greedy, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
    >>> partition(algorithm=greedy, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])
    """
    bins = outputtype.create_empty_bins(numbins)
    for item in sorted(items, key=map_item_to_value, reverse=True):
        index_of_least_full_bin = min(range(bins.num), key=lambda i: bins.sums[i])
        bins.add_item_to_bin(
            item=item,
            value=map_item_to_value(item),
            bin_index=index_of_least_full_bin,
            inplace=True,
        )
    return outputtype.extract_output_from_bins(bins)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
