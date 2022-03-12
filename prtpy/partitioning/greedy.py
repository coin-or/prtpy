"""
    Partition the numbers using the greedy number partitioning algorithm
    (also known as "Longest Processing Time First" or LPT):
       https://en.wikipedia.org/wiki/Greedy_number_partitioning

    Credit: Code review by FMc at https://codereview.stackexchange.com/a/273975/20684.
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins


def greedy(
    bins: Bins,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
):
    """
    Partition the given items using the greedy number partitioning algorithm.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> greedy(BinsKeepingContents(2), items=[1,2,3,3,5,9,9]).bins
    [[9, 5, 2], [9, 3, 3, 1]]
    >>> greedy(BinsKeepingContents(3), items=[1,2,3,3,5,9,9]).bins
    [[9, 2], [9, 1], [5, 3, 3]]
    >>> list(greedy(BinsKeepingContents(3), items=[1,2,3,3,5,9,9]).sums)
    [11.0, 10.0, 11.0]

    >>> from prtpy import partition
    >>> partition(algorithm=greedy, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
    >>> partition(algorithm=greedy, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])
    """
    for item in sorted(items, key=map_item_to_value, reverse=True):
        index_of_least_full_bin = min(range(bins.num), key=lambda i: bins.sums[i])
        bins.add_item_to_bin(
            item=item,
            value=map_item_to_value(item),
            bin_index=index_of_least_full_bin,
            inplace=True,
        )
    return bins


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
