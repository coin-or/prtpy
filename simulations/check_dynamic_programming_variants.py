""" 
Check variants of Dynamic Programming Number Partitioning on uniformly-random integers.
Aims to reproduce the results of Korf, Moffitt and Schreiber (2018), JACM paper.

Author: Erel Segal-Halevi
Since:  2022-06
"""

from typing import Callable
import numpy as np, prtpy
from prtpy import objectives as obj

TIME_LIMIT=30

def partition_random_items(
    numitems: int,
    bitsperitem: int,
    instance_id: int, # dummy parameter, to allow multiple instances of the same run
    **kwargs
):
    items = np.random.randint(1, 2**bitsperitem-1, numitems, dtype=np.int64)
    sums = prtpy.partition(
        algorithm=prtpy.partitioning.dynamic_programming,
        numbins=2,
        items=items, 
        outputtype=prtpy.out.Sums,
        # time_limit=TIME_LIMIT,
        **kwargs
    )
    return {
        "diff": sums[-1]-sums[0]
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "check_dynamic_programming_variants_1.csv", backup_folder=None)

    prt = prtpy.partitioning
    input_ranges = {
        "numitems": [10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 35, 40, 45, 50],
        "bitsperitem": [4,8,12,16,20],
        "instance_id": range(10),
        "objective": [obj.MinimizeLargestSum, obj.MaximizeSmallestSum],
        "use_boolean_matrix": [False, True],
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=TIME_LIMIT)


"""

"""