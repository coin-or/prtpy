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
    numbins: int,
    **kwargs
):
    diff = prtpy.partition_random_items(
        numitems, bitsperitem,
        algorithm=algorithm,
        numbins=numbins,
        outputtype=prtpy.out.Difference,
        # time_limit=TIME_LIMIT,
        **kwargs
    )
    return {"diff": diff}


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "rnp_variants_1.csv", backup_folder=None)

    prt = prtpy.partitioning
    input_ranges = {
        "numitems": [10, 12, 14, 16, 18, 20, 22, 24, 26, 30],
        "bitsperitem": [8, 12, 16, 20, 24, 32],
        "algorithm": [prt.recursive_number_partitioning_kg, prt.recursive_number_partitioning_sy],
        "numbins": [2, 3, 4],
        "instance_id": range(10),
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=TIME_LIMIT)


"""
RESULTS: rnp_kg is faster than rnp_sy.
"""