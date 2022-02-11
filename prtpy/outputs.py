"""
Define the various available output formats for a partition algorithm.
"""

from abc import ABC, abstractmethod
from bins import *


class OutputFormat(ABC):
    @abstractmethod
    def get_empty_bins(num_of_bins: int) -> Bins:
        """
        Construct and return a Bins structure. Used at the initialization phase of an algorithm.
        """
        pass

    @abstractmethod
    def get_output(bins: Bins) -> any:
        """
        Return the required output from the given list of filled bins.
        """
        pass


class Sums(OutputFormat):
    # Output the sums of all the bins (but not the bins contents).
    def get_output(bins: Bins) -> list:
        return bins.sums

    def get_empty_bins(num_of_bins: int) -> list:
        return BinsKeepingOnlySums(num_of_bins)


class LargestSum(Sums):
    # Output the largest bin sum.
    def get_output(bins: Bins) -> list:
        return max(bins.sums)


class SmallestSum(Sums):
    # Output the smallest bin sum.
    def get_output(bins: Bins) -> list:
        return min(bins.sums)


class EntirePartition(OutputFormat):
    # Output the set of all bins.
    def get_output(bins: Bins) -> list:
        return bins.bins

    def get_empty_bins(num_of_bins: int) -> list:
        return BinsKeepingEntireContents(num_of_bins)
