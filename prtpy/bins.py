"""
Utility functions and classes for incrementally filling bins during an algorithm.

Author: Erel Segal-Halevi
Since:  2022-02
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Any, Callable


class Bins(ABC):
    """
    An abstract bins structure.
    """

    @abstractmethod
    def __init__(self, numbins: int=0):
        self.num = numbins
        self.valueof = lambda x:x
        pass

    def set_valueof(self, valueof:Callable):
        self.valueof = valueof
        return self

    @abstractmethod
    def add_item_to_bin(self, item: Any, bin_index: int, inplace=True):
        """
        Add the given item, with the given value, to the bin with the given index.

        If inplace is True, the method modifies the current structure and returns None.
        If inplace is False, the method does not modify the current structure, but returns a new Bins structure.
        """
        pass

    @abstractmethod
    def add_empty_bins(self, numbins: int=1):
        """
        Add new empty bins.
        """
        self.num += numbins
        pass

    @abstractmethod
    def remove_bins(self, numbins: int=1):
        """
        Remove bins from the end.
        """
        self.num -= numbins
        pass

    @abstractmethod
    def bin_to_str(self, bin_index: int) -> str:
        pass

    @abstractmethod
    def sort(self):
        """
        Sort the bins by ascending order of sum. For consistency and testing.
        """
        return self

    def __repr__(self) -> str:
        bins_str = [f"Bin #{i}: {self.bin_to_str(i)}" for i in range(self.num)]
        return "\n".join(bins_str)


class BinsKeepingSums(Bins):
    """
    A bins structure that keeps track only of the total sum in each bin.

    >>> bins = BinsKeepingSums(3)
    >>> values = {"a":3, "b":4, "c":5, "d":5, "e":5}
    >>> bins.valueof = lambda x: values[x]
    >>> bins.add_item_to_bin(item="a", bin_index=0)
    Bin #0: sum=3.0
    Bin #1: sum=0.0
    Bin #2: sum=0.0
    >>> bins.add_item_to_bin(item="b", bin_index=1)
    Bin #0: sum=3.0
    Bin #1: sum=4.0
    Bin #2: sum=0.0
    >>> bins.add_item_to_bin(item="c", bin_index=1)
    Bin #0: sum=3.0
    Bin #1: sum=9.0
    Bin #2: sum=0.0
    >>> bins.add_item_to_bin(item="d", bin_index=1, inplace=False)
    Bin #0: sum=3.0
    Bin #1: sum=14.0
    Bin #2: sum=0.0
    >>> bins.add_item_to_bin(item="e", bin_index=2, inplace=False)
    Bin #0: sum=3.0
    Bin #1: sum=9.0
    Bin #2: sum=5.0
    >>> bins.num
    3
    >>> bins.add_empty_bins()
    Bin #0: sum=3.0
    Bin #1: sum=9.0
    Bin #2: sum=0.0
    Bin #3: sum=0.0
    >>> bins.num
    4
    >>> bins.remove_bins()
    Bin #0: sum=3.0
    Bin #1: sum=9.0
    Bin #2: sum=0.0
    >>> bins.num
    3
    """

    def __init__(self, numbins: int=0, sums=None):
        super().__init__(numbins)
        if sums is None:
            sums = np.zeros(numbins)
        self.sums = sums

    def add_empty_bins(self, numbins: int=1):
        super().add_empty_bins(numbins)
        self.sums = np.concatenate((self.sums, np.zeros(numbins)))
        return self

    def remove_bins(self, numbins: int=1):
        super().remove_bins(numbins)
        self.sums = self.sums[:-numbins]
        return self

    def add_item_to_bin(self, item: Any, bin_index: int, inplace=True)->Bins:
        value = self.valueof(item)
        if inplace:
            self.sums[bin_index] += value
            return self
        else:
            new_sums = np.copy(self.sums)
            new_sums[bin_index] += value
            return BinsKeepingSums(self.num, new_sums).set_valueof(self.valueof)

    def bin_to_str(self, bin_index: int) -> str:
        return f"sum={self.sums[bin_index]}"

    def sort(self):
        self.sums.sort()
        return self


class BinsKeepingContents(BinsKeepingSums):
    """
    A bins structure that keeps track of the entire contents of each bin.

    >>> bins = BinsKeepingContents(3)
    >>> values = {"a":3, "b":4, "c":5, "d":5, "e":5}
    >>> bins.valueof = lambda x: values[x]
    >>> bins.add_item_to_bin(item="a", bin_index=0)
    Bin #0: ['a'], sum=3.0
    Bin #1: [], sum=0.0
    Bin #2: [], sum=0.0
    >>> bins.add_item_to_bin(item="b", bin_index=1)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b'], sum=4.0
    Bin #2: [], sum=0.0
    >>> bins.add_item_to_bin(item="c", bin_index=1)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c'], sum=9.0
    Bin #2: [], sum=0.0
    >>> bins.add_item_to_bin(item="d", bin_index=1, inplace=False)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c', 'd'], sum=14.0
    Bin #2: [], sum=0.0
    >>> bins.add_item_to_bin(item="d", bin_index=2, inplace=False)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c'], sum=9.0
    Bin #2: ['d'], sum=5.0
    >>> bins.num
    3
    >>> bins.add_empty_bins()
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c'], sum=9.0
    Bin #2: [], sum=0.0
    Bin #3: [], sum=0.0
    >>> bins.num
    4
    >>> bins.remove_bins()
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c'], sum=9.0
    Bin #2: [], sum=0.0
    >>> bins.num
    3
    """

    def __init__(self, numbins: int=0, sums=None, bins=None):
        super().__init__(numbins, sums)
        if bins is None:
            bins = [[] for _ in range(numbins)]
        self.bins = bins

    def add_empty_bins(self, numbins: int=1):
        super().add_empty_bins(numbins)
        for _ in range(numbins):
            self.bins.append([])
        return self

    def remove_bins(self, numbins: int=1):
        super().remove_bins(numbins)
        self.bins = self.bins[:-numbins]
        return self

    def add_item_to_bin(self, item: Any, bin_index: int, inplace=True)->Bins:
        value = self.valueof(item)
        if inplace:
            self.sums[bin_index] += value
            self.bins[bin_index].append(item)
            return self
        else:
            new_sums = np.copy(self.sums)
            new_sums[bin_index] += value
            new_bins = list(self.bins)
            new_bins[bin_index] = new_bins[bin_index] + [item]
            return BinsKeepingContents(self.num, new_sums, new_bins).set_valueof(self.valueof)

    def bin_to_str(self, bin_index: int) -> str:
        return f"{self.bins[bin_index]}, sum={self.sums[bin_index]}"

    def sort(self):
        self.sums.sort()
        self.bins.sort(key=lambda bin: (sum(bin), len(bin)))
        return self


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
