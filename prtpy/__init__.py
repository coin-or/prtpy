import pathlib

HERE = pathlib.Path(__file__).parent
__version__ = (HERE / "VERSION").read_text().strip()

import prtpy.outputtypes as out
import prtpy.objectives as obj
from prtpy.binners import BinsArray, Binner, BinnerKeepingContents, BinnerKeepingSums, printbins

from prtpy.packing.adaptors import pack, pack_random_items
from prtpy.partitioning.adaptors import partition, partition_random_items, compare_algorithms, compare_algorithms_on_random_items


class partitioning:
    from prtpy.partitioning.complete_greedy import anytime as cg
    from prtpy.partitioning.complete_greedy import anytime as complete_greedy

    from prtpy.partitioning.dynamic_programming import optimal as dp
    from prtpy.partitioning.dynamic_programming import optimal as dynamic_programming

    from prtpy.partitioning.integer_programming import optimal as ilp
    from prtpy.partitioning.integer_programming import optimal as integer_programming
    from prtpy.partitioning.integer_programming_avg import optimal as ilp_avg

    from prtpy.partitioning.greedy import greedy
    from prtpy.partitioning.greedy import greedy as lpt
    from prtpy.partitioning.greedy import greedy as longest_processing_time

    from prtpy.partitioning.roundrobin import roundrobin
    from prtpy.partitioning.multifit import multifit as multifit

    # Samuel & Jonathan modules
    from prtpy.partitioning.karmarkar_karp import kk as karmarkar_karp      # Default implementation
    from prtpy.partitioning.karmarkar_karp import kk as kk

    from prtpy.partitioning.complete_karmarkar_karp import optimal as complete_karmarkar_karp     # Default implementation
    from prtpy.partitioning.complete_karmarkar_karp import optimal as ckk

    from prtpy.partitioning.sequential_number_partitioning import snp as sequential_number_partitioning
    from prtpy.partitioning.sequential_number_partitioning import snp

    from prtpy.partitioning.recursive_number_partitioning_korf import rnp as recursive_number_partitioning  # Default implementation
    from prtpy.partitioning.recursive_number_partitioning_korf import rnp as rnp

    # Eli Belkind module
    from prtpy.partitioning.cbldm import cbldm

    
partitioning.complete_greedy.__name__ = "complete-greedy"
partitioning.integer_programming.__name__ = "integer-programming"
partitioning.dynamic_programming.__name__ = "dynamic-programming"
partitioning.karmarkar_karp.__name__ = "karmarkar-karp"
partitioning.complete_karmarkar_karp.__name__ = "complete-karmarkar-karp"
partitioning.recursive_number_partitioning.__name__ = "recursive-number-partitioning"
partitioning.sequential_number_partitioning.__name__ = "sequential-number-partitioning"

class packing:
    from prtpy.packing.first_fit import online as first_fit, decreasing as first_fit_decreasing
    from prtpy.packing.first_fit import online as ff, decreasing as ffd
    from prtpy.packing.bin_completion import bin_completion

packing.first_fit.__name__ = "first-fit"
packing.first_fit_decreasing.__name__ = "first-fit-decreasing"

class covering:
    from prtpy.packing.greedy_covering import decreasing as decreasing
    from prtpy.packing.cflz_covering import twothirds as twothirds
    from prtpy.packing.cflz_covering import threequarters as threequarters
