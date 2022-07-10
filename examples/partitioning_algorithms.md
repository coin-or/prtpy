# Number-partitioning algorithms

## Approximate algorithms
`prtpy` supports single approximate algorithms. 
The simplest one is `greedy` - based on [Greedy number partitioning](https://en.wikipedia.org/wiki/Greedy_number_partitioning).
(also called: Longest Processing Time First).
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
[55606.0, 55606.0, 55606.0, 55606.0, 55606.0, 55605.0, 55605.0,
55605.0, 55605.0]
         0.24113940000000156 seconds
```



The *multifit* algorithm (Coffman et al, 1978) has a better asymptotic approximation ratio:

```python
start = perf_counter()
values = np.random.randint(1,10, 10000)
print(prtpy.partition(algorithm=prtpy.partitioning.multifit, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[5578.0, 5578.0, 5578.0, 5578.0, 5578.0, 5578.0, 5578.0, 5578.0,
5532.0]
         0.5636685999999997 seconds
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
[135.0, 135.0, 135.0, 136.0]
         0.3820400000000035 seconds
```



Another algorithm is dynamic programming. It is fast when there are few bins and the numbers are small, but quite slow otherwise.

```python
values = np.random.randint(1,10, 20)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.dynamic_programming, numbins=3, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[31.0, 30.0, 31.0]
         0.14241910000000502 seconds
```



The *complete greedy* algorithm (Korf, 1995) allows you to determine how much time you are willing to spend to find an optimal solution.

```python
start = perf_counter()
values = np.random.randint(1,1000, 10000)
print(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, numbins=9, items=values, outputtype=prtpy.out.Sums, time_limit=1))
print(f"\t {perf_counter()-start} seconds")
```

```
[554386.0, 554386.0, 554386.0, 554386.0, 554386.0, 554386.0, 554386.0,
554387.0, 554387.0]
         5.468529799999999 seconds
```



The *sequential number partitioning* algorithm (Korf, 2009) is an advanced optimal partitioning algorithm. Programmed by Shmuel and Jonathan.

```python
start = perf_counter()
values = np.random.randint(1,1000, 10)
print(prtpy.partition(algorithm=prtpy.partitioning.sequential_number_partitioning, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[187.0, 419.0, 490.0, 503.0, 531.0, 726.0, 874.0, 909.0, 920.0]
         8.094508399999995 seconds
```


---
Markdown generated automatically from [partitioning_algorithms.py](partitioning_algorithms.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-07-11.
