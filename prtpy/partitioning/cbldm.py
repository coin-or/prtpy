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
from prtpy import outputtypes as out, objectives as obj, Bins, BinsKeepingContents
import time
import math


def cbldm(
        bins: Bins,
        items: List[float],
        valueof: Callable[[Any], float] = lambda x: x,
        time_in_seconds: float = np.inf,
        partition_difference: int = sys.maxsize
) -> Bins:
    """
    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> cbldm(BinsKeepingContents(2), items=[10], time_in_seconds=1).bins
    [[], [10]]
    >>> cbldm(BinsKeepingContents(2), items=[1/2,1/3,1/5], time_in_seconds=1, partition_difference=1).bins
    [[0.5], [0.2, 0.3333333333333333]]
    >>> cbldm(BinsKeepingContents(2), items=[8,7,6,5,4], time_in_seconds=1, partition_difference=1).bins
    [[8, 7], [4, 6, 5]]
    >>> cbldm(BinsKeepingContents(2), items=[6,6,5,5,5], time_in_seconds=1, partition_difference=1).bins
    [[6, 6], [5, 5, 5]]
    >>> cbldm(BinsKeepingContents(2), items=[4,1,1,1,1], time_in_seconds=1, partition_difference=1).bins
    [[1, 1, 1], [4, 1]]

    >>> from prtpy import partition
    >>> partition(algorithm=cbldm, numbins=2, items=[10], time_in_seconds=1)
    [[], [10]]
    >>> partition(algorithm=cbldm, numbins=2, items=[1/2,1/3,1/5], time_in_seconds=1, partition_difference=1)
    [[0.5], [0.2, 0.3333333333333333]]
    >>> partition(algorithm=cbldm, numbins=2, items=[6,6,5,5,5], time_in_seconds=1, partition_difference=1)
    [[6, 6], [5, 5, 5]]
    >>> partition(algorithm=cbldm, numbins=2, items=[8,7,6,5,4], time_in_seconds=1, partition_difference=1)
    [[8, 7], [4, 6, 5]]
    >>> partition(algorithm=cbldm, numbins=2, items=[4,1,1,1,1], time_in_seconds=1, partition_difference=1)
    [[1, 1, 1], [4, 1]]

    >>> partition(algorithm=cbldm, numbins=3, items=[8,7,6,5,4], time_in_seconds=1, partition_difference=1)
    Traceback (most recent call last):
        ...
    ValueError: number of bins must be 2
    >>> partition(algorithm=cbldm, numbins=2, items=[8,7,6,5,4], time_in_seconds=-1, partition_difference=1)
    Traceback (most recent call last):
        ...
    ValueError: time_in_seconds must be positive
    >>> partition(algorithm=cbldm, numbins=2, items=[8,7,6,5,4], time_in_seconds=1, partition_difference=-1)
    Traceback (most recent call last):
        ...
    ValueError: partition_difference must be a complete number and >= 1
    >>> partition(algorithm=cbldm, numbins=2, items=[8,7,6,5,4], time_in_seconds=1, partition_difference=1.5)
    Traceback (most recent call last):
        ...
    ValueError: partition_difference must be a complete number and >= 1
    >>> partition(algorithm=cbldm, numbins=2, items=[8,7,6,5,-4], time_in_seconds=1, partition_difference=1)
    Traceback (most recent call last):
        ...
    ValueError: items must be positive
    """
    start = time.perf_counter()
    if bins.num != 2:
        raise ValueError("number of bins must be 2")
    if time_in_seconds <= 0:
        raise ValueError("time_in_seconds must be positive")
    if partition_difference < 1 or not isinstance(partition_difference, int):
        raise ValueError("partition_difference must be a complete number and >= 1")
    sorted_items = sorted(items, key=valueof, reverse=True)
    for i in reversed(sorted_items):
        if i > 0:
            break
        else:
            raise ValueError("items must be positive")
    normalised_items = []
    for i in sorted_items:
        b = BinsKeepingContents(2)
        b.add_item_to_bin(item=i, bin_index=1)
        normalised_items.append(b)
    alg = CBLDM_algo(length=len(normalised_items), time_in_seconds=np.inf, difference=partition_difference, start=start)
    alg.part(normalised_items)
    return alg.best


class CBLDM_algo:

    def __init__(self, length, time_in_seconds, difference, start):
        self.delta = np.inf
        self.length = length
        self.time_in_seconds = time_in_seconds
        self.difference = difference
        self.start = start
        self.best = BinsKeepingContents(2)
        self.best.add_item_to_bin(np.inf, 0)
        self.opt = False

    def part(self, items):
        if time.perf_counter() - self.start >= self.time_in_seconds or self.opt:
            return
        if len(items) == 1:
            if abs(len(items[0].bins[0]) - len(items[0].bins[1])) <= self.difference and abs(items[0].sums[0] - items[0].sums[1]) < self.delta:
                self.best = items[0]
                self.delta = abs(items[0].sums[0] - items[0].sums[1])
                if self.delta == 0:
                    self.opt = True
                return
        else:
            sum_xi = 0
            max_x = 0
            for i in items:
                xi = abs(i.sums[0] - i.sums[1])
                sum_xi += xi
                if xi > max_x:
                    max_x = xi
            if 2 * max_x - sum_xi >= self.delta:
                return
            sum_mi = 0
            max_m = 0
            for i in items:
                mi = abs(len(i.bins[0]) - len(i.bins[1]))
                sum_mi += mi
                if mi > max_m:
                    max_m = mi
            if 2 * max_m - sum_mi > self.difference:
                return
            if len(items) <= math.ceil(self.length / 2):
                items = sorted(items, key=lambda item: abs(item.sums[0] - item.sums[1]), reverse=True)
            left = items[2:]
            right = items[2:]
            split = BinsKeepingContents(2)
            combine = BinsKeepingContents(2)
            for section in range(2):
                for bin_i in range(2):
                    for i in items[section].bins[bin_i]:
                        combine.add_item_to_bin(i, bin_i)
            combine.sort()
            for i in items[0].bins[0]:
                split.add_item_to_bin(i, 1)
            for i in items[0].bins[1]:
                split.add_item_to_bin(i, 0)
            for bin_i in range(2):
                for i in items[1].bins[bin_i]:
                    split.add_item_to_bin(i, bin_i)
            split.sort()
            right.append(combine)
            left.append(split)
            self.part(left)
            self.part(right)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
