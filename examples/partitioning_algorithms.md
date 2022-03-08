# Number-partitioning algorithms

## Approximate algorithms
Currently, `prtpy` supports a single approximate algorithm - `greedy` - based on [Greedy number partitioning](https://en.wikipedia.org/wiki/Greedy_number_partitioning).
It is very fast, and attains very good result on random instances with many items and bins.


```python
import prtpy
import numpy as np
from time import perf_counter

values = np.random.randint(1,10, 100000)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[55530. 55530. 55530. 55530. 55530. 55530. 55530. 55530. 55529.]
         0.28508469999999875 seconds
```



## Exact algorithms
`prtpy` supports several exact algorithms. By far, the fastest of them uses integer linear programming.
It can handle a relatively large number of items when there are at most 4 bins.

```python
values = np.random.randint(1,10, 100)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.integer_programming, numbins=4, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[125. 126. 127. 130.]
         0.3779532000000003 seconds
```



Another algorithm is dynamic programming. It is fast when there are few bins and the numbers are small, but quite slow otherwise.

```python
values = np.random.randint(1,10, 20)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.dynamic_programming, numbins=3, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
(28, 27, 28)
         0.03369320000000009 seconds
```



The *complete greedy* algorithm (Korf, 1995) is also available, though it is not very useful without further heuristics and optimizations.

```python
start = perf_counter()
values = np.random.randint(1,10, 10)
print(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, numbins=2, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[18. 19.]
         0.009161999999999892 seconds
```


---
Markdown generated automatically from [partitioning.py](partitioning.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-03-08.
