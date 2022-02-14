# Optimization objectives


```python
import prtpy
from prtpy.outputtypes import PartitionAndSums
from prtpy.objectives import MaximizeSmallestSum, MinimizeLargestSum, MinimizeDifference
dp = prtpy.exact.dynamic_programming
```



Most algorithms allow you to choose the optimization objective.
The following example is based on:
    Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
With these numbers, each objective yields a different partition.

```python
items = [46, 39, 27, 26, 16, 13, 10]
```



MinimizeLargestSum:

```python
print(prtpy.partition(algorithm=dp, numbins=3, items=items, outputtype=PartitionAndSums, objective=MinimizeLargestSum))
```

```
Bin #0: [46, 16], sum=62.0
Bin #1: [39, 13, 10], sum=62.0
Bin #2: [27, 26], sum=53.0
```



MaximizeSmallestSum:

```python
print(prtpy.partition(algorithm=dp, numbins=3, items=items, outputtype=PartitionAndSums, objective=MaximizeSmallestSum))
```

```
Bin #0: [46, 10], sum=56.0
Bin #1: [27, 16, 13], sum=56.0
Bin #2: [39, 26], sum=65.0
```



MinimizeDifference:

```python
print(prtpy.partition(algorithm=dp, numbins=3, items=items, outputtype=PartitionAndSums, objective=MinimizeDifference))
```

```
Bin #0: [39, 16], sum=55.0
Bin #1: [46, 13], sum=59.0
Bin #2: [27, 26, 10], sum=63.0
```



To define a custom objective, create an Objective object with a lamdba function, 
   describing the expression that should be *minimized*.

```python
MinimizeSmallestSum = prtpy.obj.Objective(
    lambda sums, are_sums_in_ascending_order=False: 
        sums[0] if are_sums_in_ascending_order else min(sums)
)
print(prtpy.partition(algorithm=dp, numbins=3, items=items, outputtype=PartitionAndSums, objective=MinimizeSmallestSum))
```

```
Bin #0: [], sum=0.0
Bin #1: [26, 13, 10], sum=49.0
Bin #2: [46, 39, 27, 16], sum=128.0
```



Some other useful objectives are:

```python
from prtpy.objectives import MaximizeKSmallestSums, MinimizeKLargestSums
```



MaximizeKSmallestSums:

```python
print(prtpy.partition(algorithm=dp, numbins=3, items=items, objective=MaximizeKSmallestSums(2), outputtype=PartitionAndSums))
```

```
Bin #0: [46, 16], sum=62.0
Bin #1: [39, 13, 10], sum=62.0
Bin #2: [27, 26], sum=53.0
```



MinimizeKLargestSums:

```python
print(prtpy.partition(algorithm=dp, numbins=3, items=items, objective=MinimizeKLargestSums(2), outputtype=PartitionAndSums))
```

```
Bin #0: [46, 10], sum=56.0
Bin #1: [27, 16, 13], sum=56.0
Bin #2: [39, 26], sum=65.0
```


---
Markdown generated automatically from [objectives.py](objectives.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-02-14.
