#' # Number-partitioning algorithms

#' ## Approximate algorithms
#' Currently, `prtpy` supports a single approximate algorithm - `greedy` - based on [Greedy number partitioning](https://en.wikipedia.org/wiki/Greedy_number_partitioning).
#' It is very fast, and attains very good result on random instances with many items and bins.

import prtpy
import numpy as np
from time import perf_counter

values = np.random.randint(1,10, 100000)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")


#' ## Exact algorithms
#' `prtpy` supports several exact algorithms. By far, the fastest of them uses integer linear programming.
#' It can handle a relatively large number of items when there are at most 4 bins.
values = np.random.randint(1,10, 100)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.integer_programming, numbins=4, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")

#' Another algorithm is dynamic programming. It is fast when there are few bins and the numbers are small, but quite slow otherwise.
values = np.random.randint(1,10, 20)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.dynamic_programming, numbins=3, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")

#' The *complete greedy* algorithm (Korf, 1995) is also available, though it is not very useful without further heuristics and optimizations.
start = perf_counter()
values = np.random.randint(1,10, 10)
print(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, numbins=2, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
