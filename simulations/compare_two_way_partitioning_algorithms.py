""" 
Compare the performance of two-way partitioning algorithms on uniformly-random integers
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
    diff = prtpy.partition_random_items(
        numitems=numitems, 
        bitsperitem=bitsperitem,
        algorithm=algorithm,
        numbins=numbins,
        outputtype=prtpy.out.Difference,
    )
    return {
        "diff": diff,
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "two_way_partitioning_algorithms_1.csv", backup_folder=None)

    prt = prtpy.partitioning
    input_ranges = {
        "algorithm": [prt.integer_programming, prt.complete_greedy, prt.complete_karmarkar_karp, prt.dynamic_programming],
        "numbins": [2],
        "numitems": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50, 60, 70, 80, 90, 100],
        "bitsperitem": [16,24,32,48],
        "instance_id": range(10)
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=30)
