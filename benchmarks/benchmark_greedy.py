import prtpy, benchmark, logging
from matplotlib import pyplot as plt
from partition_random import partition_random_items

benchmark.logger.setLevel(logging.INFO)
benchmark.logger.addHandler(logging.StreamHandler())

results = benchmark.find_max_solvable_size(
    partition_random_items,
    "numbins",
    range(1, 100),
    max_time_in_seconds=1,
    algorithm=prtpy.partitioning.greedy,
    numitems=100000,
    minvalue=1,
    maxvalue=100,
    objective=prtpy.obj.MaximizeSmallestSum,
    outputtype=prtpy.out.Sums,
)

results.plot(plt)
