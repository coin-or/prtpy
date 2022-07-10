"""
Define the various available output formats for a partition algorithm.
"""

from abc import ABC
from typing import Any, List, Callable
from prtpy.bins import Bins, BinsKeepingContents, BinsKeepingSums
from prtpy.binners import Binner, BinnerKeepingContents, BinnerKeepingSums, BinsArray

class OutputType(ABC):
    @classmethod
    def create_empty_bins(cls, numbins: int, valueof: Callable) -> Bins:
        """
        Construct and return a Bins structure. Used at the initialization phase of an algorithm.
        """
        raise NotImplementedError("Choose a specific output type")

    @classmethod
    def create_binner(cls, numbins: int, valueof: Callable) -> Binner:
        """
        Construct and return a Bins structure. Used at the initialization phase of an algorithm.
        """
        raise NotImplementedError("Choose a specific output type")

    @classmethod
    def extract_output_from_bins(cls, bins: Bins) -> Any:
        """
        Return the required output from the given list of filled bins.
        """
        raise NotImplementedError("Choose a specific output type")

    @classmethod
    def extract_output_from_binsarray(cls, bins: BinsArray) -> List:
        """
        Return the required output from the given bins-array.
        """
        raise NotImplementedError("Choose a specific output type")



#
# Outputs based only on sums
#

class Sums(OutputType):
    """ Output the list of sums of all bins (but not the bins' contents).  """
    @classmethod
    def create_empty_bins(cls, numbins: int, valueof: Callable) -> List:
        return BinsKeepingSums(numbins, valueof)

    @classmethod
    def create_binner(cls, numbins: int, valueof: Callable) -> List:
        return BinnerKeepingSums(numbins, valueof)

    @classmethod
    def extract_output_from_sums(cls, sums: List[float]) -> List:
        return list(sums)

    @classmethod
    def extract_output_from_bins(cls, bins: Bins) -> List:
        return cls.extract_output_from_sums(bins.sums)

    @classmethod
    def extract_output_from_binsarray(cls, bins: BinsArray) -> List:
        return cls.extract_output_from_sums(bins)


class LargestSum(Sums):
    """ Output the largest bin sum. """
    @classmethod
    def extract_output_from_sums(cls, sums: List[float]) -> List:
        return max(sums)

class SmallestSum(Sums):
    """ Output the smallest bin sum. """
    @classmethod
    def extract_output_from_sums(cls, sums: List[float]) -> List:
        return min(sums)

class ExtremeSums(Sums):
    """ Output the largest and the smallest sums. """
    @classmethod
    def extract_output_from_sums(cls, sums: List[float]) -> List:
        return (min(sums), max(sums))

class SortedSums(Sums):
    """ Output the sums sorted from small to large. """
    @classmethod
    def extract_output_from_sums(cls, sums: List[float]) -> List:
        return sorted(sums)

class Difference(Sums):
    """ Output the difference between largest and smallest sum. """
    @classmethod
    def extract_output_from_sums(cls, sums: List[float]) -> List:
        return max(sums)-min(sums)

class BinCount(Sums):
    """ Output the total number of bins. """
    @classmethod
    def extract_output_from_sums(cls, sums: List[float]) -> List:
        return len(sums)




#
# Outputs based on the entire partition.
#

class Partition(OutputType):
    """ Output the set of all bins. """

    @classmethod
    def create_empty_bins(cls, numbins: int, valueof: Callable) -> List:
        return BinsKeepingContents(numbins, valueof)

    @classmethod
    def create_binner(cls, numbins: int, valueof: Callable) -> List:
        return BinnerKeepingContents(numbins, valueof)

    @classmethod
    def extract_output_from_sums_and_lists(cls, sums: List[float], lists: List[List[Any]]) -> List:
        return lists

    @classmethod
    def extract_output_from_bins(cls, bins: Bins) -> List:
        return cls.extract_output_from_sums_and_lists(bins.sums, bins.bins)

    @classmethod
    def extract_output_from_binsarray(cls, bins: BinsArray) -> List:
        return cls.extract_output_from_sums_and_lists(bins[0], bins[1])


class PartitionAndSums(Partition):
    """ Output the set of all bins with their sums. """
    @classmethod
    def extract_output_from_bins(cls, bins: Bins) -> List:
        return bins

    @classmethod
    def extract_output_from_sums_and_lists(cls, sums: List[float], lists: List[List[Any]]) -> List:
        return BinsKeepingContents(len(sums), lambda x:x, sums, lists)
