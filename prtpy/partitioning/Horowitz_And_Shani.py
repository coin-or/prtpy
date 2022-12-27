import doctest
from numpy import number

# credit: https://sites.cs.queensu.ca/courses/cisc365/Labs/Week%204/2019%20Week%204%20+%205%20Lab.pdf

# help functions:


def Pair_Sum(v1, v2, k):
    """
    divide to pair

    """
    pair1 = 0
    pair2 = (len(v2)-1)

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
    """"
    create subset sum
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
    sets = [[]]
    for i in range(0, len(s)):  # create a new set for each one
        for j in range(0, len(sets)):
            t = sets[j] + [s[i]]
            sets.append(t)
            if sum(t) == k:  # compare the sum to the target k
                return t
    return None  # no found


def horowitz_sahni(s, k):
    """
    Optimally Scheduling Small Numbers of Identical Parallel Machines,
    by ichard E.Korf and Ethan L. Schreiber (2013) https://ojs.aaai.org/index.php/ICAPS/article/view/13544
    Algorithm 1: get a list, return the pair with the sum within the complete sum, if don't exit raise an error.
    (part all the subset sum and check relative to the complete sum).

    >>> horowitz_sahni([3, 5, 3, 9, 18, 4, 5, 6], 28)
    [18, 4, 6]

    >>> horowitz_sahni([1, 2, 3, 4, 5], 5)
    [5]

    >>> horowitz_sahni([1, 2, 3, 4, 5], 9)
    [4, 5]

    >>> horowitz_sahni([-1, -2, -3, -4], -3)
    [-3]

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
            return i   # equal to the target

    # if the sums don't over than target value, sort lists to pair_sum function:

    # right side
    list_of_right_sum.sort()

    # left side
    list_of_left_sum.sort()

    # call the help function
    if Pair_Sum(list_of_right_sum, list_of_left_sum, k) is not None:
        print(Pair_Sum(list_of_right_sum, list_of_left_sum, k))
    else:
        return None


if __name__ == '__main__':
    doctest.testmod()
    # arr = [3, 5, 3, 9, 18, 4, 5, 6]
    # n = 11
    # print(horowitz_sahni(arr, n))  # [3, 5, 3]
