"""
Optimally Scheduling Small Numbers of Identical Parallel Machines,
by Richard E.Korf and Ethan L. Schreiber (2013) https://ojs.aaai.org/index.php/ICAPS/article/view/13544
Yoel Chemla
"""
# credit: https://sites.cs.queensu.ca/courses/cisc365/Labs/Week%204/2019%20Week%204%20+%205%20Lab.pdf

import doctest
import math
import sys

import numpy as np


# help functions:
def Pair_Sum(v1, v2, k):
    """
        This function sort the two lists by sum and check by 2 points(from the start on the first list, and from the end on
        the second list) if the sum of the 2 lists equal to target and each run update the nearest if the correct sum didn't found
        - if the correct sum found, return the index of the lists.
        else: return the nearest.

        >>> Pair_Sum([[], [1], [1, 4], [1, 4, 5], [1, 5], [4], [4, 5], [5]], [[], [2], [9], [9, 2], [9, 13], [9, 13, 2], [13], [13, 2]], 3)
        (1, 1)

        >>> Pair_Sum([[], [1], [1, 4], [1, 4, 5], [1, 5], [4], [4, 5], [5]], [[], [2], [9], [9, 2], [9, 13], [9, 13, 2], [13], [13, 2]], 14)
        (1, 4)

        >>> Pair_Sum([[], [1], [1, 4], [1, 4, 5], [1, 5], [4], [4, 5], [5]], [[], [2], [9], [9, 2], [9, 13], [9, 13, 2], [13], [13, 2]], 34)
        (7, 7)

        >>> Pair_Sum([[], [1], [1, 4]], [[], [9, 2], [13],  [13, 2], [9, 13], [9, 13, 2]], 20)#lengths of list are not equal
        (2, 3)
        """

    v1.sort(key=sum)
    v2.sort(key=sum)

    pair1 = 0
    pair2 = (len(v2) - 1)
    diff_min = math.inf
    diff_pair = 0, 0

    while pair1 <= (len(v1) - 1) and (pair2 >= 0):
        ans = v1[pair1] + v2[pair2]
        t = sum(ans)
        if t < k:
            if k - t < diff_min:
                diff_min = abs(t - k)
                diff_pair = pair1, pair2
            pair1 = pair1 + 1

        elif t == k:
            return pair1, pair2
        else:  # t > k
            if t - k < diff_min:
                diff_min = abs(t - k)
                diff_pair = pair1, pair2
            pair2 = pair2 - 1
    return diff_pair


    #  use power set by python
def poewer_set(s):
    """
    create all the subset sum
    
    >>> poewer_set([1, 2])
    [[], [1], [2], [1, 2]]

    >>> poewer_set([])
    [[]]

    >>> poewer_set([1, 2, 3])
    [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    """
    x = len(s)
    arr = [1 << i for i in range(x)]

    def help_function(s):
        for i in range(1 << x):
            yield [ss for res, ss in zip(arr, s) if i & res]

    temp = help_function(s)
    y = [i for i in temp]
    return y


def Horowitz_Sahni(s, k):
    """
    Algorithm 1: get a list, return the subset sum within the sum that equal to target, if don't exist: return the
    nearest sum that most close (part all the subset sum and check relative to the complete sum).

    >>> Horowitz_Sahni([3, 5, 3, 9, 18, 4, 5, 6], 28)
    [18, 4, 6]

    >>> Horowitz_Sahni([1, 2, 3, 4, 5], 4)
    [4]

    >>> Horowitz_Sahni([1, 2, 3, 4, 5], 9)
    [4, 5]

    >>> Horowitz_Sahni([-1, -2, -3, -4], -3)
    [-3]

    >>> Horowitz_Sahni([1, 2, 3, 4], 11)
    [1, 2, 3, 4]

    >>> Horowitz_Sahni([1, 2, 3, 97], 98)
    [1, 97]

    """
    left_sum = s[:len(s) // 2]
    right_sum = s[len(s) // 2:]

    # send to help function and create list of the left and right sum
    list_of_right_sum = poewer_set(right_sum)
    list_of_left_sum = poewer_set(left_sum)

    #     right side
    for i in list_of_right_sum:
        if sum(i) == k:
            return i  # equal to the target

    # left side
    for i in list_of_left_sum:
        if sum(i) == k:
            return i  # equal to the target

    #  send the lists and the target to pair_sum function:
    ans_pair = Pair_Sum(list_of_left_sum, list_of_right_sum, k)

    left_side_list = list_of_left_sum[ans_pair[0]]
    right_side_list = list_of_right_sum[ans_pair[1]]

    ans_arr = [left_side_list, right_side_list]

    # convert from list of list -> list
    arr = [ans_arr[m][n] for m in range(len(ans_arr)) for n in range(len(ans_arr[m]))]
    return arr


if __name__ == '__main__':
    doctest.testmod()
