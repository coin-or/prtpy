"""
Define various optimization objectives for a partition algorithm.

>>> objectives = [MaximizeSmallestSum, MaximizeKSmallestSums(2), MinimizeLargestSum, MinimizeKLargestSums(2), MinimizeDifference, MinimizeDistAvg]
>>> for o in objectives: print(o.value_to_minimize(sums=[1,2,3,4,5], are_sums_in_ascending_order=True))
-1
-3
5
9
4
3.0
>>> objectives.append(MaximizeSmallestWeightedSum([1, 1, 1, 3, 4]))
>>> for o in objectives: print(o.value_to_minimize(sums=[2,4,1,5,3]))
-1
-3
5
9
4
3.0
-0.75
"""

from typing import List
from abc import ABC, abstractmethod
import numpy as np

class Objective(ABC):
    @abstractmethod
    def value_to_minimize(self, sums:list, are_sums_in_ascending_order:bool=False)->float:
        pass
    # def lower_bound(self, current_sums:list, value_to_add:float, bin_index:int, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
    def lower_bound(self, sums:list, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
        """ 
        Returns an optimistic (lower) bound on the objective value, givan that:
        * the current bin sums are current_sums;
        * we add the given value_to_add to bin with index bin_index;
        * the sum of the remaining items is sum_of_remaining_items.
        This bound is used in branch-and-bound algorithms to prune branches that will never lead to an improved solution.
        """
        return -np.inf     # this means that there is essentially no lower bound (no branch will be pruned).


class MaximizeTheSmallestSum(Objective):
    def value_to_minimize(self, sums:list, are_sums_in_ascending_order:bool=False)->float:
        return -sums[0] if are_sums_in_ascending_order else -min(sums)
    def __str__(self) -> str:
        return "maximize-smallest-sum"
    # def lower_bound(self, current_sums:list, value_to_add:float, bin_index:int, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
    def lower_bound(self, sums:list, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
        """
        >>> MaximizeSmallestSum.lower_bound([10,20,30,40,50], sum_of_remaining_items=5)
        -15.0
        >>> MaximizeSmallestSum.lower_bound([10,20,30,40,50], sum_of_remaining_items=20)
        -25.0
        >>> MaximizeSmallestSum.lower_bound([10,20,30,40,50], sum_of_remaining_items=45)
        -35.0
        >>> MaximizeSmallestSum.lower_bound([10,20,30,40,50], sum_of_remaining_items=200)
        -70.0
        >>> MaximizeSmallestSum.lower_bound([0,0,0,0,0], sum_of_remaining_items=54)
        -10.0
        """
        # new_sums = np.array(current_sums)
        # new_sums[bin_index] += value_to_add
        # sorted_sums = sorted(new_sums)       # sorted by ascending sum
        sorted_sums = sums if are_sums_in_ascending_order else sorted(sums)
        # algorithm by Paul A. Robin https://or.stackexchange.com/a/8632/2576 
        sum_of_remaining_items += sorted_sums[0]
        for i in range(1, len(sorted_sums)):
            if sum_of_remaining_items <= i*sorted_sums[i]:
                return -np.floor(sum_of_remaining_items/i)
            sum_of_remaining_items += sorted_sums[i]
        return -np.floor(sum_of_remaining_items/len(sorted_sums))
MaximizeSmallestSum = MaximizeTheSmallestSum()


class MaximizeSmallestWeightedSum(Objective):
    def __init__(self, weights: List[float]):
        self.weights = weights
    def value_to_minimize(self, sums: List[float], are_sums_in_ascending_order=False) -> float:
        if are_sums_in_ascending_order:
            raise ValueError("are_sums_in_ascending_order parameter not supported")
        weighted_sums = [s / w for s, w in zip(sums, self.weights)]
        return -min(weighted_sums)
    def __str__(self) -> str:
        return f"maximize-smallest-weighted-sum({self.weights})"


class MaximizeKSmallestSums(Objective):
    def __init__(self, num_smallest_parts: int):
        self.num_smallest_parts = num_smallest_parts
    def value_to_minimize(self, sums: List[float], are_sums_in_ascending_order=False) -> float:
        sorted_sums = sums if are_sums_in_ascending_order else sorted(sums)
        return -sum(sorted_sums[0: self.num_smallest_parts])
    def __str__(self) -> str:
        return f"maximize-{self.num_smallest_parts}-smallest-sums"


class MinimizeTheLargestSum(Objective):
    def value_to_minimize(self, sums:list, are_sums_in_ascending_order:bool=False)->float:
        return sums[-1] if are_sums_in_ascending_order else max(sums)
    def __str__(self) -> str:
        return "minimize-largest-sum"
    # def lower_bound(self, current_sums:list, value_to_add:float, bin_index:int, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
    #     return current_sums[bin_index] + value_to_add
    # def lower_bound(self, current_sums:list, value_to_add:float, bin_index:int, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
    def lower_bound(self, sums:list, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
        """
        >>> MinimizeLargestSum.lower_bound([10,20,30,40,50], sum_of_remaining_items=5)
        50
        >>> MinimizeLargestSum.lower_bound([10,20,30,40,50], sum_of_remaining_items=20)
        50
        >>> MinimizeLargestSum.lower_bound([10,20,30,40,50], sum_of_remaining_items=45)
        50

        >>> MinimizeLargestSum.lower_bound([10,20,30,40,50], sum_of_remaining_items=200)
        70.0
        >>> MinimizeLargestSum.lower_bound([0,0,0,0,0], sum_of_remaining_items=54)
        11.0
        """
        current_largest_sum = sums[-1] if are_sums_in_ascending_order else max(sums)
        return max(current_largest_sum, np.ceil((sum(sums)+sum_of_remaining_items)/len(sums)))
    

MinimizeLargestSum = MinimizeTheLargestSum()

class MinimizeKLargestSums(Objective):
    def __init__(self, num_smallest_parts: int):
        self.num_smallest_parts = num_smallest_parts
    def value_to_minimize(self, sums: List[float], are_sums_in_ascending_order=False) -> float:
        sorted_sums = sums if are_sums_in_ascending_order else sorted(sums)
        return sum(sorted_sums[-self.num_smallest_parts:])
    def __str__(self) -> str:
        return f"minimize-{self.num_smallest_parts}-largest-sums"

class MinimizeTheDifference(Objective):
    def value_to_minimize(self, sums: List[float], are_sums_in_ascending_order=False) -> float:
        return sums[-1] - sums[0] if are_sums_in_ascending_order else max(sums) - min(sums)
    def __str__(self) -> str:
        return "minimize-largest-difference"
    # def lower_bound(self, current_sums:list, value_to_add:float, bin_index:int, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
    def lower_bound(self, sums:list, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
        """
        >>> MinimizeDifference.lower_bound([10,20,30,40,50], sum_of_remaining_items=5)
        35.0
        >>> MinimizeDifference.lower_bound([10,20,30,40,50], sum_of_remaining_items=20)
        25.0
        >>> MinimizeDifference.lower_bound([10,20,30,40,50], sum_of_remaining_items=45)
        15.0
        >>> MinimizeDifference.lower_bound([10,20,30,40,50], sum_of_remaining_items=200)
        0.0
        >>> MinimizeDifference.lower_bound([0,0,0,0,0], sum_of_remaining_items=54)
        1.0
        """
        return MaximizeSmallestSum.lower_bound(sums, sum_of_remaining_items, are_sums_in_ascending_order) \
             + MinimizeLargestSum.lower_bound(sums, sum_of_remaining_items, are_sums_in_ascending_order)
MinimizeDifference = MinimizeTheDifference()



class MinimizeTheDistanceFromAvg(Objective):
    def value_to_minimize(self, sums:list, are_sums_in_ascending_order:bool=False)->float:
        avg = sum(sums) / len(sums)
        diff_from_avg = 0
        for s in sums:
            if (s > avg):
                diff_from_avg = diff_from_avg + (s - avg)
        return diff_from_avg
    def __str__(self) -> str:
        return "minimize-the-distance-from-avg"
    def lower_bound(self, sums:list, sum_of_remaining_items:float, are_sums_in_ascending_order:bool=False)->float:
        """
        First we calculate the final avg including the remaining items.
        We try to add values from the remaining sum to the bins that haven't reached the avg yet
        (they don't contribute to our final difference because we only take the bins that are more than avg).
        If at any point all bins are equal to avg then we just need to divide the remaining sum amongst all bins
        and the residue will be given out to random bins (one each).
        We calculate and return the difference.
        >>> MinimizeDistAvg.lower_bound([10,20,30,40,50], sum_of_remaining_items=5)
        28.0
        >>> MinimizeDistAvg.lower_bound([10,20,30,40,50], sum_of_remaining_items=20)
        22.0
        >>> MinimizeDistAvg.lower_bound([10,20,30,40,50], sum_of_remaining_items=45)
        12.0

        >>> MinimizeDistAvg.lower_bound([10,20,30,40,50], sum_of_remaining_items=200)
        0.0
        >>> MinimizeDistAvg.lower_bound([0,0,0,0,0], sum_of_remaining_items=54)
        0.8
        """
        remaining = sum_of_remaining_items
        avg = (sum(sums) + remaining) / len(sums)
        diff_from_avg = 0
        for s in sums:
            if (s < avg and remaining > 0):
                remaining = remaining - min(remaining, int(avg - s))
            if(s > avg):
                diff_from_avg = diff_from_avg + (s - avg)
        return diff_from_avg + ((remaining % len(sums)) / len(sums))

MinimizeDistAvg = MinimizeTheDistanceFromAvg()



if __name__ == "__main__":
    import doctest
    print(doctest.testmod())