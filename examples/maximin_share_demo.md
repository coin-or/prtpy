```python
""" 
Demonstrates maximin-share computation.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import prtpy
from typing import Collection, Any
import numpy as np


def maximin_share_partition(c:int, valuation:list, items:Collection[Any]=None, numerator:int=1, **kwargs)->int:
    """	
    Compute the of 1-of-c MMS of the given items, by the given valuation.
    :return (partition, part_values, maximin-share value)

    >>> maximin_share_partition(c=1, valuation=[10,20,40,1])
    ([[0, 1, 2, 3]], [71.0], 71.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1])
    ([[0, 1, 3], [2]], [31.0, 40.0], 31.0)
    >>> int(maximin_share_partition(c=3, valuation=[10,20,40,1])[2])
    11
    >>> int(maximin_share_partition(c=4, valuation=[10,20,40,1])[2])
    1
    >>> int(maximin_share_partition(c=5, valuation=[10,20,40,1])[2])
    0
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], items=[1,2])
    ([[1], [2]], [20.0, 40.0], 20.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], copies=2)
    ([[0, 1, 2, 3], [0, 1, 2, 3]], [71.0, 71.0], 71.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], copies=[2,1,1,0])
    ([[0, 0, 1], [2]], [40.0, 40.0], 40.0)
    >>> maximin_share_partition(c=3, valuation=[10,20,40,1], numerator=2)
    ([[0, 3], [1], [2]], [11.0, 20.0, 40.0], 31.0)
    >>> maximin_share_partition(c=3, valuation=[10,20,40,1], numerator=2, additional_constraints=lambda sums:[sums[0]==0])
    ([[], [0, 1, 3], [2]], [0.0, 31.0, 40.0], 31.0)
    """
    if len(valuation)==0:
        raise ValueError("Valuation is empty")
    num_of_items = len(valuation)
    if items is None:
        items = list(range(num_of_items))

    bins:prtpy = prtpy.partition(
        algorithm=prtpy.partitioning.integer_programming,
        numbins=c,
        items=items,
        valueof=lambda item: valuation[item],
        objective=prtpy.obj.MaximizeKSmallestSums(numerator),
        outputtype=prtpy.out.PartitionAndSums,
        **kwargs
    )

    return (bins.bins, list(bins.sums), sum(sorted(bins.sums)[:numerator]))



def show_mms_partition(numerator, c, valuation):
	(partition, part_values, value) = maximin_share_partition(c, valuation, numerator=numerator)
	print(f"{numerator}-out-of-{c} partition = {partition}, values = {part_values}, min-value = {value}")

def mms_demo(c, valuation):
	print("\nValuation: ", valuation)
	show_mms_partition(1, c, valuation)
	show_mms_partition(2, c, valuation)

def items_to_values(partition, valuation):
	return [
			[valuation[x] for x in part]
			for part in partition
	]

def check_example(valuation, c:int, verbose=True):
	(partition1, part_values1, value1) = maximin_share_partition(c, valuation, numerator=1)
	(partition12, part_values12, value12) = maximin_share_partition(c, valuation, numerator=2, 
		additional_constraints=lambda bin_sums: [bin_sums[0]==value1])
	(partition2, part_values2, value2) = maximin_share_partition(c, valuation, numerator=2)
	# if part_values2[0] < part_values1[0] and sum(part_values2[0:2]) > sum(part_values1[0:2]):
	if verbose or (part_values2[0] < part_values12[0] and sum(part_values2[0:2]) > sum(part_values12[0:2])):
		print("Found interesting example!")
		print(f"Valuation = {valuation}")
		print(f"1-out-of-{c} partition = {items_to_values(partition1,valuation)}, values = {part_values1}, min-value = {value1}")
		print(f"Better 1-out-of-{c} partition = {items_to_values(partition12,valuation)}, values = {part_values12}, min-value = {value12}")
		print(f"2-out-of-{c} partition = {items_to_values(partition2,valuation)}, values = {part_values2}, min-value = {value2}")


def find_example():
	for c in range(3,4):
		for size in range(c+1,20):
			print(f"\nc = {c}, size = {size}")
			for i in range(1000):
				print(".", end="", flush=True)
				valuation = np.random.randint(1,20, size=size)
				check_example(valuation, c, verbose=False)



import doctest
doctest.testmod()
mms_demo(3, [5, 5, 5, 7, 7, 7, 11, 17, 23, 23, 23, 31, 31, 31, 65])  # The APS example of Babaioff, Ezra and Feige (2021), Lemma C.3.
mms_demo(3, [29, 29, 28, 16, 2])
# check_example([5,5,5,7,8,11], c=3, verbose=False)
# # check_example([7,7,7,10,11,16], c=3, verbose=True)
# # find_example()
```

```

Valuation:  [5, 5, 5, 7, 7, 7, 11, 17, 23, 23, 23, 31, 31, 31, 65]
1-out-of-3 partition = [[11, 14], [2, 3, 4, 5, 7, 8, 12], [0, 1, 6, 9,
10, 13]], values = [96.0, 97.0, 98.0], min-value = 96.0
2-out-of-3 partition = [[11, 14], [0, 2, 3, 6, 8, 9, 10], [1, 4, 5, 7,
12, 13]], values = [96.0, 97.0, 98.0], min-value = 193.0

Valuation:  [29, 29, 28, 16, 2]
1-out-of-3 partition = [[0], [2, 4], [1, 3]], values = [29.0, 30.0,
45.0], min-value = 29.0
2-out-of-3 partition = [[1], [0, 4], [2, 3]], values = [29.0, 31.0,
44.0], min-value = 60.0
```


---
Markdown generated automatically from [maximin_share_demo.py](maximin_share_demo.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-03-08.
