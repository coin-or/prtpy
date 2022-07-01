""" 
Check partitioning algorithms on uniformly-random integers.
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
    instance_id: int = 0,
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

    input_ranges = {
        # "algorithm": [prtpy.partitioning.greedy, prtpy.partitioning.roundrobin, prtpy.partitioning.multifit],
        "algorithm": [prtpy.partitioning.ilp, prtpy.partitioning.complete_greedy],
        "numbins": [2],
        "numitems": [10,20,30,40,50,60,70,80],
        "bitsperitem": [16,32,48],
        "instance_id": range(10)
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=1)
