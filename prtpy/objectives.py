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


class Objective(ABC):
    @abstractmethod
    def value_to_minimize(self, sums:list, are_sums_in_ascending_order:bool=False)->float:
        pass

class MaximizeSmallestSumSingleton(Objective):
    def value_to_minimize(self, sums:list, are_sums_in_ascending_order:bool=False)->float:
        return -sums[0] if are_sums_in_ascending_order else -min(sums)
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
MinimizeDifference = MinimizeDifferenceSingleton()



if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
