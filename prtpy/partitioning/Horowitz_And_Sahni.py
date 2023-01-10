"""
Optimally Scheduling Small Numbers of Identical Parallel Machines,
by ichard E.Korf and Ethan L. Schreiber (2013) https://ojs.aaai.org/index.php/ICAPS/article/view/13544
Yoel Chemla
"""
import doctest
import numpy as np
# credit: https://sites.cs.queensu.ca/courses/cisc365/Labs/Week%204/2019%20Week%204%20+%205%20Lab.pdf


# help functions:
def Pair_Sum(v1, v2, k):
    """
    divide to pair
    """
    pair1 = 0
    pair2 = (len(v2) - 1)

    while pair1 <= (len(v1) - 1) and (pair2 >= 0):
        ans = v1[pair1] + v2[pair2]
        t = sum(ans)
        if t < k:
            pair1 = pair1 + 1
        elif t == k:
            return pair1, pair2
        else:
            pair2 = pair2 - 1
    return None


def generate_subset_sum(s):
    """
    create subset sum
    >>> generate_subset_sum([1, 2])
    [[], [1], [2], [1, 2]]

    >>> generate_subset_sum([])
    [[]]
    """
    sets = [[]]
    for i in range(0, len(s)):
        length_sets = len(sets)
        for j in range(0, length_sets):
            t = sets[j] + [s[i]]
            sets.append(t)  # add t in the set
    return sets


def compute_each_subset_sum(s, k):
    """
    compute the sum of each subset sum
    """
    ans = generate_subset_sum(s)
    arr_sum = []
    # print(ans)
    sets = [[]]
    for i in range(0, len(s)):  # create a new set for each one
        for j in range(0, len(sets)):
            t = sets[j] + [s[i]]
            sets.append(t)
            arr_sum.append(sum(t))
            if sum(t) == k:  # compare the sum to the target k
                # print("the res is: ", t)
                return t

    closest = closest_value(arr_sum, k)  # call to func that compute the nearest value
    i = 0
    for i in range(len(sets)):
        if sum(sets[i]) == closest:
            # print(sets[i])
            return sets[i]
    # return None  # no found


def closest_value(input_list, input_value):
    """
     find the nearest value in the list
    """
    arr = np.asarray(input_list)
    i = (np.abs(arr - input_value)).argmin()
    return arr[i]


def Horowitz_Sahni(s, k):
    """
    Algorithm 1: get a list, return the pair with the sum within the complete sum, if don't exit raise an error.
    (part all the subset sum and check relative to the complete sum).

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

    """
    left_sum = s[:len(s) // 2]
    right_sum = s[len(s) // 2:]

    # send to help function and create list of the left and right sum
    list_of_right_sum = generate_subset_sum(right_sum)
    list_of_left_sum = generate_subset_sum(left_sum)

    # Checks the sums if over than target value:

    #     right side
    for i in list_of_right_sum:
        if sum(i) == k:
            return i  # equal to the target

    # left side
    for i in list_of_left_sum:
        if sum(i) == k:
            return i  # equal to the target

    # if the sums don't over than target value, sort lists to pair_sum function:

    # right side
    list_of_right_sum.sort()

    # left side
    list_of_left_sum.sort()

    # call the help function
    if Pair_Sum(list_of_right_sum, list_of_left_sum, k) is not None:
        # print(Pair_Sum(list_of_right_sum, list_of_left_sum, k))
        return Pair_Sum(list_of_right_sum, list_of_left_sum, k)
    else:
        # if we didn't found a set that equal to target
        # print(compute_each_subset_sum(s, k))
        return compute_each_subset_sum(s, k)


if __name__ == '__main__':
    doctest.testmod()
    # arr = [3, 5, 3, 9, 18, 4, 5, 6]
    # n = 11
    # print(Horowitz_Sahni(arr, n))  # [3, 5, 3]
    # compute_each_subset_sum([1, 2, 3, 4, 5], 7)

    # print(Horowitz_Sahni([1, 2, 3, 4, 5], 22))
    # s = [1, 2, 3, 4, 5]
    # print(generate_subset_sum(s))
    # print(len(generate_subset_sum(s)))
