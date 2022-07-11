""" 
Compare the performance of variants of Complete Greedy algorithm on uniformly-random integers.
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
    use_dynamic_programming: bool,
    **kwargs
):
    items = np.random.randint(1, 2**bitsperitem-1, numitems, dtype=np.int64)
    if use_dynamic_programming:
        sums = prtpy.partition(
            algorithm=prtpy.partitioning.dynamic_programming,
            numbins=2,
            items=items, 
            outputtype=prtpy.out.Sums,
        )
    else:
        sums = prtpy.partition(
            algorithm=prtpy.partitioning.complete_greedy,
            numbins=2,
            items=items, 
            outputtype=prtpy.out.Sums,
            time_limit=TIME_LIMIT,
            **kwargs
    )
    return {
        "diff": sums[-1]-sums[0]
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "complete_greedy_variants_8.csv", backup_folder=None)

    prt = prtpy.partitioning
    input_ranges = {
        "numitems": [10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 35, 40, 45, 50],
        "bitsperitem": [16,32,48],
        "instance_id": range(10),
        "objective": [obj.MinimizeLargestSum, obj.MaximizeSmallestSum],
        "use_lower_bound": [False, True],
        "use_fast_lower_bound": [False, True],
        "use_set_of_seen_states": [False, True],
        "use_dynamic_programming": [False],
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=TIME_LIMIT)

    input_ranges = {
        "numitems": [10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 35, 40, 45, 50],
        "bitsperitem": [16,32,48],
        "instance_id": range(10),
        "objective": [obj.MinimizeLargestSum, obj.MaximizeSmallestSum],
        "use_lower_bound": [None],
        "use_fast_lower_bound": [None],
        "use_set_of_seen_states": [None],
        "use_dynamic_programming": [True],
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=TIME_LIMIT)


"""
complete_greedy_variants_3: minimize largest sum objective; compare lower bound, heuristic 2, and heuristic 3. 
  --  Heuristic 2 (use_fast_lower_bound) is the best, then lower bound; Heuristic 3 is not useful.

complete_greedy_variants_4: maximize smallest sum objective; compare lower bound and heuristic 2. 
  -- Heuristic 2 (use_fast_lower_bound) is the best, then lower bound.
  -- But lower-bound is very useful for 16 bits.

complete_greedy_variants_5: maximize smallest sum and minimize largest sum; stopping when an optimal solution is found.
  -- Both objectives have similar performance.
  -- Heuristic 3 harms performance.

complete_greedy_variants_6: compare use_lower_bound to use_set_of_seen_states, when fast_lower_bound is used.
  -- with 16 bits, both of them are not needed.
  -- with 32 bits, use_set_of_seen_states is slightly better.
  -- with 48 bits, use_lower_bound is slightly better.

complete_greedy_variants_7: compare all lower bounds with dynamic programming.
  -- set_of_seen_states is useful only with 16 bits.
  -- fast_lower_bound is best.

complete_greedy_variants_8: same as 7, but a different implementation, using a binner.
  -- fast_lower_bound alone is best.
  -- dynamic programming is worst.

"""