"""
    Pack the numbers using the first-fit bin-packing algorithms:
       https://en.wikipedia.org/wiki/First-fit_bin_packing
       https://en.wikipedia.org/wiki/First-fit-decreasing_bin_packing
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out


def online(
    binsize: float,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    outputtype: out.OutputType = out.Partition,
):
    """
    Pack the given items into bins using the online first-fit algorithm.
    The online algorithm handles the items in the order they are given.

    >>> online(binsize=9, items=[1,2,3,3,5,9,9], outputtype=out.Partition)
    [[1, 2, 3, 3], [5], [9], [9]]
    >>> online(binsize=18, items=[1,2,3,3,5,9,9], outputtype=out.Partition)
    [[1, 2, 3, 3, 5], [9, 9]]
    >>> list(online(binsize=9, items=[1,2,3,3,5,9,9], outputtype=out.Sums))
    [9.0, 5.0, 9.0, 9.0]
    >>> online(binsize=18, items=[1,2,3,3,5,9,9], outputtype=out.LargestSum)
    18.0
    """
    bins = outputtype.create_empty_bins(1)
    for item in items:
        value = map_item_to_value(item)
        if value>binsize:
            raise ValueError(f"Item {item} has size {value} which is larger than the bin size {binsize}.")
        ibin = 0
        while ibin  < bins.num:
            if bins.sums[ibin] + value <= binsize:
                bins.add_item_to_bin(item, value, ibin)
                break
            ibin += 1
        else:  # if not added to any bin
            bins.add_empty_bins(1)
            bins.add_item_to_bin(item, value, ibin)
    return outputtype.extract_output_from_bins(bins)


def decreasing(
    binsize: float,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    outputtype: out.OutputType = out.Partition,
):
    """
    Pack the given items into bins using the first-fit-decreasing algorithm.
    It sorts the items by descending value, and then runs first-fit.

    >>> decreasing(binsize=9, items=[1,2,3,3,5,9,9], outputtype=out.Partition)
    [[9], [9], [5, 3, 1], [3, 2]]
    >>> decreasing(binsize=18, items=[1,2,3,3,5,9,9], outputtype=out.Partition)
    [[9, 9], [5, 3, 3, 2, 1]]
    >>> list(decreasing(binsize=9, items=[1,2,3,3,5,9,9], outputtype=out.Sums))
    [9.0, 9.0, 9.0, 5.0]
    >>> decreasing(binsize=18, items=[1,2,3,3,5,9,9], outputtype=out.LargestSum)
    18.0

    Non-monotonicity examples from Wikipedia:
    >>> example1 = [44, 24, 24, 22, 21, 17, 8, 8, 6, 6]
    >>> decreasing(binsize=60, items=example1) # 3 bins
    [[44, 8, 8], [24, 24, 6, 6], [22, 21, 17]]
    >>> decreasing(binsize=61, items=example1) # 4 bins
    [[44, 17], [24, 24, 8], [22, 21, 8, 6], [6]]
    >>> example2 = [51, 27.5, 27.5, 27.5, 27.5, 25, 12, 12, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    >>> decreasing(binsize=75, items=example2) # 4 bins
    [[51, 12, 12], [27.5, 27.5, 10, 10], [27.5, 27.5, 10, 10], [25, 10, 10, 10, 10, 10]]
    >>> decreasing(binsize=76, items=example2) # 5 bins
    [[51, 25], [27.5, 27.5, 12], [27.5, 27.5, 12], [10, 10, 10, 10, 10, 10, 10], [10, 10]]
    """
    return online(
        binsize, 
        sorted(items, key=map_item_to_value, reverse=True),
        map_item_to_value,
        outputtype
    )


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
