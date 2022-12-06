import doctest


def greedy(lst: list, t: int) -> list:
    """
    Optimally Scheduling Small Numbers of Identical Parallel Machines,
    by ichard E.Korf and Ethan L. Schreiber (2013) https://ojs.aaai.org/index.php/ICAPS/article/view/13544
    Algorithm 1: get a list and a number, return a list that contain a subset that equal to the number t.


    >>> greedy([3,1,1,2,2,1], 4)
    [3, 1]

    >>> greedy([9, 8, 7], 0)
    []

    >>> greedy([100, 20 ,30], 300)
    Traceback (most recent call last):
        ...
    Exception: Exception

    >>> greedy([10, 10, 10, 10], -1)
     Traceback (most recent call last):
        ...
     Exception: Exception

    >>> greedy([1,2,3], 6)
    [1, 2, 3]

    >>> greedy([2, 4, 6, 8, 10], 10)
    [4, 6]

    """
    return lst  # Empty implementation


if __name__ == '__main__':
    doctest.testmod()
