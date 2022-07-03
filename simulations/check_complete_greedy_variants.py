""" 
Check variants of Complete Greedy algorithm on uniformly-random integers.
Aims to reproduce the results of Korf, Moffitt and Schreiber (2018), JACM paper.

Author: Erel Segal-Halevi
Since:  2022-06
"""

from typing import Callable
import numpy as np, prtpy
from prtpy.partitioning.complete_greedy_2 import optimal as CGA
from prtpy import objectives as obj

def partition_random_items(
    numitems: int,
    bitsperitem: int,
    instance_id: int, # dummy parameter, to allow multiple instances of the same run
    **kwargs
):
    items = np.random.randint(1, 2**bitsperitem-1, numitems, dtype=np.int64)
    sums = prtpy.partition(
        algorithm=CGA,
        numbins=2,
        items=items, 
        outputtype=prtpy.out.Sums,
        **kwargs
    )
    return {
        "diff": sums[-1]-sums[0]
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "check_complete_greedy_variants.csv", backup_folder=None)

    prt = prtpy.partitioning
    input_ranges = {
        "numitems": [10,15,20,25,30,35,40,50,60,70,80,90,100],
        "bitsperitem": [16,32,48],
        "instance_id": range(10),
        "objective": [obj.MaximizeSmallestSum, obj.MinimizeLargestSum],
        "use_lower_bound": [False, True],
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=30)
