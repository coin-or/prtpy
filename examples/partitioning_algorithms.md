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
[55605.0, 55604.0, 55604.0, 55604.0, 55604.0, 55604.0, 55604.0,
55604.0, 55604.0]
         0.23440219999999812 seconds
```



The *multifit* algorithm (Coffman et al, 1978) has a better asymptotic approximation ratio:

```python
start = perf_counter()
values = np.random.randint(1,10, 10000)
print(prtpy.partition(algorithm=prtpy.partitioning.multifit, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[5567.0, 5567.0, 5567.0, 5567.0, 5567.0, 5567.0, 5567.0, 5567.0,
5520.0]
         0.4883513999999991 seconds
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
[118.0, 119.0, 119.0, 119.0]
         0.18726790000000193 seconds
```



Another algorithm is dynamic programming. It is fast when there are few bins and the numbers are small, but quite slow otherwise.

```python
values = np.random.randint(1,10, 20)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.dynamic_programming, numbins=3, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[35.0, 35.0, 34.0]
         0.15508069999999918 seconds
```



The *complete greedy* algorithm (Korf, 1995) allows you to determine how much time you are willing to spend to find an optimal solution.

```python
start = perf_counter()
values = np.random.randint(1,1000, 10000)
print(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, numbins=9, items=values, outputtype=prtpy.out.Sums, time_limit=1))
print(f"\t {perf_counter()-start} seconds")
```

```
---------------------------------------------------------------------------TypeError
Traceback (most recent call last)Input In [1], in <module>
      1 start = perf_counter()
      2 values = np.random.randint(1,1000, 10000)
----> 3
print(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy,
numbins=9, items=values, outputtype=prtpy.out.Sums, time_limit=1))
      4 print(f"\t {perf_counter()-start} seconds")
File
d:\dropbox\papers\electricitydivision__dinesh\code\prtpy\prtpy\partitioning\adaptors.py:82,
in partition(algorithm, numbins, items, valueof, outputtype, **kwargs)
     80 binner = outputtype.create_binner(valueof)
     81 bins   = algorithm(binner, numbins, item_names, **kwargs)
---> 82 return outputtype.extract_output_from_binsarray(bins)
File
d:\dropbox\papers\electricitydivision__dinesh\code\prtpy\prtpy\outputtypes.py:47,
in Sums.extract_output_from_binsarray(cls, bins)
     45 except:
     46     sums = bins          # If it fails, it means that bins is
a singleton: sums.
---> 47 return cls.extract_output_from_sums(sums)
File
d:\dropbox\papers\electricitydivision__dinesh\code\prtpy\prtpy\outputtypes.py:38,
in Sums.extract_output_from_sums(cls, sums)
     36 @classmethod
     37 def extract_output_from_sums(cls, sums: List[float]) -> List:
---> 38     return list(sums)
TypeError: 'NoneType' object is not iterable
```



The *sequential number partitioning* algorithm (Korf, 2009) is an advanced optimal partitioning algorithm. Programmed by Shmuel and Jonathan.

```python
start = perf_counter()
values = np.random.randint(1,1000, 10)
print(prtpy.partition(algorithm=prtpy.partitioning.sequential_number_partitioning, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[254.0, 299.0, 403.0, 496.0, 553.0, 579.0, 828.0, 937.0, 943.0]
         10.203577499999998 seconds
```


---
Markdown generated automatically from [partitioning_algorithms.py](partitioning_algorithms.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-07-11.
