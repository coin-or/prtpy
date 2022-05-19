"""
    Pack the numbers using the best-fit bin-packing algorithms:
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, Bins


def online(
    bins: Bins,
    binsize: float,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
):
    bins.add_empty_bins()
    for item in items:
        value = valueof(item)
        if value > binsize:
            raise ValueError(f"Item {item} has size {value} which is larger than the bin size {binsize}.")
        ibin = 0
        best_bin = (-1, -1)
        while ibin < bins.num:
            new_sum = bins.sums[ibin] + value
            if new_sum <= binsize and new_sum > best_bin[1]:
                best_bin = (ibin, new_sum)
            ibin += 1

        if best_bin[0] > -1:
            bins.add_item_to_bin(item, best_bin[0])
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

    return online(
        bins,
        binsize,
        sorted(items, key=valueof, reverse=True),
        valueof,
    )

#
# if __name__ == "__main__":
#     import doctest
#
#     (failures, tests) = doctest.testmod(report=True)
#     print("{} failures, {} tests".format(failures, tests))
