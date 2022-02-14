"""
The generic partition function.
"""

from prtpy import outputtypes as out, objectives as obj
from typing import Callable, List, Any



def partition(
    algorithm: Callable,
    numbins: int,
    items: Any,
    map_item_to_value: Callable[[Any], float] = None,
    objective: obj.Objective = obj.MinimizeDifference,
    outputtype: out.OutputType = out.Partition,
    **kwargs
) -> List[List[int]]:
    """
    A generic partition routine.

    >>> from greedy import greedy
    >>> import numpy as np
    >>> partition(algorithm=greedy, numbins=2, items=[1,2,3,3,5,9,9])
    [[9, 5, 2], [9, 3, 3, 1]]
    >>> partition(algorithm=greedy, numbins=3, items=[1,2,3,3,5,9,9])
    [[9, 2], [9, 1], [5, 3, 3]]
    >>> partition(algorithm=greedy, numbins=2, items=np.array([1,2,3,3,5,9,9]), outputtype=out.Sums)
    array([16., 16.])
    >>> partition(algorithm=greedy, numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.LargestSum)
    11.0
    >>> partition(algorithm=greedy, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'e', 'b'], ['g', 'c', 'd', 'a']]
    >>> partition(algorithm=greedy, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
    """
    if isinstance(items, dict):  # items is a dict mapping an item to its value.
        item_names = items.keys()
        if map_item_to_value is None:
            map_item_to_value = lambda item: items[item]
    else:  # items is a list
        item_names = items
        if map_item_to_value is None:
            map_item_to_value = lambda item: item
    return algorithm(numbins, item_names, map_item_to_value, objective, outputtype, **kwargs)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
