"""
An implementation anytime balanced number partition form:
A complete anytime algorithm for balanced number partitioning
by Stephan Mertens 1999
https://arxiv.org/abs/cs/9903011

The algorithm gets a list of numbers and returns a partition with
the smallest sum difference between 2 groups the list is divided to.
The algorithm runs until it finds the optimal partition, or it runs out of time.
"""
import sys
from typing import Callable, List, Any
import numpy as np
from prtpy import outputtypes as out, objectives as obj, Bins


def CBLDM(
    bins: Bins,
    items: List[float],
    valueof: Callable[[Any], float] = lambda x: x,
    time_in_seconds: float = np.inf,
    partition_difference: int = sys.maxint
) -> Bins:

    """
    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> CBLDM(BinsKeepingContents(2), items=[10], time_in_seconds=1).bins
    [[], [10]]
    >>> CBLDM(BinsKeepingContents(2), items=[1/2,1/3,1/5], time_in_seconds=1, partition_difference=1).bins
    [[0.5], [0.2,0.3333333333333333]]
    >>> CBLDM(BinsKeepingContents(2), items=[8,7,6,5,4], time_in_seconds=1, partition_difference=1).bins
    [[4,5,6], [7,8]]
    >>> CBLDM(BinsKeepingContents(2), items=[6,6,5,5,5], time_in_seconds=1, partition_difference=1).bins
    [[6,6], [5,5,5]]
    >>> CBLDM(BinsKeepingContents(2), items=[4,1,1,1,1], time_in_seconds=1, partition_difference=1).bins
    [[1,1,1], [1,4]]

    >>> from prtpy import partition
    >>> partition(algorithm=CBLDM, numbins=2, items=[10], time_in_seconds=1)
    [[], [10]]
    >>> partition(algorithm=CBLDM, numbins=2, items=[1/2,1/3,1/5], time_in_seconds=1, partition_difference=1)
    [[0.5], [0.2,0.3333333333333333]]
    >>> partition(algorithm=CBLDM, numbins=2, items=[6,6,5,5,5], time_in_seconds=1, partition_difference=1)
    [[6,6], [5,5,5]]
    >>> partition(algorithm=CBLDM, numbins=2, items=[8,7,6,5,4], time_in_seconds=1, partition_difference=1)
    [[4,5,6], [7,8]]
    >>> partition(algorithm=CBLDM, numbins=2, items=[4,1,1,1,1], time_in_seconds=1, partition_difference=1)
    [[1,1,1], [1,4]]

    >>> partition(algorithm=CBLDM, numbins=3, items=[8,7,6,5,4], time_in_seconds=1, partition_difference=1)
    Traceback (most recent call last):
        ...
    ValueError numbins must be 2
    >>> partition(algorithm=CBLDM, numbins=2, items=[8,7,6,5,4], time_in_seconds=-1, partition_difference=1)
    Traceback (most recent call last):
        ...
    ValueError: time_in_seconds must be positive
    >>> partition(algorithm=CBLDM, numbins=2, items=[8,7,6,5,4], time_in_seconds=1, partition_difference=-1)
    Traceback (most recent call last):
        ...
    ValueError: partition_difference must be a complete number and >= 1
    >>> partition(algorithm=CBLDM, numbins=2, items=[8,7,6,5,4], time_in_seconds=1, partition_difference=1.5)
    Traceback (most recent call last):
        ...
    ValueError: partition_difference must be a complete number and >= 1
    >>> partition(algorithm=CBLDM, numbins=2, items=[8,7,6,5,-4], time_in_seconds=1, partition_difference=1)
    Traceback (most recent call last):
        ...
    ValueError: items must be positive
    """
    
    pass


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))