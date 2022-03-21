"""
This module implements an adaptor function for bin-packing algorithms.

The specific packing algorithms accept as input a list of items, 
and a function that maps each item to its value.

This module lets you call a packing algorithm with more convenient input types,
such as: a list of values, and a dict that maps an item to its value.
"""

from prtpy import outputtypes as out
from typing import Callable, List, Any



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
    array([60., 60., 60.])
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
    bins = outputtype.create_empty_bins(0)
    bins.set_valueof(valueof)
    bins = algorithm(bins, binsize, item_names, valueof, **kwargs)
    return outputtype.extract_output_from_bins(bins)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
