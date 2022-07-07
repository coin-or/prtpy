"""
Checks whether the given partition problem is trivial_partition and can be solved easily.
It is used for the base case of number partitioning algorithms.

"Trivial" means one of the following:
* Zero bins;
* One bin;
* Number of bins equals number of items.

Author: Kfir Goldfarb
Date: 08/06/2022
Email: kfir.goldfarb@msmail.ariel.ac.il
"""


import itertools
from copy import deepcopy
from typing import List, Callable, Tuple
import random
import numpy as np

from prtpy import Bins, BinsKeepingContents


def trivial_partition(bins: Bins, items: List[any]) -> bool:
    """
    This function is used for the base case of number partitioning algorithms.
    It gets a list of items and an array of bins.
    If the problem is trivial_partition (that is: zero bins, one bin, or number of bins equals number of items),
       it solves it, updates the "bins" structure, and returns True.
    Otherwise, it returns False.

    >>> bins0 = BinsKeepingContents(0)
    >>> trivial_partition(bins0, items=[1, 2, 3, 4, 5, 6])
    True
    >>> bins0.bins
    []

    >>> trivial_partition(bins0, items=[random.randint(0, 100) for i in range(random.randint(100, 1000))])
    True
    >>> bins0.bins
    []

    >>> trivial_partition(bins0, items=[random.randint(0, 100) for i in range(random.randint(100, 1000))])
    True
    >>> bins0.bins
    []

    >>> bins1 = BinsKeepingContents(1)
    >>> trivial_partition(bins1, items=[1, 2, 3, 4, 5, 6])
    True
    >>> bins1.bins
    [[1, 2, 3, 4, 5, 6]]

    >>> bins1 = BinsKeepingContents(1)
    >>> trivial_partition(bins1, items=[3, 6, 13, 20, 30, 40, 73])
    True
    >>> bins1.bins
    [[3, 6, 13, 20, 30, 40, 73]]

    >>> bins1 = BinsKeepingContents(1)
    >>> trivial_partition(bins1, items=[1, 2, 3, 4, 5, 6])
    True
    >>> bins1 = BinsKeepingContents(1)
    >>> trivial_partition(bins1, items=[random.randint(0, 100) for i in range(random.randint(100, 1000))])
    True
    >>> bins1 = BinsKeepingContents(1)
    >>> trivial_partition(bins1, items=[1])
    True
    >>> bins1.bins
    [[1]]

    >>> bins5 = BinsKeepingContents(5)
    >>> trivial_partition(bins=bins5, items=[1, 2, 3, 4, 5])
    True
    >>> bins5.bins
    [[1], [2], [3], [4], [5]]
    >>> trivial_partition(bins=bins5, items=[1, 2, 3, 4, 5, 6])
    False
    """
    if bins.num == 0:
        return True

    if bins.num == 1:
        for item in items:
            bins.add_item_to_bin(item, bin_index=0)
        return True

    if len(items) == bins.num:
        for index, item in enumerate(items):
            bins.add_item_to_bin(item, bin_index=index)
        return True

    return False


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
