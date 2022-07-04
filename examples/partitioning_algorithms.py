#' # Number-partitioning algorithms

#' ## Approximate algorithms
#' `prtpy` supports single approximate algorithms. 
#' The simplest one is `greedy` - based on [Greedy number partitioning](https://en.wikipedia.org/wiki/Greedy_number_partitioning).
#' (also called: Longest Processing Time First).
#' It is very fast, and attains very good result on random instances with many items and bins.

import prtpy
import numpy as np
from time import perf_counter

values = np.random.randint(1,10, 100000)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")

#' The *multifit* algorithm (Coffman et al, 1978) has a better asymptotic approximation ratio:
start = perf_counter()
values = np.random.randint(1,10, 10000)
print(prtpy.partition(algorithm=prtpy.partitioning.multifit, numbins=9, items=values, outputtype=prtpy.out.Sums))
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

#' The *complete greedy* algorithm (Korf, 1995) allows you to determine how much time you are willing to spend to find an optimal solution.
start = perf_counter()
values = np.random.randint(1,1000, 10000)
print(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, numbins=9, items=values, outputtype=prtpy.out.Sums, time_limit=1))
print(f"\t {perf_counter()-start} seconds")
