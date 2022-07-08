"""
A partitioning algorithm usually keeps an array of "bins", and fills it incrementally.
Some algorithms (e.g. branch-and-bound algorithms) keep many arrays of bins simultaneously.

A Binner is a class that manages a collection of bin-arrays.
It can create a new bins-array, fill an existing array, etc.

It uses the FlyWeight design pattern. See: https://refactoring.guru/design-patterns/flyweight

Author: Erel Segal-Halevi
Since:  2022-07
"""

from abc import ABC, abstractmethod

import numpy as np, itertools
from typing import Any, Callable, List, Tuple, Iterator

BinsArray = Any

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
    def new_bins(self, numbins=None)->BinsArray:
        '''
        Create a new bins-array with numbins or self.numbins bins.
        '''
        return None

    @abstractmethod
    def clone(self, bins:BinsArray)->BinsArray:
        '''
        Create a new bins-array with the same contents as the given bins-array.
        '''
        return None

    @abstractmethod
    def add_empty_bins(self, bins: BinsArray, numbins:int)->BinsArray:
        '''
        Add some new empty bins at the end of the given BinsArray.
        Returns a copy of "bins" with the added empty bins.
        NOTE: This does NOT change bins in-place; it returns a copy.
        '''
        pass

    @abstractmethod
    def remove_bins(self, bins: BinsArray, numbins:int)->BinsArray:
        '''
        Remove some bins from the end of the given BinsArray.
        Returns a copy of "bins" with the removed bins.
        NOTE: This does NOT change bins in-place; it returns a copy.
        '''
        pass

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
        """
        pass
        # return bins

    @abstractmethod
    def sums(self, bins: BinsArray) -> Tuple[float]:
        """
        Return only the current sums. 
        """
        return None

    def sums_as_tuple(self, bins: BinsArray) -> Tuple[float]:
        """
        Return a tuple with only the current sums. Can be used as a key in a set or dict.
        """
        return tuple(self.sums(bins))

    @abstractmethod
    def combine_bins(self, bins1:BinsArray, ibin1:int, bins2:BinsArray, ibin2:int):
        """
        Combine between bin ibin1 at array bins1 to bin ibin2 at array bins2.
        NOTE: bins1 is modified; bins2 is not.
        """
        pass

    @abstractmethod
    def all_combinations(self, bins1: BinsArray, bins2: BinsArray)->Iterator[BinsArray]:
        '''
        generate all the possible combinations of bins between two object bins
        NOTE: duplicate combinations are not returned.
        '''
        pass

    @abstractmethod
    def clone_with_new_numbins(self,  new_numbins:int):
        pass


    # @abstractmethod
    # def clear_bins(self, numbins):
    #     """
    #     @param: numbins - the number of the bins
    #      clear the content of the bins.
    #     """
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

    >>> printbins(binner.add_empty_bins(bins, 1))
    Bin #0: sum=0.0
    Bin #1: sum=3.0
    Bin #2: sum=9.0
    Bin #3: sum=0.0
    >>> printbins(binner.remove_bins(bins, 1))
    Bin #0: sum=0.0
    Bin #1: sum=3.0
    """

    BinsArray = np.ndarray    # Here, the bins-array is simply an array of the sums.

    def new_bins(self, numbins=None)->BinsArray:
        if numbins is None: numbins = self.numbins
        bins = np.zeros(numbins)
        return bins

    def clone(self, bins: BinsArray)->BinsArray:
        return np.array(bins)

    def add_empty_bins(self, bins: BinsArray, numbins:int)->BinsArray:
        '''
        Add some new empty bins at the end of the given BinsArray.
        Returns a copy of "bins" with the added empty bins.
        NOTE: This does NOT change bins in-place; it returns a copy.
        '''
        return np.append(bins, np.zeros(numbins))

    def remove_bins(self, bins: BinsArray, numbins:int)->BinsArray:
        '''
        Remove some bins from the end of the given BinsArray.
        Returns a copy of "bins" with the removed bins.
        NOTE: This does NOT change bins in-place; it returns a copy.
        '''
        return bins[0:len(bins)-numbins]

    def add_item_to_bin(self, bins: BinsArray, item: Any, bin_index: int)->BinsArray:
        bins[bin_index] += self.valueof(item)
        return bins

    def sums(self, bins: BinsArray) -> Tuple[float]:
        return bins

    def sort_by_ascending_sum(self, bins:BinsArray)->BinsArray:
        bins.sort()
        # return bins

    def combine_bins(self, bins1:BinsArray, ibin1:int, bins2:BinsArray, ibin2:int):
        bins1[ibin1] += bins2[ibin2]

    def all_combinations(self, bins1: BinsArray, bins2: BinsArray)->Iterator[BinsArray]:
        """
        >>> binner = BinnerKeepingSums(3)
        >>> b1 = [1,2,3]
        >>> b2 = [4,5,6]
        >>> for perm in binner.all_combinations(b1, b2): perm
        [5, 7, 9]
        [5, 8, 8]
        [6, 6, 9]
        [6, 7, 8]
        [7, 7, 7]
        >>> b1 = [1,20,300]
        >>> b2 = [4,50,600]
        >>> for perm in binner.all_combinations(b1, b2): perm
        [5, 70, 900]
        [5, 350, 620]
        [24, 51, 900]
        [24, 350, 601]
        [51, 304, 620]
        [70, 304, 601]
        """
        yielded = set()   # prevent duplicates
        for perm in itertools.permutations(range(self.numbins)):
            # print("perm=",perm)
            new_sums = [bins1[perm[i]] + bins2[i] for i in range(self.numbins)]
            new_sums.sort()   # to avoid duplicates
            new_sums_tuple = tuple(new_sums)
            if new_sums_tuple not in yielded:
                yielded.add(new_sums_tuple)
                yield new_sums

    def clone_with_new_numbins(self,  new_numbins:int):
        return BinnerKeepingSums(new_numbins, self.valueof)


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


    >>> printbins(binner.add_empty_bins(bins, 1))
    Bin #0: [], sum=0.0
    Bin #1: ['a'], sum=3.0
    Bin #2: ['b', 'c'], sum=9.0
    Bin #3: [], sum=0.0
    >>> printbins(binner.remove_bins(bins, 1))
    Bin #0: [], sum=0.0
    Bin #1: ['a'], sum=3.0
    """

    BinsArray = Tuple[np.ndarray, List[List]]  # Here, each bins-array is a tuple: sums,lists. sums is an array of sums; lists is a list of lists of items.

    def new_bins(self, numbins:int=None)->BinsArray:
        if numbins is None: numbins = self.numbins
        sums  = np.zeros(numbins)
        lists = [[] for _ in range(numbins)]
        return (sums, lists)

    def clone(self, bins: BinsArray)->BinsArray:
        sums, lists = bins
        return (np.array(sums), list(map(list, lists)))

    def add_empty_bins(self, bins: BinsArray, numbins:int):
        sums, lists = bins
        new_sums = np.append(sums, np.zeros(numbins))
        new_lists = lists + numbins*[[]]
        return (new_sums, new_lists)

    def remove_bins(self, bins: BinsArray, numbins:int)->BinsArray:
        '''
        Remove some bins from the end of the given BinsArray.
        Returns a copy of "bins" with the removed bins.
        NOTE: This does NOT change bins in-place; it returns a copy.
        '''
        sums, lists = bins
        new_sums =  sums[0:len(sums)-numbins]
        new_lists = lists[0:len(lists)-numbins]
        return (new_sums, new_lists)

    def add_item_to_bin(self, bins:BinsArray, item: Any, bin_index: int)->BinsArray:
        sums, lists = bins
        value = self.valueof(item)
        sums[bin_index] += value
        lists[bin_index].append(item)
        return bins

    def sums(self, bins: BinsArray) -> Tuple[float]:
        return bins[0]

    def sort_by_ascending_sum(self, bins: BinsArray) -> BinsArray:
        sums, lists = bins
        sorted_indices = sorted(range(self.numbins), key=lambda i: sums[i])
        sums[:] = list(map(sums.__getitem__, sorted_indices))
        lists[:] = list(map(lists.__getitem__, sorted_indices))
        # return bins

    def combine_bins(self, bins1:BinsArray, ibin1:int, bins2:BinsArray, ibin2:int):
        sums1, lists1 = bins1
        sums2, lists2 = bins2
        sums1[ibin1] += sums2[ibin2]
        lists1[ibin1] += lists2[ibin2]

    def all_combinations(self, bins1: BinsArray, bins2: BinsArray)->Iterator[BinsArray]:
        """
        >>> binner = BinnerKeepingContents(3)
        >>> b1 = ([1, 20, 300],  [[1], [20], [300]])
        >>> b2 = ([4, 50, 600],  [[1, 3], [4, 46], [600]])
        >>> for perm in binner.all_combinations(b1,b2): perm[1]
        [[1, 1, 3], [4, 20, 46], [300, 600]]
        [[1, 1, 3], [4, 46, 300], [20, 600]]
        [[1, 3, 20], [1, 4, 46], [300, 600]]
        [[1, 3, 20], [4, 46, 300], [1, 600]]
        [[1, 4, 46], [1, 3, 300], [20, 600]]
        [[4, 20, 46], [1, 3, 300], [1, 600]]
        """
        yielded = set() # to avoid duplicates
        sums1, lists1 = bins1
        sums2, lists2 = bins2
        for perm in itertools.permutations(range(self.numbins)):
            new_sums =  [sums1[perm[i]] + sums2[i] for i in range(self.numbins)]
            new_lists = [sorted(lists1[perm[i]] + lists2[i]) for i in range(self.numbins)]  # sorting to avoid duplicates
            new_bins = (new_sums, new_lists)
            self.sort_by_ascending_sum(new_bins)
            new_lists_tuple = tuple(map(tuple,new_bins[1]))
            if new_lists_tuple not in yielded:
                yielded.add(new_lists_tuple)
                yield new_bins

    def clone_with_new_numbins(self,  new_numbins:int):
        return BinnerKeepingContents(new_numbins, self.valueof)


if __name__ == "__main__":
    import doctest, sys
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    if failures>0:
        sys.exit(1)


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
    # compare_ways_to_add_items()