
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
    for item in items:  # we change from iter on range to iter on items
        this_partition = []  #: Partition

        for n in range(bins.num - 1):
            this_partition.append([])
        this_partition.append([valueof(item)])
        this_sizes = [0] * (bins.num - 1) + [valueof(item)]  # : List[int]
        heapq.heappush(
            partitions, (-valueof(item), next(heap_count), this_partition, this_sizes)
        )
    print(partitions)

    for k in range(len(items) - 1):
        _, _, p1, p1_sum = heapq.heappop(partitions)
        _, _, p2, p2_sum = heapq.heappop(partitions)
        new_sizes = [p1_sum[j] + p2_sum[bins.num - j - 1] for j in range(bins.num)]
        new_partition = [p1[j] + p2[bins.num - j - 1] for j in range(bins.num)]

        indices = _argsort(new_sizes)
        new_sizes = [new_sizes[i] for i in indices]
        new_partition = [new_partition[i] for i in indices]
        diff = new_sizes[-1] - new_sizes[0]

        heapq.heappush(partitions, (-diff, next(heap_count), new_partition, new_sizes))

    _, _, final_partition, final_sums = partitions[0]

    # print(partitions)

    return final_partition, final_sums


if __name__ == '__main__':
    final_partition, final_sums = kk(BinsKeepingContents(2), items=[4, 5, 6, 7, 8,9])
    # print(final_partition)
    # print(final_sums)
