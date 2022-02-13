"""
Utility functions and classes for incrementally filling bins during an algorithm.

Author: Erel Segal-Halevi
Since:  2022-02
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import List, Any


##### FUNCTIONS
# The following functions do not change their argument - they return a modified copy of it.


def add_input_to_bin_sum(bin_sums: tuple, bin_index: int, input: float):
    """
    Adds the given input value to bin #bin_index in the given list of bins.
    >>> a = [11, 22, 33]
    >>> tuple(add_input_to_bin_sum(a, 0, 77))
    (88, 22, 33)
    >>> tuple(add_input_to_bin_sum(a, 1, 77))
    (11, 99, 33)
    >>> add_input_to_bin_sum(a, 2, 77)
    (11, 22, 110)
    """
    new_bin_sums = list(bin_sums)
    new_bin_sums[bin_index] += input
    return tuple(new_bin_sums)


def add_input_to_bin(bins: list, bin_index: int, input: Any):
    """
    Adds the given input to bin #bin_index in the given list of bins.

    :param bins: the current vector of bin bundles, before adding the new item.
    :param bin_index: the bin to which the item is given.
    :param item_index: the index of the given item.

    >>> a = [[11,22], [33,44], [55,66]]
    >>> add_input_to_bin(a, 1, "aa")
    [[11, 22], [33, 44, 'aa'], [55, 66]]
    >>> add_input_to_bin(a, 2, "bb")
    [[11, 22], [33, 44], [55, 66, 'bb']]
    """
    new_bins = list(bins)
    new_bins[bin_index] = new_bins[bin_index] + [input]
    return new_bins


##### CLASSES
# The following class methods change their argument.


class Bins(ABC):
    """
    An abstract bins structure.
    """

    @abstractmethod
    def __init__(self, numbins: int):
        self.num = numbins
        pass

    @abstractmethod
    def add_item_to_bin(self, item: Any, value: float, bin_index: int, inplace=True):
        """
        Add the given item, with the given value, to the bin with the given index.

        If inplace is True, the method modifies the current structure and returns None.
        If inplace is False, the method does not modify the current structure, but returns a new Bins structure.
        """
        pass

    @abstractmethod
    def bin_to_str(self, bin_index: int) -> str:
        pass

    def __repr__(self) -> str:
        bins_str = [f"Bin #{i}: {self.bin_to_str(i)}" for i in range(self.num)]
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
    >>> bins.add_item_to_bin(item="", value=5, bin_index=1, inplace=False)
    Bin #0: sum=3.0
    Bin #1: sum=14.0
    Bin #2: sum=0.0
    >>> bins.add_item_to_bin(item="", value=5, bin_index=2, inplace=False)
    Bin #0: sum=3.0
    Bin #1: sum=9.0
    Bin #2: sum=5.0
    """

    def __init__(self, numbins: int, sums=None):
        super().__init__(numbins)
        if sums is None:
            sums = np.zeros(numbins)
        self.sums = sums

    def add_item_to_bin(self, item: Any, value: float, bin_index: int, inplace=True):
        if inplace:
            self.sums[bin_index] += value
        else:
            new_sums = np.copy(self.sums)
            new_sums[bin_index] += value
            return BinsKeepingOnlySums(self.num, new_sums)

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
    >>> bins.add_item_to_bin(item="d", value=5, bin_index=1, inplace=False)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c', 'd'], sum=14.0
    Bin #2: [], sum=0.0
    >>> bins.add_item_to_bin(item="d", value=5, bin_index=2, inplace=False)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c'], sum=9.0
    Bin #2: ['d'], sum=5.0
    """

    def __init__(self, numbins: int, sums=None, bins=None):
        super().__init__(numbins, sums)
        if bins is None:
            bins = [[] for _ in range(numbins)]
        self.bins = bins

    def add_item_to_bin(self, item: Any, value: float, bin_index: int, inplace=True):
        if inplace:
            self.sums[bin_index] += value
            self.bins[bin_index].append(item)
        else:
            new_sums = np.copy(self.sums)
            new_sums[bin_index] += value
            new_bins = list(self.bins)
            new_bins[bin_index] = new_bins[bin_index] + [item]
            return BinsKeepingEntireContents(self.num, new_sums, new_bins)

    def bin_to_str(self, bin_index: int) -> str:
        return f"{self.bins[bin_index]}, sum={self.sums[bin_index]}"


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
