import prtpy, benchmark, logging
from matplotlib import pyplot as plt
from partition_uniform_integers import partition_random_items

benchmark.logger.setLevel(logging.INFO)
benchmark.logger.addHandler(logging.StreamHandler())

results = benchmark.find_max_solvable_size(
    partition_random_items,
    "numitems",
    range(1, 101, 10),
    max_time_in_seconds=10,
    algorithm=prtpy.partitioning.greedy,
    numbins=4,
    bitsperitem=7,
)

results.plot(plt)
