"""
Define various optimization objectives for a partition algorithm.

>>> objectives = [MaximizeSmallestSum, MaximizeKSmallestSums(2), MinimizeLargestSum, MinimizeKLargestSums(2), MinimizeDifference]
>>> for o in objectives: print(o.get_value_to_minimize([1,2,3,4,5], are_sums_in_ascending_order=True))
-1
-3
5
9
4
>>> objectives.append(MaximizeSmallestWeightedSum([1, 1, 1, 3, 4]))
>>> for o in objectives: print(o.get_value_to_minimize([2,4,1,5,3]))
-1
-3
5
9
4
-0.75
"""

from typing import List, Callable
from dataclasses import dataclass

@dataclass
class Objective:
    get_value_to_minimize: Callable

MaximizeSmallestSum = Objective(
    lambda sums, are_sums_in_ascending_order=False: 
        -sums[0] if are_sums_in_ascending_order else -min(sums)
)

def MaximizeSmallestWeightedSum(weights: List[float]):
    def get_value_to_minimize(sums: List[float], are_sums_in_ascending_order=False) -> float:
        if are_sums_in_ascending_order:
            raise ValueError("are_sums_in_ascending_order parameter not supported")
        weighted_sums = [s/w for s,w in zip(sums,weights)]
        return -min(weighted_sums)
    return Objective(get_value_to_minimize)

def MaximizeKSmallestSums(num_smallest_parts: int):
    def get_value_to_minimize(sums: List[float], are_sums_in_ascending_order=False) -> float:
        sorted_sums = sums if are_sums_in_ascending_order else sorted(sums)
        return -sum(sorted_sums[0 : num_smallest_parts])
    return Objective(get_value_to_minimize)

MinimizeLargestSum = Objective(
    lambda sums, are_sums_in_ascending_order=False:
        sums[-1] if are_sums_in_ascending_order else max(sums)
)

def MinimizeKLargestSums(num_smallest_parts: int):
    def get_value_to_minimize(sums: List[float], are_sums_in_ascending_order=False) -> float:
        sorted_sums = sums if are_sums_in_ascending_order else sorted(sums)
        return sum(sorted_sums[-num_smallest_parts:])
    return Objective(get_value_to_minimize)

MinimizeDifference = Objective(
    lambda sums, are_sums_in_ascending_order=False: 
        sums[-1] - sums[0] if are_sums_in_ascending_order else max(sums) - min(sums)
)



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
