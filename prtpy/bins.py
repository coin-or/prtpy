"""
Utility functions and classes for incrementally filling bins during an algorithm.

Author: Erel Segal-Halevi
Co-Authors: Jonathan Escojido & Samuel Harroch
Since:  2022-02
"""

from abc import ABC, abstractmethod
from typing import Iterator
from copy import deepcopy
from itertools import permutations

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
    def add_item_to_bin(self, item: Any, bin_index: int):
        """
        Add the given item, with the given value, to the bin with the given index.
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

    @abstractmethod
    def clear_bins(self, numbins):
        """
        @param: numbins - the number of the bins
         clear the content of the bins.
        """
        pass

    @abstractmethod
    def combine_bins(self, ibin, other_bin, other_ibin):
        """
        combine between bin at index ibin and bin of other bin at index other ibin
        """
        pass

    @abstractmethod
    def combinations(self, other_bins):
        '''
        generate all the possible combinations of bins between two object bins
        NOTE: there is no duplicates combinations
        '''
        pass

    @abstractmethod
    def create_new_bins(self, numbins):
        '''
        @param: numbins - the number of the bins
        create new bins object
        '''
        pass

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

    Adding to a deep copy should not change the original:
    >>> deepcopy(bins).add_item_to_bin(item="d", bin_index=1)
    Bin #0: sum=3.0
    Bin #1: sum=14.0
    Bin #2: sum=0.0
    >>> deepcopy(bins).add_item_to_bin(item="e", bin_index=2)
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
    >>> bins.sort()
    Bin #0: sum=0.0
    Bin #1: sum=3.0
    Bin #2: sum=9.0
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

    def add_item_to_bin(self, item: Any, bin_index: int)->Bins:
        value = self.valueof(item)
        self.sums[bin_index] += value
        return self

    def bin_to_str(self, bin_index: int) -> str:
        return f"sum={self.sums[bin_index]}"

    def sort(self):
        self.sums.sort()
        return self

    def clear_bins(self, numbins):
        self.sums = np.zeros(numbins)
        return self

    def combine_bins(self, ibin, other_bin, other_ibin):
        self.sums[ibin] += other_bin.sums[other_ibin]
        return self

    def combinations(self, other_bins:Bins) -> Iterator[Bins]:
        """
        >>> b1 = BinsKeepingSums(3,[1,2,3])
        >>> b2 = BinsKeepingSums(3,[4,5,6])
        >>> for perm in b1.combinations(b2): perm.sums
        [5, 7, 9]
        [5, 8, 8]
        [6, 6, 9]
        [6, 7, 8]
        [7, 7, 7]
        """
        if self.num != other_bins.num:
            raise ValueError

        yielded = set()
        for permutation in permutations(self.sums, self.num):
            new_sums = sorted(p + l for p, l in zip(permutation, other_bins.sums))
            out_ = tuple(el for el in new_sums)
            if out_ not in yielded:
                yielded.add(out_)
                yield BinsKeepingSums(self.num, new_sums).set_valueof(self.valueof)

    def create_new_bins(self, numbins):
        return BinsKeepingSums(numbins).set_valueof(self.valueof)


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

    Adding to a deep copy should not change the original:
    >>> deepcopy(bins).add_item_to_bin(item="d", bin_index=1)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c', 'd'], sum=14.0
    Bin #2: [], sum=0.0
    >>> deepcopy(bins).add_item_to_bin(item="d", bin_index=2)
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
    >>> bins.sort()
    Bin #0: [], sum=0.0
    Bin #1: ['a'], sum=3.0
    Bin #2: ['b', 'c'], sum=9.0
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

    def add_item_to_bin(self, item: Any, bin_index: int)->Bins:
        value = self.valueof(item)
        self.sums[bin_index] += value
        self.bins[bin_index].append(item)
        return self

    def bin_to_str(self, bin_index: int) -> str:
        return f"{self.bins[bin_index]}, sum={self.sums[bin_index]}"

    def sort(self):
        sorted_indices = sorted(range(self.num), key=lambda i: self.sums[i])
        self.sums = [self.sums[sorted_indices[i]] for i in range(self.num)]
        self.bins = [self.bins[sorted_indices[i]] for i in range(self.num)]
        return self

    def clear_bins(self, numbins):
        super().clear_bins(numbins)
        self.bins = [[] for _ in range(numbins)]
        return self

    def combine_bins(self, ibin, other_bin, other_ibin):
        super().combine_bins(ibin, other_bin, other_ibin)
        self.bins[ibin] += other_bin.bins[other_ibin]
        return self

    def combinations(self, other_bins:Bins) -> Iterator[Bins]:
        """
        >>> b1 = BinsKeepingContents(3, [1, 2, 3], [[1], [2], [3]])
        >>> b2 = BinsKeepingContents(3, [4, 5, 6], [[1, 3], [4, 1], [6]])
        >>> for perm in b1.combinations(b2): perm.bins
        [[1, 1, 3], [1, 2, 4], [3, 6]]
        [[1, 1, 3], [1, 3, 4], [2, 6]]
        [[1, 1, 4], [1, 2, 3], [3, 6]]
        [[1, 2, 3], [1, 3, 4], [1, 6]]
        [[1, 1, 4], [1, 3, 3], [2, 6]]
        [[1, 2, 4], [1, 3, 3], [1, 6]]
        """
        if self.num != other_bins.num:
            raise ValueError

        yielded = set()
        for permutation in permutations(self.bins, self.num):
            new_bins = sorted(sorted(p + l) for p, l in zip(permutation, other_bins.bins))
            out_ = tuple(tuple(el) for el in new_bins)
            if out_ not in yielded:
                new_sums = [sum(map(self.valueof,bin) )for bin in new_bins]
                yielded.add(out_)
                yield BinsKeepingContents(self.num, new_sums,new_bins).set_valueof(self.valueof)

    def create_new_bins(self, numbins):
        return BinsKeepingContents(numbins).set_valueof(self.valueof)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

