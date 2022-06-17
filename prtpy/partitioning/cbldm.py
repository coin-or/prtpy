"""
An implementation anytime balanced number partition form:
A complete anytime algorithm for balanced number partitioning
by Stephan Mertens 1999
https://arxiv.org/abs/cs/9903011

The algorithm gets a list of numbers and returns a partition with
the smallest sum difference between 2 groups the list is divided to.
The algorithm runs until it finds the optimal partition, or it runs out of time.

implemented by Eli Belkind 3.6.22
"""
import sys
from typing import Callable, List, Any
import numpy as np
from prtpy import Bins, BinsKeepingContents
import time
import math


def cbldm(                  # max items length can be between 900 and 1000 due to stack limitations
        bins: Bins,         # max length of items can vary from computer to computer
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
    [[4, 6, 5], [8, 7]]
    >>> cbldm(BinsKeepingContents(2), items=[6,6,5,5,5], time_in_seconds=1, partition_difference=1).bins
    [[6, 6], [5, 5, 5]]
    >>> cbldm(BinsKeepingContents(2), items=[4,1,1,1,1], time_in_seconds=1, partition_difference=1).bins
    [[1, 1, 1], [4, 1]]

    >>> from prtpy import partition, out
    >>> partition(algorithm=cbldm, numbins=2, items=[10], time_in_seconds=1)
    [[], [10]]
    >>> partition(algorithm=cbldm, numbins=2, items=[10,0], time_in_seconds=1, partition_difference=3)
    [[0], [10]]
    >>> partition(algorithm=cbldm, numbins=2, items=[1/2,1/3,1/5], time_in_seconds=1, partition_difference=1)
    [[0.5], [0.2, 0.3333333333333333]]
    >>> partition(algorithm=cbldm, numbins=2, items=[6,6,5,5,5], time_in_seconds=1, partition_difference=1)
    [[6, 6], [5, 5, 5]]
    >>> partition(algorithm=cbldm, numbins=2, items=[8,7,6,5,4], time_in_seconds=1, partition_difference=1)
    [[4, 6, 5], [8, 7]]
    >>> partition(algorithm=cbldm, numbins=2, items=[4,1,1,1,1], time_in_seconds=1, partition_difference=1)
    [[1, 1, 1], [4, 1]]

    >>> partition(algorithm=cbldm, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['g', 'd', 'c', 'a'], ['f', 'b', 'e']]

    >>> rng = np.random.default_rng(1)
    >>> items = rng.integers(1, 1000, 100)
    >>> partition(algorithm=cbldm, numbins=2, items=items, outputtype=out.Sums)
    [25390.0, 25390.0]

    >>> items = rng.integers(1, 1000, 899)
    >>> partition(algorithm=cbldm, numbins=2, items=items, outputtype=out.Sums, time_in_seconds=1)
    [225368.0, 225369.0]
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
        if valueof(i) >= 0:
            break
        else:
            raise ValueError("items must be none negative")

    length = len(items)
    if length == 0:  # empty items returns empty partition
        return bins

    normalised_items = []  # list of bins, each bin contain a sub partition
    for i in sorted_items:
        b = BinsKeepingContents(2)
        b.set_valueof(valueof)
        b.add_item_to_bin(item=i, bin_index=1)
        normalised_items.append(b)
    alg = CBLDM_algo(length=length, time_in_seconds=time_in_seconds, len_delta=partition_difference, start=start, val=valueof)
    alg.part(normalised_items)
    return alg.best


class CBLDM_algo:

    def __init__(self, length, time_in_seconds, len_delta, start, val):
        self.sum_delta = np.inf  # partition sum difference
        self.length = length
        self.time_in_seconds = time_in_seconds
        self.len_delta = len_delta  # partition cardinal difference
        self.start = start
        self.best = BinsKeepingContents(2)
        self.best.add_item_to_bin(np.inf, 1)
        self.opt = False
        self.val = val

    def part(self, items):
        if time.perf_counter() - self.start >= self.time_in_seconds or self.opt:
            return
        if len(items) == 1:  # possible partition
            if abs(len(items[0].bins[0]) - len(items[0].bins[1])) <= self.len_delta and abs(
                    items[0].sums[0] - items[0].sums[1]) < self.sum_delta:
                self.best = items[0]
                self.sum_delta = abs(items[0].sums[0] - items[0].sums[1])
                if self.sum_delta == 0:
                    self.opt = True
                return
        else:
            sum_xi = 0  # calculate the sum of the sum differences in items
            max_x = 0  # max sum difference
            sum_mi = 0  # calculate the sum of the cardinal differences in items
            max_m = 0  # max cardinal difference
            for i in items:
                xi = abs(i.sums[0] - i.sums[1])
                sum_xi += xi
                mi = abs(len(i.bins[0]) - len(i.bins[1]))
                sum_mi += mi
                if mi > max_m:
                    max_m = mi
                if xi > max_x:
                    max_x = xi
            if 2 * max_x - sum_xi >= self.sum_delta:
                return
            # despite being in the paper, or condition breaks algorithm. for example breaks on [1,1,1,1,1,1,1,1,1,1]
            if 2 * max_m - sum_mi > self.len_delta:  # or sum_mi < self.difference:
                return
            if len(items) <= math.ceil(self.length / 2):
                items = sorted(items, key=lambda item: abs(item.sums[0] - item.sums[1]), reverse=True)
            # split items to left branch and right branch according to partition type
            left = items[2:]
            right = items[2:]
            split = BinsKeepingContents(2)  # split partition according to sum of bins
            combine = BinsKeepingContents(2)  # merge partition according to sum of bins
            split.set_valueof(self.val)
            combine.set_valueof(self.val)

            for section in range(2):  # [small, big] + [small, big] -> [small + small, big + big]
                for bin_i in range(2):
                    for i in items[section].bins[bin_i]:
                        combine.add_item_to_bin(i, bin_i)
            combine.sort()

            for i in items[0].bins[0]:  # [small, big] + [small, big] -> [small + big, small + big]
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
