import doctest
from heapq import heapify
from heapq import heapify, heappush, heappop


from numpy import number


def schroeppel_shamir(s):
    """
        Algorithm 2: get a list, return list that contain all the pair from the groups partiroins.
        This algorithm help to algorithm1 with the partition.

        # (2^3 = 8)

        >>> schroeppel_shamir([1, 2, 3])
        [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]

        >>> schroeppel_shamir([-1, -2, -3])
        Traceback (most recent call last):
        ...
        Exception: Exception
    """
    sets = [[]]

    # sort s in decrease order
    sorted(s, reverse=True)
    a0 = []
    a1 = []
    b0 = []
    b1 = []

    # randomly divide to four subset sum
    for i in range(len(s) - 4):
        a0.append(i)
        a1.append(i + 1)
        b0.append((i + 2))
        b1.append(i + 3)

    # sort a0, a1 in increase order
    sorted(a0)
    sorted(a1)

    # sort b0, b1 in decrease order
    sorted(b0, reverse=True)
    sorted(b1, reverse=True)

# divide a0,a1 to min heap and b0, b1 to max heap and print each group.

    compute_left_subset_sum(a0, a1)
    compute_right_subset_sum(b0, b1)


def compute_left_subset_sum(a0, a1):
    sets_left = [[]]
    for i in range(0, a0):
        for j in range(0, a1):
            t = a0[j] + [a1[i]]
            sets_left.append(t)
            heapify(sets_left)
    return sets_left


def compute_right_subset_sum(b0, b1):
    sets_right = [[]]
    for i in range(0, b0):
        for j in range(0, b1):
            t = b0[j] + [b1[i]]
            sets_right.append(t)
            heapify(sets_right)
    return sets_right


if __name__ == '__main__':
    doctest.testmod()
