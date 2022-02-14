# Algorithms

```python
import prtpy
import numpy as np
from time import perf_counter
```



## Approximate algorithms
Currently, `prtpy` supports a single approximate algorithm - `greedy` - based on [Greedy number partitioning](https://en.wikipedia.org/wiki/Greedy_number_partitioning).
It is very fast, and attains very good result on random instances with many items and bins.

```python
values = np.random.randint(1,10, 100000)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.approx.greedy, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[55566. 55566. 55566. 55566. 55566. 55565. 55565. 55565. 55565.]
         0.2700902999999997 seconds
```



## Exact algorithms
Currently, `prtpy` supports several exact algorithms. By far, the fastest of them uses integer linear programming.
It can handle a relatively large number of items when there are at most 3 bins.

```python
values = np.random.randint(1,10, 100)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.exact.integer_programming, numbins=4, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[114. 118. 123. 126.]
         1.1145717 seconds
```



You can choose another solver. For example, if you install the XPRESS solver, you can try the following (it will return an error if XPRESS is not installed):

```python
# import cvxpy
# print(prtpy.partition(algorithm=prtpy.exact.integer_programming, numbins=4, items=values, outputtype=prtpy.out.Sums, solver=cvxpy.XPRESS))
```



Another algorithm is dynamic programming. It is fast when there are few bins and the numbers are small, but quite slow otherwise.

```python
values = np.random.randint(1,10, 20)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.exact.dynamic_programming, numbins=3, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
(27, 26, 27)
         0.034918799999999806 seconds
```



The *complete greedy* algorithm (Korf, 1995) is also available, though it is not very useful without further heuristics and optimizations.

```python
start = perf_counter()
values = np.random.randint(1,10, 10)
print(prtpy.partition(algorithm=prtpy.exact.complete_greedy, numbins=2, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[25. 26.]
         0.01448740000000015 seconds
```


---
Markdown generated automatically from [algorithms.py](algorithms.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-02-14.
