"""
    Pack the numbers using the first-fit bin-packing algorithms:
       https://en.wikipedia.org/wiki/First-fit_bin_packing
       https://en.wikipedia.org/wiki/First-fit-decreasing_bin_packing
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, Bins


def online(
    bins: Bins,
    binsize: float,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
):
    """
    Pack the given items into bins using the online first-fit algorithm.
    The online algorithm handles the items in the order they are given.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> online(BinsKeepingContents(), binsize=9, items=[1,2,3,3,5,9,9]).bins
    [[1, 2, 3, 3], [5], [9], [9]]
    >>> online(BinsKeepingContents(), binsize=18, items=[1,2,3,3,5,9,9]).bins
    [[1, 2, 3, 3, 5], [9, 9]]
    >>> list(online(BinsKeepingContents(), binsize=9, items=[1,2,3,3,5,9,9]).sums)
    [9.0, 5.0, 9.0, 9.0]
    """
    bins.add_empty_bins(1) 
    for item in items:
        value = valueof(item)
        if value>binsize:
            raise ValueError(f"Item {item} has size {value} which is larger than the bin size {binsize}.")
        ibin = 0
        while ibin  < bins.num:
            if bins.sums[ibin] + value <= binsize:
                bins.add_item_to_bin(item, ibin)
                break
            ibin += 1
        else:  # if not added to any bin
            bins.add_empty_bins(1)
            bins.add_item_to_bin(item, ibin)
    return bins


def decreasing(
    bins: Bins,
    binsize: float,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
):
    """
    Pack the given items into bins using the first-fit-decreasing algorithm.
    It sorts the items by descending value, and then runs first-fit.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> decreasing(BinsKeepingContents(), binsize=9, items=[1,2,3,3,5,9,9]).bins
    [[9], [9], [5, 3, 1], [3, 2]]
    >>> decreasing(BinsKeepingContents(), binsize=18, items=[1,2,3,3,5,9,9]).bins
    [[9, 9], [5, 3, 3, 2, 1]]
    >>> list(decreasing(BinsKeepingContents(), binsize=9, items=[1,2,3,3,5,9,9]).sums)
    [9.0, 9.0, 9.0, 5.0]

    Non-monotonicity examples from Wikipedia:
    >>> example1 = [44, 24, 24, 22, 21, 17, 8, 8, 6, 6]
    >>> decreasing(BinsKeepingContents(), binsize=60, items=example1).bins # 3 bins
    [[44, 8, 8], [24, 24, 6, 6], [22, 21, 17]]
    >>> decreasing(BinsKeepingContents(), binsize=61, items=example1).bins # 4 bins
    [[44, 17], [24, 24, 8], [22, 21, 8, 6], [6]]
    >>> example2 = [51, 27.5, 27.5, 27.5, 27.5, 25, 12, 12, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    >>> decreasing(BinsKeepingContents(), binsize=75, items=example2).bins # 4 bins
    [[51, 12, 12], [27.5, 27.5, 10, 10], [27.5, 27.5, 10, 10], [25, 10, 10, 10, 10, 10]]
    >>> decreasing(BinsKeepingContents(), binsize=76, items=example2).bins # 5 bins
    [[51, 25], [27.5, 27.5, 12], [27.5, 27.5, 12], [10, 10, 10, 10, 10, 10, 10], [10, 10]]

    >>> from prtpy import pack
    >>> pack(algorithm=decreasing, binsize=60, items={"a":44, "b":24, "c":24, "d":22, "e":21, "f":17, "g":8, "h":8, "i":6, "j":6})
    [['a', 'g', 'h'], ['b', 'c', 'i', 'j'], ['d', 'e', 'f']]
    >>> pack(algorithm=decreasing, binsize=60, items={"a":44, "b":24, "c":24, "d":22, "e":21, "f":17, "g":8, "h":8, "i":6, "j":6}, outputtype=out.Sums)
    array([60., 60., 60.])
    """
    return online(
        bins,
        binsize, 
        sorted(items, key=valueof, reverse=True),
        valueof,
    )


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
