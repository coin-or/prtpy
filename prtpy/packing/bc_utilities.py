"""
These functions are being used by the Bin-Completion algorithm for solving the bin packing problem.
See "bin_completion.py" for more details.
"""

from typing import List
from prtpy import outputtypes as out, Bins, BinsKeepingContents


def l2_lower_bound(binsize: float, items: List) -> float:
    copy_items = items.copy()

    copy_items.sort(reverse=True)

    total_sum = sum(copy_items)
    estimated_waste = 0
    capacity = binsize

    for x in copy_items:
        r = capacity - x
        smaller_elements = []
        for i in range(len(copy_items) - 1, copy_items.index(x), -1):
            if copy_items[i] > r:
                break
            smaller_elements.append(copy_items[i])

        s = sum(smaller_elements)
        if s == r:
            for element in smaller_elements:
                copy_items.remove(element)
            capacity = binsize
        elif s < r:
            estimated_waste += r - s
            for element in smaller_elements:
                copy_items.remove(element)
            capacity = binsize
        else:
            for element in smaller_elements:
                copy_items.remove(element)
            capacity = binsize - (s - r)

    return (estimated_waste + total_sum) / binsize


class NodeBin:
    def __init__(self, items: List, level: int = 0, prev=None):
        self.items = items.copy()
        self.prev = prev
        self.next_bins = BinsKeepingContents()
        self.level = level


