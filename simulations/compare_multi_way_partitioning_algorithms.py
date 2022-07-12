""" 
Compare the performance of multi-way partitioning algorithms on uniformly-random integers
Aims to reproduce the results of Korf, Moffitt and Schreiber (2018), JACM paper.

Author: Erel Segal-Halevi
Since:  2022-07
"""

import prtpy

def partition_random_items(
    algorithm: callable,
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
    experiment = experiments_csv.Experiment("results/", "multi_way_partitioning_algorithms.csv", backup_folder=None)

    prt = prtpy.partitioning
    input_ranges = {
        "algorithm": [prt.integer_programming, prt.complete_greedy, prt.sequential_number_partitioning, prt.recursive_number_partitioning],
        "numbins": [3,4,5],
        "numitems": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50, 60, 70, 80, 90, 100],
        "bitsperitem": [8,10,12,16],
        "instance_id": range(10)
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=30)
    input_ranges = {
        "algorithm": [prt.integer_programming, prt.complete_greedy, prt.sequential_number_partitioning],
        "numbins": [6],
        "numitems": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50, 60, 70, 80, 90, 100],
        "bitsperitem": [8,10,12,16],
        "instance_id": range(10)
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=30)
