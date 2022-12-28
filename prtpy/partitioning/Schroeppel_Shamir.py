import doctest
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
    for i in range(len(s)-4):
        a0.append(i)
        a1.append(i+1)
        b0.append((i+2))
        b1.append(i+3)

    # sort a0, a1 in increase order
    sorted(a0)
    sorted(a1)

    # sort b0, b1 in decrease order
    sorted(b0, reverse=True)
    sorted(b1, reverse=True)

# the last stage:
# divide a0,a1 to min heap and b0, b1 to max heap and print each group.
# the end
# (didn't finish yet)


if __name__ == '__main__':
    doctest.testmod()
