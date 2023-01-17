""" 
Compare the performance of number-partitioning algorithms on uniformly-random integers.
Aims to reproduce the results of Korf, Moffitt and Schreiber (2018), JACM paper.

Author: Erel Segal-Halevi
Since:  2022-05
"""

from typing import Callable
import numpy as np, prtpy


def partition_random_items(
    algorithm: Callable,
    numbins: int,
    numitems: int,
    bitsperitem: int,
    instance_id: int = 0, # dummy parameter, to allow multiple instances of the same run
):
    items = np.random.randint(1, 2**bitsperitem-1, numitems, dtype=np.int64)
    sums = prtpy.partition(
        algorithm=algorithm,
        numbins=numbins,
        items=items, 
        outputtype=prtpy.out.Sums,
    )
    max_sums = max(sums)
    min_sums = min(sums)
    return {
        "diff": (max_sums-min_sums)/max_sums,
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "partition_uniform_integers.csv", backup_folder=None)

    prt = prtpy.partitioning
    # input_ranges = {
    #     "algorithm": [prt.integer_programming, prt.complete_greedy, prt.dynamic_programming, prt.ckk],
    #     "numbins": [2],
    #     "numitems": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40, 50, 60, 70, 80, 90, 100],
    #     "bitsperitem": [16,32,48],
    #     "instance_id": range(10)
    # }
    input_ranges = {
        "algorithm": [prt.complete_greedy],
        "numbins": [2],
        "numitems": [60, 70, 80, 90, 100],
        "bitsperitem": [32,48],
        "instance_id": range(10)
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=3000)
