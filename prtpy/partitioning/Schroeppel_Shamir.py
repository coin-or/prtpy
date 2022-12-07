import doctest
from numpy import number


def schroeppel_shamir(lst: list) -> list:
    """
        Algorithm 2: get a list, return list that contain all the pair from the groups partiroins.
        This algorithm help to algorithm1 with the partition.

        >>> schroeppel_shamir([1, 2, 3])
        [[1,2], [1,3], [2,3]]

        >>> horowitz_sahni([-1, -2, -3])
        Traceback (most recent call last):
        ...
        Exception: Exception
    """
    return lst  # empty implementation


if __name__ == '__main__':
    doctest.testmod()
