"""
Implementations of some bin covering algorithms from:

Csirik, Frenk, Labbe, Zhang. "Two simple algorithms for bin covering". 
Acta Cybernetica, 1999.

AUTHOR: Erel Segal-Halevi
SINCE: 2021-04
"""

from prtpy import outputtypes as out
from typing import Callable, List, Any
from prtpy.packing.greedy_covering import decreasing_subroutine



def twothirds(
    binsize: float,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    outputtype: out.OutputType = out.Partition,
):
    """
    Run the 2/3-approximation algorithm for bin covering.
    From Csirik et al (1999).

    >>> twothirds(10, [11,12,13])   # large items
    [[13], [12], [11]]
    >>> twothirds(10, [3,3,3,3, 3,3,3,3, 3,3,3])   # identical items
    [[3, 3, 3, 3], [3, 3, 3, 3]]
    >>> twothirds(10, [1,2,3,4,5,6,7,8,9,10])   # different items
    [[10], [9, 1], [8, 2], [7, 3], [6, 4]]
    >>> twothirds(1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1])   # worst-case example (k=1)
    [[994, 1, 1, 1, 1, 1, 1], [499, 499, 499], [499, 499, 499]]
    >>> twothirds(1000, [988] + 12*[499] + 12*[1])   # worst-case example (k=2)
    [[988, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [499, 499, 499], [499, 499, 499], [499, 499, 499], [499, 499, 499]]
    >>> twothirds(1200, [594,594] + 12*[399] + 12*[1])   # worst-case example for 3/4 (k=1)
    [[594, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 399, 399], [594, 399, 399], [399, 399, 399, 399], [399, 399, 399, 399]]
    """
    bins = outputtype.create_empty_bins(1)
    items = sorted(items, key=map_item_to_value, reverse=True)
    while len(items)>0:
        # Initialize with a single biggest item:
        biggest_item = items[0]
        bins.add_item_to_bin(biggest_item, map_item_to_value(biggest_item), -1)
        del items[0]

        while len(items)>0 and bins.sums[-1]<binsize:
            # Fill with the smallest items in ascending order:
            smallest_item = items[-1]
            bins.add_item_to_bin(smallest_item, map_item_to_value(smallest_item), -1)
            del items[-1]

        if bins.sums[-1]>=binsize:  # The current bin is full - add it and continue
            bins.add_empty_bins(1)
    bins.remove_bins(1) # remove the last, not-full bin.
    return outputtype.extract_output_from_bins(bins)



def threequarters(
    binsize: float,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    outputtype: out.OutputType = out.Partition,
):
    """
    Run the 3/4-approximation algorithm for bin covering.
    From Csirik et al (1999).

    >>> threequarters(10, [11,12,13])   # large items
    [[13], [12], [11]]
    >>> threequarters(10, [3,3,3,3, 3,3,3,3, 3,3,3])   # identical items
    [[3, 3, 3, 3], [3, 3, 3, 3]]
    >>> threequarters(10, [1,2,3,4,5,6,7,8,9,10])   # different items
    [[10], [9, 1], [8, 2], [7, 3], [6, 5]]
    >>> threequarters(1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1])   # worst-case example for 2/3 (k=1)
    [[499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1]]
    >>> threequarters(1000, [988] + 12*[499] + 12*[1])   # worst-case example for 2/3 (k=2)
    [[499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1]]
    >>> threequarters(1200, [594,594] + 12*[399] + 12*[1])   # worst-case example for 3/4 (k=1)
    [[594, 594, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [399, 399, 399, 399], [399, 399, 399, 399], [399, 399, 399, 399]]
    >>> threequarters(1000, [994, 501,501, 499,499,499,499]+12*[1])
    [[499, 499, 1, 1], [499, 499, 1, 1], [994, 1, 1, 1, 1, 1, 1], [501, 1, 1, 501]]
    """
    bins = outputtype.create_empty_bins(1)
    items = sorted(items, key=map_item_to_value, reverse=True)

    big_items = [item for item in items if binsize/2 <= item]  # X
    medium_items = [item for item in items if binsize/3 <= item < binsize/2]  # Y
    small_items = [item for item in items if item < binsize/3]  # Z

    while True:
        if len(small_items)==0:
            # NOTE: We re-use the items remaining in the last bin.
            decreasing_subroutine(bins, binsize, big_items, map_item_to_value)
            decreasing_subroutine(bins, binsize, medium_items, map_item_to_value)
            break

        elif len(big_items)==0 and len(medium_items)==0:
            decreasing_subroutine(bins, binsize, small_items, map_item_to_value)
            break

        else:
            # Here, there are both small items, and big/medium items.
            # Initialize a bin with either a single biggest item, or two biggest medium items:
            biggest_item = big_items[0:1]              # It will be empty if X is empty
            biggest_medium_items = medium_items[0:2]   # It will be empty if Y is empty
            if sum(biggest_item) >= sum(biggest_medium_items):
                for item in biggest_item:
                    bins.add_item_to_bin(item, map_item_to_value(item), -1)
                    del big_items[0]
            else:
                for item in biggest_medium_items:
                    bins.add_item_to_bin(item, map_item_to_value(item), -1)
                    del medium_items[0]

            while len(small_items)>0 and bins.sums[-1]<binsize:
                # Fill with the smallest items in ascending order:
                smallest_item = small_items[-1]
                bins.add_item_to_bin(smallest_item, map_item_to_value(smallest_item), -1)
                del small_items[-1]

            if bins.sums[-1]>=binsize:  # The current bin is full - add it and continue
                bins.add_empty_bins(1)

    bins.remove_bins(1)  # the last bin is not full - remove it
    return outputtype.extract_output_from_bins(bins)



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

