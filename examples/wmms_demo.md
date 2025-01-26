```python
""" 
Demonstrates weighted maximin-share computation.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import prtpy
import numpy as np


def weighted_maximin_share_partition(valuation:list, weights:list):
    """	
    Compute the of 1-of-c MMS of the given items, by the given valuation.
    :return (partition, part_values, maximin-share value)
    """
    if len(valuation)==0:
        raise ValueError("Valuation is empty")

    sums, lists = prtpy.partition(
        algorithm=prtpy.partitioning.integer_programming,
        numbins=len(weights),
        items=valuation,
        objective=prtpy.obj.MaximizeSmallestSum,
        outputtype=prtpy.out.PartitionAndSumsTuple,
        weights = weights
    )
    min_weighted_sum = min([s/w for s,w in zip(sums,weights)])
    wmms_values = [min_weighted_sum * w for w in weights]
    return (lists, list(sums), wmms_values)



def show_wmms_partition(valuation,weights):
	(partition, part_values, wmms_values) = weighted_maximin_share_partition(valuation, weights)
	print(f"WMMS partition = {partition}, values = {part_values}, wmms-values = {wmms_values}")

def wmms_demo(valuation,weights):
	print("\nValuation: ", valuation, "weights: ", weights)
	show_wmms_partition(valuation,weights)


import doctest
doctest.testmod()
wmms_demo([11.1,11,11,11,22], [1,1])   # WMMS partition = [[11, 11, 11], [11.1, 22]], values = [33.0, 33.1], wmms-values = [33.0, 33.0]
wmms_demo([11.1,11,11,11,22], [1,2])   # WMMS partition = [[22], [11.1, 11, 11, 11]], values = [22.0, 44.1], wmms-values = [22.0, 44.0]
wmms_demo([11.1,11,11,11,22], [10,2])   # WMMS partition = [[22], [11.1, 11, 11, 11]], values = [22.0, 44.1], wmms-values = [55.0, 11.0]
```

```

Valuation:  [11.1, 11, 11, 11, 22] weights:  [1, 1]
```

```
---------------------------------------------------------------------------TypeError
Traceback (most recent call last)Cell In[1], line 45
     43 import doctest
     44 doctest.testmod()
---> 45 wmms_demo([11.1,11,11,11,22], [1,1])   # WMMS partition =
[[11, 11, 11], [11.1, 22]], values = [33.0, 33.1], wmms-values =
[33.0, 33.0]
     46 wmms_demo([11.1,11,11,11,22], [1,2])   # WMMS partition =
[[22], [11.1, 11, 11, 11]], values = [22.0, 44.1], wmms-values =
[22.0, 44.0]
     47 wmms_demo([11.1,11,11,11,22], [10,2])   # WMMS partition =
[[22], [11.1, 11, 11, 11]], values = [22.0, 44.1], wmms-values =
[55.0, 11.0]
Cell In[1], line 40, in wmms_demo(valuation, weights)
     38 def wmms_demo(valuation,weights):
     39         print("\nValuation: ", valuation, "weights: ",
weights)
---> 40         show_wmms_partition(valuation,weights)
Cell In[1], line 35, in show_wmms_partition(valuation, weights)
     34 def show_wmms_partition(valuation,weights):
---> 35         (partition, part_values, wmms_values) =
weighted_maximin_share_partition(valuation, weights)
     36         print(f"WMMS partition = {partition}, values =
{part_values}, wmms-values = {wmms_values}")
Cell In[1], line 20, in weighted_maximin_share_partition(valuation,
weights)
     17 if len(valuation)==0:
     18     raise ValueError("Valuation is empty")
---> 20 sums, lists = prtpy.partition(
     21     algorithm=prtpy.partitioning.integer_programming,
     22     numbins=len(weights),
     23     items=valuation,
     24     objective=prtpy.obj.MaximizeSmallestSum,
     25     outputtype=prtpy.out.PartitionAndSumsTuple,
     26     weights = weights
     27 )
     28 min_weighted_sum = min([s/w for s,w in zip(sums,weights)])
     29 wmms_values = [min_weighted_sum * w for w in weights]
File
D:\Dropbox\papers\ElectricityDivision__Dinesh\Code\prtpy\prtpy\partitioning\adaptors.py:105,
in partition(algorithm, numbins, items, valueof, copies, outputtype,
**kwargs)
    103         raise TypeError(f"copies parameter {copies} is of
wrong type {type(copies)}")
    104 binner = outputtype.create_binner(valueof,copiesof)
--> 105 bins   = algorithm(binner, numbins, item_names, **kwargs)
    106 return outputtype.extract_output_from_binsarray(bins)
TypeError: optimal() got an unexpected keyword argument 'weights'
```


---
Markdown generated automatically from [wmms_demo.py](wmms_demo.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2025-01-26.
