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
[55505.0, 55504.0, 55504.0, 55504.0, 55504.0, 55504.0, 55504.0,
55504.0, 55504.0]
         0.2455579000088619 seconds
```



The *multifit* algorithm (Coffman et al, 1978) has a better asymptotic approximation ratio:

```python
start = perf_counter()
values = np.random.randint(1,10, 10000)
print(prtpy.partition(algorithm=prtpy.partitioning.multifit, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[5592.0, 5592.0, 5592.0, 5592.0, 5592.0, 5592.0, 5592.0, 5592.0,
5547.0]
         0.3740479999978561 seconds
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
[129.0, 129.0, 130.0, 130.0]
         0.3462842000008095 seconds
```



Another algorithm is dynamic programming. It is fast when there are few bins and the numbers are small, but quite slow otherwise.

```python
values = np.random.randint(1,10, 20)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.dynamic_programming, numbins=3, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[34.0, 35.0, 34.0]
         0.19563360000029206 seconds
```



The *complete greedy* algorithm (Korf, 1995) allows you to determine how much time you are willing to spend to find an optimal solution.

```python
start = perf_counter()
values = np.random.randint(1,1000, 100)
print(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, numbins=9, items=values, outputtype=prtpy.out.Sums, time_limit=1))
print(f"\t {perf_counter()-start} seconds")
```

```
[5819.0, 5822.0, 5827.0, 5833.0, 5843.0, 5852.0, 5871.0, 5875.0,
5876.0]
         1.002595799989649 seconds
```



The *sequential number partitioning* algorithm (Korf, 2009) is an advanced optimal partitioning algorithm. Programmed by Shmuel and Jonathan.

```python
start = perf_counter()
values = np.random.randint(1,100, 10)
print(prtpy.partition(algorithm=prtpy.partitioning.sequential_number_partitioning, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[18.0, 19.0, 25.0, 33.0, 61.0, 65.0, 72.0, 90.0, 99.0]
         50.17736359999981 seconds
```


---
Markdown generated automatically from [partitioning_algorithms.py](partitioning_algorithms.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2025-01-26.
