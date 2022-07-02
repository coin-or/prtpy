"""
Define various optimization objectives for a partition algorithm.

>>> objectives = [MaximizeSmallestSum, MaximizeKSmallestSums(2), MinimizeLargestSum, MinimizeKLargestSums(2), MinimizeDifference]
>>> for o in objectives: print(o.value_to_minimize(sums=[1,2,3,4,5], are_sums_in_ascending_order=True))
-1
-3
5
9
4
>>> objectives.append(MaximizeSmallestWeightedSum([1, 1, 1, 3, 4]))
>>> for o in objectives: print(o.value_to_minimize(sums=[2,4,1,5,3]))
-1
-3
5
9
4
-0.75
"""

from typing import List
from abc import ABC, abstractmethod
import numpy as np

class Objective(ABC):
    @abstractmethod
    def value_to_minimize(self, sums:list, are_sums_in_ascending_order:bool=False)->float:
        pass
    def lower_bound(self, current_sums:list, value_to_add:float, bin_index:int, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
        """ 
        Returns an optimistic (lower) bound on the objective value, givan that:
        * the current bin sums are current_sums;
        * we add the given value_to_add to bin with index bin_index;
        * the sum of the remaining items is sum_of_remaining_items.
        This bound is used in branch-and-bound algorithms to prune branches that will never lead to an improved solution.
        """
        return -np.inf     # this means that there is essentially no lower bound (no branch will be pruned).


class MaximizeSmallestSumSingleton(Objective):
    def value_to_minimize(self, sums:list, are_sums_in_ascending_order:bool=False)->float:
        return -sums[0] if are_sums_in_ascending_order else -min(sums)
    def lower_bound(self, current_sums:list, value_to_add:float, bin_index:int, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
        return  -np.inf
MaximizeSmallestSum = MaximizeSmallestSumSingleton()


class MaximizeSmallestWeightedSum(Objective):
    def __init__(self, weights: List[float]):
        self.weights = weights
    def value_to_minimize(self, sums: List[float], are_sums_in_ascending_order=False) -> float:
        if are_sums_in_ascending_order:
            raise ValueError("are_sums_in_ascending_order parameter not supported")
        weighted_sums = [s / w for s, w in zip(sums, self.weights)]
        return -min(weighted_sums)


class MaximizeKSmallestSums(Objective):
    def __init__(self, num_smallest_parts: int):
        self.num_smallest_parts = num_smallest_parts
    def value_to_minimize(self, sums: List[float], are_sums_in_ascending_order=False) -> float:
        sorted_sums = sums if are_sums_in_ascending_order else sorted(sums)
        return -sum(sorted_sums[0: self.num_smallest_parts])


class MinimizeLargestSumSingleton(Objective):
    def value_to_minimize(self, sums:list, are_sums_in_ascending_order:bool=False)->float:
        return sums[-1] if are_sums_in_ascending_order else max(sums)
    def lower_bound(self, current_sums:list, value_to_add:float, bin_index:int, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
        return current_sums[bin_index] + value_to_add
MinimizeLargestSum = MinimizeLargestSumSingleton()

class MinimizeKLargestSums(Objective):
    def __init__(self, num_smallest_parts: int):
        self.num_smallest_parts = num_smallest_parts
    def value_to_minimize(self, sums: List[float], are_sums_in_ascending_order=False) -> float:
        sorted_sums = sums if are_sums_in_ascending_order else sorted(sums)
        return sum(sorted_sums[-self.num_smallest_parts:])

class MinimizeDifferenceSingleton(Objective):
    def value_to_minimize(self, sums: List[float], are_sums_in_ascending_order=False) -> float:
        return sums[-1] - sums[0] if are_sums_in_ascending_order else max(sums) - min(sums)
    def lower_bound(self, current_sums:list, value_to_add:float, bin_index:int, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
        return  -np.inf
MinimizeDifference = MinimizeDifferenceSingleton()



if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
