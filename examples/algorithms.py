#' # Algorithms
import prtpy
import numpy as np
from time import perf_counter

#' ## Approximate algorithms
#' Currently, `prtpy` supports a single approximate algorithm - `greedy` - based on [Greedy number partitioning](https://en.wikipedia.org/wiki/Greedy_number_partitioning).
#' It is very fast, and attains very good result on random instances with many items and bins.
values = np.random.randint(1,10, 100000)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.approx.greedy, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")


#' ## Exact algorithms
#' `prtpy` supports several exact algorithms. By far, the fastest of them uses integer linear programming.
#' It can handle a relatively large number of items when there are at most 4 bins.
values = np.random.randint(1,10, 100)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.exact.integer_programming, numbins=4, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")

#' The default solver is CBC. You can choose another, potentially faster solver. 
#' For example, if you install the XPRESS solver, you can try the following (it will return an error if XPRESS is not installed):
# import cvxpy
# print(prtpy.partition(algorithm=prtpy.exact.integer_programming, numbins=4, items=values, outputtype=prtpy.out.Sums, solver=cvxpy.XPRESS))

#' Another algorithm is dynamic programming. It is fast when there are few bins and the numbers are small, but quite slow otherwise.
values = np.random.randint(1,10, 20)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.exact.dynamic_programming, numbins=3, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")

#' The *complete greedy* algorithm (Korf, 1995) is also available, though it is not very useful without further heuristics and optimizations.
start = perf_counter()
values = np.random.randint(1,10, 10)
print(prtpy.partition(algorithm=prtpy.exact.complete_greedy, numbins=2, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
