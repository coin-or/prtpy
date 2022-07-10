"""
An implementation of the anytime balanced number partition from:
    "A complete anytime algorithm for balanced number partitioning"
    by Stephan Mertens 1999
    https://arxiv.org/abs/cs/9903011

The algorithm gets a list of numbers and returns a partition into two bins, 
with the smallest sum-difference between the bins.
The algorithm runs until it finds the optimal partition, or it runs out of time.

Programmer: Eli Belkind 
Date: 2022-06-03
"""

import sys
from typing import Callable, List, Any
import numpy as np
from prtpy import Bins, BinsKeepingContents, Binner
import time
import math


def cbldm(
        bins: Bins,
        items: List[float],
        valueof: Callable[[Any], float] = lambda x: x,
        time_limit: float = np.inf,
        partition_difference: int = sys.maxsize
) -> Bins:
    """
    Balanced number partitioning into two bins.
    :param items - the items to partition. The length must be at most 900--1000 due to stack limitations; the exact maximum can vary between computers.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> cbldm(BinsKeepingContents(2), items=[10], time_limit=1).bins
    [[], [10]]
    >>> cbldm(BinsKeepingContents(2), items=[1/2,1/3,1/5], time_limit=1, partition_difference=1).bins
    [[0.5], [0.2, 0.3333333333333333]]
    >>> cbldm(BinsKeepingContents(2), items=[8,7,6,5,4], time_limit=1, partition_difference=1).bins
    [[4, 6, 5], [8, 7]]
    >>> cbldm(BinsKeepingContents(2), items=[6,6,5,5,5], time_limit=1, partition_difference=1).bins
    [[6, 6], [5, 5, 5]]
    >>> cbldm(BinsKeepingContents(2), items=[4,1,1,1,1], time_limit=1, partition_difference=1).bins
    [[1, 1, 1], [4, 1]]

    >>> from prtpy import partition, out
    >>> partition(algorithm=cbldm, numbins=2, items=[10], time_limit=1)
    [[], [10]]
    >>> partition(algorithm=cbldm, numbins=2, items=[10,0], time_limit=1, partition_difference=3)
    [[0], [10]]
    >>> partition(algorithm=cbldm, numbins=2, items=[1/2,1/3,1/5], time_limit=1, partition_difference=1)
    [[0.5], [0.2, 0.3333333333333333]]
    >>> partition(algorithm=cbldm, numbins=2, items=[6,6,5,5,5], time_limit=1, partition_difference=1)
    [[6, 6], [5, 5, 5]]
    >>> partition(algorithm=cbldm, numbins=2, items=[8,7,6,5,4], time_limit=1, partition_difference=1)
    [[4, 6, 5], [8, 7]]
    >>> partition(algorithm=cbldm, numbins=2, items=[4,1,1,1,1], time_limit=1, partition_difference=1)
    [[1, 1, 1], [4, 1]]

    >>> partition(algorithm=cbldm, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['g', 'd', 'c', 'a'], ['f', 'b', 'e']]
    """
    binner = bins.get_binner()

    start = time.perf_counter()
    if binner.numbins != 2:
        raise ValueError("numbins must be 2")
    if time_limit <= 0:
        raise ValueError("time_limit must be positive")
    if partition_difference < 1 or not isinstance(partition_difference, int):
        raise ValueError("partition_difference must be a complete number and >= 1")

    sorted_items = sorted(items, key=valueof, reverse=True) # Sort by descending value
    if valueof(sorted_items[-1])<0:
        raise ValueError("All items must be non-negative")

    numitems = len(items)
    if numitems == 0:  # empty items returns empty partition
        return bins

    sub_partitions = []    # list of bin-arrays, each of which contains a possible sub-partition.
    for item in sorted_items:
        b = BinsKeepingContents(2, valueof)
        b.add_item_to_bin(item=item, bin_index=1)
        sub_partitions.append(b)
    alg = CBLDM_algo(numitems=numitems, time_limit=time_limit, len_delta=partition_difference, start_time=start, binner=binner)
    alg.part(sub_partitions)
    return alg.best_partition_so_far


class CBLDM_algo:

    def __init__(self, numitems:int, time_limit:float, len_delta:int, start_time:float, binner:Binner):
        self.sum_delta = np.inf  # partition sum difference
        self.numitems = numitems
        self.time_limit = time_limit
        self.len_delta = len_delta  # partition cardinal difference
        self.start_time = start_time
        self.best_partition_so_far = BinsKeepingContents(2)    # valueof = identity
        self.best_partition_so_far.add_item_to_bin(np.inf, 1)
        self.is_optimal = False
        self.binner = binner

    def part(self, sub_partitions):
        if time.perf_counter() - self.start_time >= self.time_limit or self.is_optimal:
            return
        if len(sub_partitions) == 1:  # possible partition
            potential_partition = sub_partitions[0]
            if abs(len(potential_partition.bins[0]) - len(potential_partition.bins[1])) <= self.len_delta and \
                abs(potential_partition.sums[0] - potential_partition.sums[1]) < self.sum_delta:
                self.best_partition_so_far = potential_partition
                self.sum_delta = abs(potential_partition.sums[0] - potential_partition.sums[1])
                if self.sum_delta == 0:
                    self.is_optimal = True
                return
        else:
            sum_xi = 0  # calculate the sum of the sum differences in items
            max_x = 0  # max sum difference
            sum_mi = 0  # calculate the sum of the cardinal differences in items
            max_m = 0  # max cardinal difference
            for i in sub_partitions:
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
            # Despite being in the paper, the "or" condition breaks the algorithm. For example, it breaks on [1,1,1,1,1,1,1,1,1,1].
            if 2 * max_m - sum_mi > self.len_delta:  # or sum_mi < self.difference:
                return
            if len(sub_partitions) <= math.ceil(self.numitems / 2):
                sub_partitions.sort(key=lambda sub_partition: -abs(sub_partition.sums[0] - sub_partition.sums[1])) # Sort by descending difference.

            # Split items to left branch and right branch according to partition type
            left_sub_partitions  = sub_partitions[2:]
            right_sub_partitions = sub_partitions[2:]

            combined_bins = BinsKeepingContents(2, self.binner.valueof)  # merge partition according to sum of bins
            # combined_bins.combine_bins(0, sub_partitions[0], 0)
            # combined_bins.combine_bins(0, sub_partitions[1], 0)
            # combined_bins.combine_bins(1, sub_partitions[0], 1)
            # combined_bins.combine_bins(1, sub_partitions[1], 1)
            for section in range(2):  # [small, big] + [small, big] -> [small + small, big + big]
                for bin_index in range(2):
                    combined_bins.combine_bins(bin_index, sub_partitions[section], bin_index)
            combined_bins.sort_by_ascending_sum()

            split_bins    = BinsKeepingContents(2, self.binner.valueof)  # split partition according to sum of bins
            # split_bins.combine_bins(0, sub_partitions[0], 1)
            # split_bins.combine_bins(0, sub_partitions[1], 0)
            # split_bins.combine_bins(1, sub_partitions[0], 0)
            # split_bins.combine_bins(1, sub_partitions[1], 1)
            for section in range(2):  # [small, big] + [small, big] -> [small + small, big + big]
                for bin_index in range(2):
                    split_bins.combine_bins(bin_index, sub_partitions[section], (bin_index+section+1)%2)
            split_bins.sort_by_ascending_sum()

            right_sub_partitions.append(combined_bins)
            left_sub_partitions.append(split_bins)
            self.part(left_sub_partitions)
            self.part(right_sub_partitions)


if __name__ == "__main__":
    import doctest, sys
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    if failures>0:
        sys.exit(1)

    # Demonstrating the efficiency of the algorithm on large inputs
    from prtpy import partition, out
    rng = np.random.default_rng(1)

    items = rng.integers(1, 1000, 100)
    assert partition(algorithm=cbldm, numbins=2, items=items, outputtype=out.Sums) == [25390.0, 25390.0]

    # items = rng.integers(1, 1000, 899)
    # assert partition(algorithm=cbldm, numbins=2, items=items, outputtype=out.Sums, time_limit=10) == [225368.0, 225369.0]
