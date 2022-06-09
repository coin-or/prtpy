"""
A simple greedy bin-covering algorithm

AUTHOR: Erel Segal-Halevi
SINCE: 2021-04
"""

from prtpy import outputtypes as out, Bins
from typing import Callable, List, Any







def decreasing(
    bins: Bins,
    binsize: float,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
):
    """
    Run a simple bin-covering algorithm:
    it orders the items in descending order, and puts them into a bin until it is filled.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> decreasing(BinsKeepingContents(), 10, [11,12,13]).bins  # large items
    [[13], [12], [11]]
    >>> decreasing(BinsKeepingContents(), 10, [3,3,3,3, 3,3,3,3, 3,3,3]).bins   # identical items
    [[3, 3, 3, 3], [3, 3, 3, 3]]
    >>> decreasing(BinsKeepingContents(), 10, [1,2,3,4,5,6,7,8,9,10]).bins   # different items
    [[10], [9, 8], [7, 6], [5, 4, 3]]
    >>> decreasing(BinsKeepingContents(), 1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1]).bins   # worst-case example (k=1)
    [[994, 499], [499, 499, 499], [499, 499, 1, 1]]
    >>> decreasing(BinsKeepingContents(), 1000, [988] + 12*[499] + 12*[1]).bins   # worst-case example (k=2)
    [[988, 499], [499, 499, 499], [499, 499, 499], [499, 499, 499], [499, 499, 1, 1]]

    >>> from prtpy import pack
    >>> pack(algorithm=decreasing, binsize=60, items={"a":44, "b":24, "c":24, "d":22, "e":21, "f":17, "g":8, "h":8, "i":6, "j":6})
    [['a', 'b'], ['c', 'd', 'e']]
    >>> pack(algorithm=decreasing, binsize=60, items={"a":44, "b":24, "c":24, "d":22, "e":21, "f":17, "g":8, "h":8, "i":6, "j":6}, outputtype=out.Sums)
    array([68., 67.])
    """
    bins.add_empty_bins(1)
    items = sorted(items, key=valueof, reverse=True)
    decreasing_subroutine(bins, binsize, sorted_items=items, valueof=valueof)
    bins.remove_bins(1)  # the last bin is not full - remove it
    return bins


def decreasing_subroutine(
    bins: Bins, 
    binsize: float,
    sorted_items: List[any],
    valueof: Callable[[Any], float]
):
    """
    Run a simple bin-covering algorithm:
    it orders the items in descending order, and puts them into a bin until it is filled.
    This is a subroutine that accepts an already-initialized Bins structure, and already-sorted items list.
    """
    for item in sorted_items:
        bins.add_item_to_bin(item, -1)
        if bins.sums[-1] >= binsize: # the last bin is full - open a new one
            bins.add_empty_bins(1)


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

