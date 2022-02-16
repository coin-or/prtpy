from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj

def bidirectional_balanced(
    numbins: int,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = None,  # Not used
    outputtype: out.OutputType = out.Partition,
):
    """
    Partition the numbers using "bidirectional balanced partition" (ABCCBA order).

    >>> bidirectional_balanced(numbins=2, items=[1,2,3,4,5,9])
    [[9, 3, 2], [5, 4, 1]]
    >>> bidirectional_balanced(numbins=3, items=[1,2,3,4,5,9])
    [[9, 1], [5, 2], [4, 3]]

    >>> from prtpy.partitioning import partition
    >>> partition(algorithm=bidirectional_balanced, numbins=3, items={"a":1, "b":2, "c":3, "d":4, "e":5, "f":9})
    [['f', 'a'], ['e', 'b'], ['d', 'c']]
    >>> partition(algorithm=bidirectional_balanced, numbins=2, items={"a":1, "b":2, "c":3, "d":4, "e":5, "f":9}, outputtype=out.Sums)
    array([14., 10.])
    """
    bins = outputtype.create_empty_bins(numbins)
    current_bin = 0
    current_direction = +1
    for item in sorted(items, key=map_item_to_value, reverse=True):
        bins.add_item_to_bin(item=item, value=map_item_to_value(item), bin_index=current_bin, inplace=True)
        current_bin += current_direction
        if current_bin > numbins-1:
            current_bin = numbins-1
            current_direction = -1
        if current_bin < 0:
            current_bin = 0
            current_direction = +1
    return outputtype.extract_output_from_bins(bins)




if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))


