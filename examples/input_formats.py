#' # Input formats

#' You can send the input as a list of values:
import prtpy
values = [4, 5, 5, 6, 7, 8, 8]
print(prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=2, items=values))

#' You can also send the input as a dict mapping items to values; in this case, the partition will show the items:
map_items_to_values = {"a": 4, "b": 5, "b2": 5, "c": 6, "d": 7, "e": 8, "e2": 8}
print(prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=2, items=map_items_to_values))

#' For experiments, you can use a numpy random matrix:
import numpy as np

values = np.random.randint(1, 100, 20)
print(values)
print(prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=3, items=values))
