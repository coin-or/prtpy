""" 
Compare the performance of variants of the Karmarkar-Karp Number Partitioning algorithm uniformly-random integers.

Author: Erel Segal-Halevi
Since:  2022-07
"""

import numpy as np, prtpy
from prtpy import objectives as obj
from typing import Callable

TIME_LIMIT=30

def partition_random_items(
    numitems: int,
    bitsperitem: int,
    algorithm: Callable,
    instance_id: int, # dummy parameter, to allow multiple instances of the same run
    **kwargs
):
    diff = prtpy.partition_random_items(
        numitems, bitsperitem,
        algorithm=algorithm,
        numbins=2,
        outputtype=prtpy.out.Difference,
        # time_limit=TIME_LIMIT,
        **kwargs
    )
    return {"diff": diff}


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "karmarkar_karp_variants_1.csv", backup_folder=None)

    prt = prtpy.partitioning
    # input_ranges = {
    #     "numitems": [10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 35, 40, 45, 50, 60, 80, 100, 150, 200],
    #     "bitsperitem": [4, 8, 12, 16, 20],
    #     "algorithm": [prt.karmarkar_karp_kg, prt.karmarkar_karp_sy, prt.complete_karmarkar_karp_kg, prt.complete_karmarkar_karp_sy],
    #     "instance_id": range(10),
    # }
    # experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=TIME_LIMIT)

    input_ranges = {
        "numitems": [10, 12, 14, 16, 18, 20],
        "bitsperitem": [32],
        "algorithm": [prt.complete_karmarkar_karp_kg, prt.complete_karmarkar_karp_sy],
        "instance_id": range(10),
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=TIME_LIMIT)


"""
RESULTS: 
  * karmarkar_karp_sy is much faster than karmarkar_karp_kg; its runtime is approximately linear in the number of items.
    The runtime of karmarkar_karp_kg increases super-linearly with the number of items.
  * complete_karmarkar_karp_sy is slightly faster than complete_karmarkar_kg for at most 16 bits, but slightly slower for 20-32 bits.
"""