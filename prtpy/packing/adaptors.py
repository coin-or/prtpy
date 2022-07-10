"""
This module implements Adaptor functions for bin-packin algorithms.

The functions accept a packing algorithm as an argument.

They allow you to call the packing algorithm with convenient input types,
such as: a list of values, or a dict that maps an item to its value.

Author: Erel Segal-Halevi
Since: 2022-07
"""
import numpy as np

from prtpy import outputtypes as out, Bins
from typing import Callable, List, Any
from prtpy.packing.first_fit import decreasing as ffd



def pack(
    algorithm: Callable,
    binsize: float,
    items: Any,
    valueof: Callable[[Any], float] = None,
    outputtype: out.OutputType = out.Partition,
    **kwargs
) -> List[List[int]]:
    """
    An adaptor partition function.

    :param algorithm: a specific bin-packing algorithm. Should accept the following parameters: 
        binsize (float), 
        items (list), 
        valueof (callable), 
        outputtype (OutputType).

    :param items: can be one of the following:
       * A list of item-values (so that each item is equal to its value);
       * A list of item-names  (in this case, valueof should also be defined);
       * A dict (where the keys are the items and the values are their values).

    :param valueof: optional; required only if `items` is a list of item-names.

    :param outputtype: defines the output format. See `outputtypes.py'.

    :return: a partition, or a list of sums - depending on outputtype.

    >>> import prtpy
    >>> from prtpy.packing.first_fit import decreasing as ffd
    >>> import numpy as np
    >>> pack(algorithm=ffd, binsize=60, items=[44, 24, 24, 22, 21, 17, 8, 8, 6, 6])
    [[44, 8, 8], [24, 24, 6, 6], [22, 21, 17]]
    >>> pack(algorithm=ffd, binsize=60, items={"a":44, "b":24, "c":24, "d":22, "e":21, "f":17, "g":8, "h":8, "i":6, "j":6})
    [['a', 'g', 'h'], ['b', 'c', 'i', 'j'], ['d', 'e', 'f']]
    >>> pack(algorithm=ffd, binsize=60, items=np.array([44, 24, 24, 22, 21, 17, 8, 8, 6, 6]), outputtype=out.Sums)
    [60.0, 60.0, 60.0]
    >>> pack(algorithm=ffd, binsize=60, items=[44, 24, 24, 22, 21, 17, 8, 8, 6, 6], outputtype=out.BinCount)
    3
    >>> pack(algorithm=ffd, binsize=61, items=[44, 24, 24, 22, 21, 17, 8, 8, 6, 6], outputtype=out.BinCount)
    4
    """
    if isinstance(items, dict):  # items is a dict mapping an item to its value.
        item_names = items.keys()
        if valueof is None:
            valueof = items.__getitem__
    else:  # items is a list
        item_names = items
        if valueof is None:
            valueof = lambda item: item
    bins = outputtype.create_empty_bins(0, valueof)
    bins = algorithm(bins, binsize, item_names, valueof, **kwargs)
    if isinstance(bins, Bins):
        return outputtype.extract_output_from_bins(bins)
    else:
        return outputtype.extract_output_from_binsarray(bins)

def pack_random_items(numitems: int, bitsperitem: int, **kwargs):
    """
    Generates a uniformly-random list of items and packs them using the given algorithm.

    :param numitems: how many items to generate.
    :param bitsperitem: how many bits in each item.
    :param kwargs: keyword arguments delegated to `pack`.
    """
    items = np.random.randint(1, 2**bitsperitem-1, numitems, dtype=np.int64)
    return pack(items=items, **kwargs)


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

    print(pack_random_items(10, 16, algorithm=ffd, binsize=2**17, outputtype=out.PartitionAndSums))
