
from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins
import heapq
from itertools import count
from prtpy.bins import BinsKeepingContents, BinsKeepingSums


def _argsort(seq: List[int]) -> List[int]:
    return sorted(range(len(seq)), key=seq.__getitem__)


def kk(bins: Bins, items: List[any], valueof: Callable=lambda x: x) -> Bins:
    partitions = []  # : List[(int, int, Partition, List[int])]
    heap_count = count()  # To avoid ambiguity in heap

    #  initial a heap
    for item in items:
        this_partition = []

        for n in range(bins.num - 1):
            this_partition.append([])
        this_partition.append([valueof(item)])

        this_sizes = [0] * (bins.num - 1) + [valueof(item)]  # : List[int]

        heapq.heappush(
            partitions, (-valueof(item), next(heap_count), this_partition, this_sizes)
        )

    for k in range(len(items) - 1):
        _, _, p1, p1_sums = heapq.heappop(partitions)
        _, _, p2, p2_sums = heapq.heappop(partitions)

        new_sizes = [p1_sums[j] + p2_sums[bins.num - j - 1] for j in range(bins.num)]
        new_partition = [p1[j] + p2[bins.num - j - 1] for j in range(bins.num)]

        indices = _argsort(new_sizes)
        new_sizes = [new_sizes[i] for i in indices]
        new_partition = [new_partition[i] for i in indices]
        diff = new_sizes[-1] - new_sizes[0]

        heapq.heappush(partitions, (-diff, next(heap_count), new_partition, new_sizes))

    _, _, final_partition, final_sums = partitions[0]

    for ibin in range(bins.num):
        for item in final_partition[ibin]:
            bins.add_item_to_bin(item, ibin)

    return bins


if __name__ == '__main__':
    from prtpy import partition

    print( partition(algorithm=kk, numbins=2, items={"a":4, "b":5, "c":6, "d":7, "e":8}) )
    # print(final_partition)
    # print(final_sums)
