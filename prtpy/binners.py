"""
A partitioning algorithm usually keeps an array of "bins", and fills it incrementally.
Some algorithms (e.g. branch-and-bound algorithms) keep many arrays of bins simultaneously.

A Binner is a class that manages a collection of bin-arrays.
It can create a new bins-array, fill an existing array, etc.

Author: Erel Segal-Halevi
Since:  2022-07
"""

from abc import ABC, abstractmethod
from itertools import permutations

import numpy as np
from typing import Any, Callable, List, Tuple

BinsArray = Any

# def bin2str(bins: BinsArray, bin_index:int):
#     try:
#         # bins is a tuple (sums,lists):
#         sums, lists = bins
#         return f"{lists[bin_index]}, sum={sums[bin_index]}"
#     except:
#         # bins is an array of sums:
#         return f"sum={bins[bin_index]}"

def bins2str(bins: BinsArray)->str:
    try:
        # bins is a tuple (sums,lists):
        sums, lists = bins
        numbins = len(sums)
        bins_str = [f"Bin #{i}: {lists[i]}, sum={sums[i]}" for i in range(numbins)]
    except:
        # bins is an array of sums:
        numbins = len(bins)
        bins_str = [f"Bin #{i}: sum={bins[i]}" for i in range(numbins)]
    return "\n".join(bins_str)

def printbins(bins:BinsArray):
    print(bins2str(bins))

class Binner(ABC):
    """
    An abstract bins-array manager.
    
    All arrays created by the same binner share the following two variables:
     * numbins - the total number of bins.
     * valueof - a function that maps an item to its value.
    """

    def __init__(self, numbins: int, valueof: Callable = lambda x:x):
        self.numbins = numbins
        self.valueof = valueof

    @abstractmethod
    def new_bins(self)->BinsArray:
        '''
        Create a new bins-array with self.numbins bins.
        '''
        return None

    @abstractmethod
    def clone(self, bins:BinsArray)->BinsArray:
        '''
        Create a new bins-array with the same contents as the given bins-array.
        '''
        return None

    @abstractmethod
    def add_item_to_bin(self, bins:BinsArray, item: Any, bin_index: int)->BinsArray:
        """
        Add the given item to the given bin in the given array.
        Return the bins after the addition.
        """
        return bins


    @abstractmethod
    def sort_by_ascending_sum(self, bins:BinsArray):
        """
        Sort the bins by ascending order of sum. For consistency and testing.
        # Return the bins after the sorting.
        """
        pass
        # return bins

    @abstractmethod
    def sums_as_tuple(self, bins: BinsArray) -> Tuple[float]:
        """
        Return a tuple with only the current sums. Can be used as a key in a set or dict.
        """
        return None


    # @abstractmethod
    # def clear_bins(self, numbins):
    #     """
    #     @param: numbins - the number of the bins
    #      clear the content of the bins.
    #     """
    #     pass

    # @abstractmethod
    # def combine_bins(self, ibin, other_bin, other_ibin):
    #     """
    #     combine between bin at index ibin and bin of other bin at index other ibin
    #     """
    #     pass

    # @abstractmethod
    # def combinations(self, other_bins):
    #     '''
    #     generate all the possible combinations of bins between two object bins
    #     NOTE: there is no duplicates combinations
    #     '''
    #     pass


class BinnerKeepingSums(Binner):
    """
    A binner that creates bin-arrays that keep track only of the total sum in each bin.

    >>> values = {"a":3, "b":4, "c":5, "d":5, "e":5}
    >>> binner = BinnerKeepingSums(3, lambda x: values[x])
    >>> bins = binner.new_bins()
    >>> printbins(binner.add_item_to_bin(bins, item="a", bin_index=0))
    Bin #0: sum=3.0
    Bin #1: sum=0.0
    Bin #2: sum=0.0
    >>> _=binner.add_item_to_bin(bins, item="b", bin_index=1)
    >>> printbins(bins)
    Bin #0: sum=3.0
    Bin #1: sum=4.0
    Bin #2: sum=0.0
    >>> _=binner.add_item_to_bin(bins, item="c", bin_index=1)
    >>> printbins(bins)
    Bin #0: sum=3.0
    Bin #1: sum=9.0
    Bin #2: sum=0.0

    Adding to a clone should not change the original:
    >>> printbins(binner.add_item_to_bin(binner.clone(bins), item="d", bin_index=1))
    Bin #0: sum=3.0
    Bin #1: sum=14.0
    Bin #2: sum=0.0
    >>> printbins(bins)
    Bin #0: sum=3.0
    Bin #1: sum=9.0
    Bin #2: sum=0.0
    >>> bins2 = binner.clone(bins)
    >>> _=binner.add_item_to_bin(bins2, item="e", bin_index=2)
    >>> printbins(bins2)
    Bin #0: sum=3.0
    Bin #1: sum=9.0
    Bin #2: sum=5.0
    >>> binner.sort_by_ascending_sum(bins)
    >>> printbins(bins)
    Bin #0: sum=0.0
    Bin #1: sum=3.0
    Bin #2: sum=9.0
    >>> binner.sums_as_tuple(bins)
    (0.0, 3.0, 9.0)
    """

    BinsArray = np.ndarray    # Here, the bins-array is simply an array of the sums.

    def new_bins(self)->BinsArray:
        bins = np.zeros(self.numbins)
        return bins

    def clone(self, bins: BinsArray)->BinsArray:
        return np.array(bins)

    def add_item_to_bin(self, bins: BinsArray, item: Any, bin_index: int)->BinsArray:
        bins[bin_index] += self.valueof(item)
        return bins

    def sums_as_tuple(self, bins: BinsArray) -> Tuple[float]:
        """
        Return a tuple with only the current sums. Can be used as a key in a set or dict.
        """
        return tuple(bins)

    def sort_by_ascending_sum(self, bins:BinsArray)->BinsArray:
        bins.sort()
        # return bins

    # def combine_bins(self, ibin, other_bin, other_ibin):
    #     self.sums[ibin] += other_bin.sums[other_ibin]
    #     return self

    # def combinations(self, other_bins:Bins) -> Iterator[Bins]:
    #     """
    #     >>> b1 = BinsKeepingSums(3, sums=[1,2,3])
    #     >>> b2 = BinsKeepingSums(3, sums=[4,5,6])
    #     >>> for perm in b1.combinations(b2): perm.sums
    #     [5, 7, 9]
    #     [5, 8, 8]
    #     [6, 6, 9]
    #     [6, 7, 8]
    #     [7, 7, 7]
    #     """
    #     if self.numbins != other_bins.numbins:
    #         raise ValueError

    #     yielded = set()
    #     for permutation in permutations(self.sums, self.numbins):
    #         new_sums = sorted(p + l for p, l in zip(permutation, other_bins.sums))
    #         out_ = tuple(el for el in new_sums)
    #         if out_ not in yielded:
    #             yielded.add(out_)
    #             yield BinsKeepingSums(self.numbins, self.valueof, new_sums)


class BinnerKeepingContents(BinnerKeepingSums):
    """
    A binner that creates bin-arrays that keep track of the entire contents of each bin.

    >>> values = {"a":3, "b":4, "c":5, "d":5, "e":5}
    >>> binner = BinnerKeepingContents(3, lambda x: values[x])
    >>> bins = binner.new_bins()
    >>> printbins(binner.add_item_to_bin(bins, item="a", bin_index=0))
    Bin #0: ['a'], sum=3.0
    Bin #1: [], sum=0.0
    Bin #2: [], sum=0.0
    >>> _=binner.add_item_to_bin(bins, item="b", bin_index=1)
    >>> printbins(bins)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b'], sum=4.0
    Bin #2: [], sum=0.0
    >>> _=binner.add_item_to_bin(bins, item="c", bin_index=1);
    >>> printbins(bins)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c'], sum=9.0
    Bin #2: [], sum=0.0

    Adding to a clone should not change the original:
    >>> printbins(binner.add_item_to_bin(binner.clone(bins), item="d", bin_index=1))
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c', 'd'], sum=14.0
    Bin #2: [], sum=0.0
    >>> printbins(bins)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c'], sum=9.0
    Bin #2: [], sum=0.0
    >>> bins2 = binner.clone(bins)
    >>> _=binner.add_item_to_bin(bins2, item="e", bin_index=2)
    >>> printbins(bins2)
    Bin #0: ['a'], sum=3.0
    Bin #1: ['b', 'c'], sum=9.0
    Bin #2: ['e'], sum=5.0
    >>> binner.sort_by_ascending_sum(bins)
    >>> printbins(bins)
    Bin #0: [], sum=0.0
    Bin #1: ['a'], sum=3.0
    Bin #2: ['b', 'c'], sum=9.0
    >>> binner.sums_as_tuple(bins)
    (0.0, 3.0, 9.0)
    """

    BinsArray = Tuple[np.ndarray, List[List]]  # Here, each bins-array is a tuple: sums,lists. sums is an array of sums; lists is a list of lists of items.

    def new_bins(self)->BinsArray:
        sums  = np.zeros(self.numbins)
        lists = [[] for _ in range(self.numbins)]
        return (sums, lists)

    def clone(self, bins: BinsArray)->BinsArray:
        sums, lists = bins
        return (np.array(sums), list(map(list, lists)))

    def add_item_to_bin(self, bins:BinsArray, item: Any, bin_index: int)->BinsArray:
        sums, lists = bins
        value = self.valueof(item)
        sums[bin_index] += value
        lists[bin_index].append(item)
        return bins

    def sums_as_tuple(self, bins: BinsArray) -> Tuple[float]:
        """
        Return a tuple with only the current sums. Can be used as a key in a set or dict.
        """
        return tuple(bins[0])

    def sort_by_ascending_sum(self, bins: BinsArray) -> BinsArray:
        sums, lists = bins
        sorted_indices = sorted(range(self.numbins), key=lambda i: sums[i])
        sums[:] = list(map(sums.__getitem__, sorted_indices))
        lists[:] = list(map(lists.__getitem__, sorted_indices))
        # return bins

    # def combine_bins(self, ibin, other_bin, other_ibin):
    #     super().combine_bins(ibin, other_bin, other_ibin)
    #     self.bins[ibin] += other_bin.bins[other_ibin]
    #     return self

    # def combinations(self, other_bins:Bins) -> Iterator[Bins]:
    #     """
    #     >>> b1 = BinsKeepingContents(3, sums=[1, 2, 3], bins=[[1], [2], [3]])
    #     >>> b2 = BinsKeepingContents(3, sums=[4, 5, 6], bins=[[1, 3], [4, 1], [6]])
    #     >>> for perm in b1.combinations(b2): perm.bins
    #     [[1, 1, 3], [1, 2, 4], [3, 6]]
    #     [[1, 1, 3], [1, 3, 4], [2, 6]]
    #     [[1, 1, 4], [1, 2, 3], [3, 6]]
    #     [[1, 2, 3], [1, 3, 4], [1, 6]]
    #     [[1, 1, 4], [1, 3, 3], [2, 6]]
    #     [[1, 2, 4], [1, 3, 3], [1, 6]]
    #     """
    #     if self.numbins != other_bins.numbins:
    #         raise ValueError

    #     yielded = set()
    #     for permutation in permutations(self.bins, self.numbins):
    #         new_bins = sorted(sorted(p + l) for p, l in zip(permutation, other_bins.bins))
    #         out_ = tuple(tuple(el) for el in new_bins)
    #         if out_ not in yielded:
    #             new_sums = [sum(map(self.valueof,bin) )for bin in new_bins]
    #             yielded.add(out_)
    #             yield BinsKeepingContents(self.numbins, self.valueof, new_sums, new_bins)


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

    import time
    from prtpy import BinsKeepingSums, BinnerKeepingSums

    def compare_ways_to_add_items():
        current_bins = BinsKeepingSums(3)
        current_bins.add_item_to_bin(10, 1).add_item_to_bin(20,2).add_item_to_bin(30,0).sort_by_ascending_sum()
        print(current_bins)
        times = 100000

        start = time.perf_counter()
        for _ in range(times):
            new_sums = list(current_bins.sums)
            new_sums[0] += current_bins.valueof(5)
            new_sums.sort()
        print("list: ",time.perf_counter()-start)  # 0.12
        
        start = time.perf_counter()
        for _ in range(times):
            current_bins.clone().add_item_to_bin(5, 0).sort_by_ascending_sum() 
        print("bins: ",time.perf_counter()-start)  # 0.21; about 1.5-2 times slower. (deepcopy is 10 times slower; __deepcopy__ is 3-4 times slower).
        
        binner = current_bins.get_binner()
        binsarray = np.array(current_bins.sums)
        print(binsarray)

        start = time.perf_counter()
        for _ in range(times):
            binner.sort_by_ascending_sum(binner.add_item_to_bin(binner.clone(binsarray), 5, 0))
        print("binner: ",time.perf_counter()-start)  # 0.14; almost the same as list.
    compare_ways_to_add_items()
