"""
A simple greedy bin-covering algorithm

AUTHOR: Erel Segal-Halevi
SINCE: 2021-04
"""

from prtpy import outputtypes as out, Bins
from typing import Callable, List, Any







def decreasing(
    binsize: float,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    outputtype: out.OutputType = out.Partition,
):
    """
    Run a simple bin-covering algorithm:
    it orders the items in descending order, and puts them into a bin until it is filled.

    >>> decreasing(10, [11,12,13])   # large items
    [[13], [12], [11]]
    >>> decreasing(10, [3,3,3,3, 3,3,3,3, 3,3,3])   # identical items
    [[3, 3, 3, 3], [3, 3, 3, 3]]
    >>> decreasing(10, [1,2,3,4,5,6,7,8,9,10])   # different items
    [[10], [9, 8], [7, 6], [5, 4, 3]]
    >>> decreasing(1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1])   # worst-case example (k=1)
    [[994, 499], [499, 499, 499], [499, 499, 1, 1]]
    >>> decreasing(1000, [988] + 12*[499] + 12*[1])   # worst-case example (k=2)
    [[988, 499], [499, 499, 499], [499, 499, 499], [499, 499, 499], [499, 499, 1, 1]]
    """
    bins = outputtype.create_empty_bins(1)
    items = sorted(items, key=map_item_to_value, reverse=True)
    decreasing_subroutine(bins, binsize, sorted_items=items, map_item_to_value=map_item_to_value)
    bins.remove_bins(1)  # the last bin is not full - remove it
    return outputtype.extract_output_from_bins(bins)


def decreasing_subroutine(
    bins: Bins, 
    binsize: float,
    sorted_items: List[any],
    map_item_to_value: Callable[[Any], float]
):
    """
    Run a simple bin-covering algorithm:
    it orders the items in descending order, and puts them into a bin until it is filled.
    This is a subroutine that accepts an already-initialized Bins structure, and already-sorted items list.
    """
    for item in sorted_items:
        value = map_item_to_value(item)
        bins.add_item_to_bin(item, value, -1)
        if bins.sums[-1] >= binsize: # the last bin is full - open a new one
            bins.add_empty_bins(1)


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

