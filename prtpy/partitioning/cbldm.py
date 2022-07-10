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
from prtpy import Binner, BinsArray, printbins
import time
import math

from prtpy.binners import BinnerKeepingContents


def cbldm(
    binner: Binner, numbins: int, items: List[any],
    time_limit: float = np.inf, 
    partition_difference: int = sys.maxsize) -> BinsArray:
    """
    Balanced number partitioning into two bins.
    :param items - the items to partition. The length must be at most 900--1000 due to stack limitations; the exact maximum can vary between computers.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums
    >>> printbins(cbldm(BinnerKeepingContents(), 2, items=[10], time_limit=1))
    Bin #0: [], sum=0.0
    Bin #1: [10], sum=10.0
    >>> printbins(cbldm(BinnerKeepingContents(), 2, items=[8,7,6,5,4], time_limit=1, partition_difference=1))
    Bin #0: [4, 6, 5], sum=15.0
    Bin #1: [8, 7], sum=15.0
    >>> printbins(cbldm(BinnerKeepingContents(), 2, items=[6,6,5,5,5], time_limit=1, partition_difference=1))
    Bin #0: [6, 6], sum=12.0
    Bin #1: [5, 5, 5], sum=15.0
    >>> printbins(cbldm(BinnerKeepingContents(), 2, items=[4,1,1,1,1], time_limit=1, partition_difference=1))
    Bin #0: [1, 1, 1], sum=3.0
    Bin #1: [4, 1], sum=5.0
    
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
    start = time.perf_counter()
    if numbins != 2:
        raise ValueError("numbins must be 2")
    if time_limit <= 0:
        raise ValueError("time_limit must be positive")
    if partition_difference < 1 or not isinstance(partition_difference, int):
        raise ValueError("partition_difference must be a complete number and >= 1")

    sorted_items = sorted(items, key=binner.valueof, reverse=True) # Sort by descending value
    if binner.valueof(sorted_items[-1])<0:
        raise ValueError("All items must be non-negative")

    numitems = len(items)
    if numitems == 0:  # empty items returns empty partition
        return binner.new_bins(numbins)

    binner = BinnerKeepingContents(binner.valueof)  # Must keep contents, because we need to count the number of items in each bin!

    sub_partitions = []    # list of bin-arrays, each of which contains a possible sub-partition.
    for item in sorted_items:
        b = binner.new_bins(numbins)
        binner.add_item_to_bin(b, item=item, bin_index=1)
        sub_partitions.append(b)
    alg = CBLDM_algo(numitems=numitems, time_limit=time_limit, len_delta=partition_difference, start_time=start, binner=binner)
    alg.part(sub_partitions)
    return alg.best_partition_so_far

def sum_difference(binner:Binner, bins:BinsArray):
    sums = binner.sums(bins)
    return abs(sums[0]-sums[1])

def len_difference(binner:Binner, bins:BinsArray):
    return abs(binner.numitems(bins,0)-binner.numitems(bins,1))

class CBLDM_algo:

    def __init__(self, numitems:int, time_limit:float, len_delta:int, start_time:float, binner:Binner):
        self.sum_delta = np.inf  # partition sum difference
        self.numitems = numitems
        self.time_limit = time_limit
        self.len_delta = len_delta  # partition cardinal difference
        self.start_time = start_time
        self.best_partition_so_far = ([0,np.inf],[0,np.inf])
        self.is_optimal = False
        self.binner = binner

    def part(self, sub_partitions):
        binner = self.binner
        if time.perf_counter() - self.start_time >= self.time_limit or self.is_optimal:
            return
        if len(sub_partitions) == 1:  # possible partition
            potential_partition = sub_partitions[0]
            new_len_delta = len_difference(binner, potential_partition)
            new_sum_delta = sum_difference(binner, potential_partition)
            if new_len_delta <= self.len_delta and new_sum_delta < self.sum_delta:
                self.best_partition_so_far = potential_partition
                self.sum_delta = new_sum_delta
                if self.sum_delta == 0:
                    self.is_optimal = True
                return
        else:
            sum_xi = 0  # calculate the sum of the sum differences in items
            max_x = 0  # max sum difference
            sum_mi = 0  # calculate the sum of the cardinal differences in items
            max_m = 0  # max cardinal difference
            for sub_partition in sub_partitions:
                xi = sum_difference(binner, sub_partition)
                sum_xi += xi
                mi = len_difference(binner, sub_partition)
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
                sub_partitions.sort(key=lambda sub_partition: -sum_difference(binner, sub_partition))

            # Split items to left branch and right branch according to partition type
            left_sub_partitions  = sub_partitions[2:]
            right_sub_partitions = sub_partitions[2:]

            combined_bins = binner.new_bins(2)
            for section in range(2):  # [small, big] + [small, big] -> [small + small, big + big]
                for bin_index in range(2):
                    # combined_bins.combine_bins(bin_index, sub_partitions[section], bin_index)
                    binner.combine_bins(combined_bins, bin_index, sub_partitions[section], bin_index)
            # combined_bins.sort_by_ascending_sum()
            binner.sort_by_ascending_sum(combined_bins)

            split_bins = binner.new_bins(2)
            for section in range(2):  # [small, big] + [small, big] -> [small + small, big + big]
                for bin_index in range(2):
                    # split_bins.combine_bins(bin_index, sub_partitions[section], (bin_index+section+1)%2)
                    binner.combine_bins(split_bins, bin_index, sub_partitions[section], (bin_index+section+1)%2)
            # split_bins.sort_by_ascending_sum()
            binner.sort_by_ascending_sum(split_bins)

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
    sums = partition(algorithm=cbldm, numbins=2, items=items, outputtype=out.Sums)
    print(sums)
    assert sums == [25390.0, 25390.0]

    # items = rng.integers(1, 1000, 899)
    # assert partition(algorithm=cbldm, numbins=2, items=items, outputtype=out.Sums, time_limit=10) == [225368.0, 225369.0]
