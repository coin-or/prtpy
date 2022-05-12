from dataclasses import dataclass
from typing import List

Partition = List[List[int]]


@dataclass
class PartitioningResult:
    """The result of performing a partitioning.
    Parameters
    ----------
    partition:
        The partition as a list of lists; each inner list is a part; a subset of the
        numbers being partitioned so that their disjoint union make up the full set.
    sizes:
        List containing the corresponding sums of the parts; that is, the i'th element
        is the sum of the i'th element of the partition.
    """

    partition: Partition
    sizes: List[int]