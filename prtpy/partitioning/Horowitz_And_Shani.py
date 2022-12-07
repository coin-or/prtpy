import doctest

from numpy import number


def horowitz_sahni(lst: list):
    """
    Optimally Scheduling Small Numbers of Identical Parallel Machines,
    by ichard E.Korf and Ethan L. Schreiber (2013) https://ojs.aaai.org/index.php/ICAPS/article/view/13544
    Algorithm 1: get a list, return the pair with the sum within the complete sum, if don't exit raise an error.
    (part all the subset sum and check relative to the complete sum).

    >>> horowitz_sahni([3, 1, 2, 2])
    [3, 1] # 4

    >>> horowitz_sahni([9, 8, 7])
    Traceback (most recent call last):
        ...
    Exception: Exception

    >>> horowitz_sahni([100, 20 ,30])
    Traceback (most recent call last):
        ...
    Exception: Exception

    >>> horowitz_sahni([10, 10, 10, 10] )
     [10, 10] # 20

    >>> horowitz_sahni([0, 2, 4, 3, 1])
    [2,3] # 5

    >>> horowitz_sahni([2, 4, 6, 8, 10])
    Traceback (most recent call last):
        ...
    Exception: Exception

    """

    return number   # Empty implementation


if __name__ == '__main__':
    doctest.testmod()
