"""
    Partition the numbers using the greedy number partitioning algorithm:
       https://en.wikipedia.org/wiki/Greedy_number_partitioning

    Credit: Code review by FMc at https://codereview.stackexchange.com/a/273975/20684.

    >>> from partition import partition
    >>> partition(algorithm=greedy, num_of_bins=2, values=[1,2,3,3,5,9,9])
    [[9, 5, 2], [9, 3, 3, 1]]
    >>> partition(algorithm=greedy, num_of_bins=3, values=[1,2,3,3,5,9,9])
    [[9, 2], [9, 1], [5, 3, 3]]
    >>> partition(algorithm=greedy, num_of_bins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'e', 'b'], ['g', 'c', 'd', 'a']]
    >>> partition(algorithm=greedy, num_of_bins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
"""

from bins import Bins
from outputs import OutputFormat, Sums, LargestSum, SmallestSum, Bins
from typing import Callable


def greedy(
    bins: Bins,
    items: list[any],
    map_item_to_value: Callable[[any], float],
):
    for item in sorted(items, key=map_item_to_value, reverse=True):
        index_of_least_full_bin = min(
            range(bins.num), key=lambda i: bins.sums[i]
        )
        bins.add_item_to_bin(
            item=item,
            value=map_item_to_value(item),
            bin_index=index_of_least_full_bin,
        )


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
