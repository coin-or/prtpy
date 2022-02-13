"""
Define the various available output formats for a partition algorithm.
"""

from abc import ABC, abstractmethod
from bins import *
from typing import Any, List


class OutputType(ABC):
    @abstractmethod
    def create_empty_bins(numbins: int) -> Bins:
        """
        Construct and return a Bins structure. Used at the initialization phase of an algorithm.
        """
        pass

    @abstractmethod
    def extract_output_from_bins(bins: Bins) -> Any:
        """
        Return the required output from the given list of filled bins.
        """
        pass


class Sums(OutputType):
    def create_empty_bins(numbins: int) -> List:
        return BinsKeepingOnlySums(numbins)

    # Output the sums of all the bins (but not the bins contents).
    def extract_output_from_bins(bins: Bins) -> List:
        return bins.sums


class LargestSum(Sums):
    # Output the largest bin sum.
    def extract_output_from_bins(bins: Bins) -> List:
        return max(bins.sums)


class SmallestSum(Sums):
    # Output the smallest bin sum.
    def extract_output_from_bins(bins: Bins) -> List:
        return min(bins.sums)


class Partition(OutputType):
    def create_empty_bins(numbins: int) -> List:
        return BinsKeepingEntireContents(numbins)

    # Output the set of all bins.
    def extract_output_from_bins(bins: Bins) -> List:
        return bins.bins


class PartitionAndSums(Partition):
    # Output the set of all bins.
    def extract_output_from_bins(bins: Bins) -> List:
        return bins
