"""
Defines a Bins structure, for incrementally filling bins during an algorithm.

@author Erel Segal-Halevi
"""

from abc import ABC, abstractmethod
import numpy as np


class Bins(ABC):
    """
    An abstract bins structure.
    """

    @abstractmethod
    def __init__(self, num_of_bins: int):
        self.num = num_of_bins
        pass

    @abstractmethod
    def add_item_to_bin(self, item: any, value: float, bin_index: int):
        pass

    @abstractmethod
    def bin_to_str(self, bin_index: int) -> str:
        pass

    def __repr__(self) -> str:
        bins_str = [
            f"Bin #{i}: {self.bin_to_str(i)}" for i in range(self.num_of_bins)
        ]
        return "\n".join(bins_str)


class BinsKeepingOnlySums(Bins):
    """
    A bins structure that keeps track only of the total sum in each bin.

    >>> bins = BinsKeepingOnlySums(3)
    >>> bins.add_item_to_bin(item="a", value=3, bin_index=0)
    >>> bins.add_item_to_bin(item="", value=4, bin_index=1)
    >>> bins.add_item_to_bin(item="", value=5, bin_index=1)
    >>> bins
    Bin #0: sum=3.0
    Bin #1: sum=9.0
    Bin #2: sum=0.0
    """

    def __init__(self, num_of_bins: int):
        super().__init__(num_of_bins)
        self.sums = np.zeros(num_of_bins)

    def add_item_to_bin(self, item: any, value: float, bin_index: int):
        self.sums[bin_index] += value

    def bin_to_str(self, bin_index: int) -> str:
        return f"sum={self.sums[bin_index]}"


class BinsKeepingEntireContents(BinsKeepingOnlySums):
    """
    A bins structure that keeps track of the entire contents of each bin.

    >>> bins = BinsKeepingEntireContents(3)
    >>> bins.add_item_to_bin(item="a", value=3, bin_index=0)
    >>> bins.add_item_to_bin(item="b", value=4, bin_index=1)
    >>> bins.add_item_to_bin(item="c", value=5, bin_index=1)
    >>> bins
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c'], sum=9.0
    Bin #2: [], sum=0.0
    """

    def __init__(self, num_of_bins: int):
        super().__init__(num_of_bins)
        self.bins = [[] for _ in range(num_of_bins)]

    def add_item_to_bin(self, item: any, value: float, bin_index: int):
        super().add_item_to_bin(item, value, bin_index)
        self.bins[bin_index].append(item)

    def bin_to_str(self, bin_index: int) -> str:
        return f"{self.bins[bin_index]}, sum={self.sums[bin_index]}"


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
