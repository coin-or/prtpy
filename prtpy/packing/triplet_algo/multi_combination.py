from typing import List, Tuple
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class MultiCombination:
    """
    Class for generating and indexing multi-combinations of items grouped by weight.

    It allows:
    - Counting how many unique combinations of size `k` exist.
    - Fetching a specific combination by index.

    Each item has a weight (group label), and items with the same weight are treated as indistinguishable.

    The core of the implementation is the `ctr` table, which is a dynamic programming
    table used to efficiently count and index combinations.

    Explanation of `ctr` table:

    - `ctr[k][b]` holds the number of ways to choose `k` items from the last `b` groups.

    - Base cases:
    - Choosing 0 items (k=0) always has 1 way regardless of groups.
    - Choosing items with zero groups available results in 0 ways.

    - For each number of items `k` and group count `b`,
    the value is computed by summing over possible counts `c` of items chosen
    from the current group (limited by group size and `k`),
    combining with ways to choose the remaining `k-c` items from previous groups.

    This dynamic programming table enables efficient querying and retrieval of
    combination counts and specific combinations.

    This approach efficiently counts all valid combinations without enumerating them explicitly.

    Example:
        >>> mc = MultiCombination()
        >>> mc.init(indices=[1, 2, 3, 4], weights=[1, 1, 2, 3])
        >>> mc.get_choice_count(2)
        4
        >>> mc.get_single_choice(2, 0)  # one valid combination of size 2
        [4, 3]

    """

    class Item:
        """
        Internal representation of an item group by weight.

        Attributes:
            weight (int): The weight/group ID of the items.
            indices (List[int]): The actual item identifiers in this group.

        Example:
            >>> item = MultiCombination.Item(weight=3)
            >>> item.indices = [10, 11]
            >>> repr(item)
            'Item(weight=3, indices=[10, 11])'
        """

        def __init__(self, weight: int):
            self.weight = weight
            self.indices: List[int] = []

        def __repr__(self):
            return f"Item(weight={self.weight}, indices={self.indices})"

    def __init__(self, indices: List[int] = [], weights: List[int] = []):
        """
        Initializes the MultiCombination with given item indices and weights.

        Args:
            indices (List[int]): List of item identifiers.
            weights (List[int]): Corresponding weights for each item (same length as indices).

        Raises:
            ValueError: If lengths of indices and weights differ.

        The method groups items by their weights (descending),
        and constructs the `ctr` table used for counting and indexing combinations.

        Example:
        >>> mc = MultiCombination()
        >>> mc.init([10, 11, 12], [1, 2, 1])
        >>> mc.get_choice_count(2)
        2
        """
        self.items: List[MultiCombination.Item] = []
        self.total_count = 0
        self.ctr: List[List[int]] = []

        self.init(indices, weights)

    def init(self, indices: List[int], weights: List[int]):
        """
        Initializes the MultiCombination object with given indices and their weights (group labels).

        Args:
            indices (List[int]): List of item identifiers.
            weights (List[int]): List of weights (group IDs), must be same length as `indices`.

        Raises:
            ValueError: If indices and weights are not the same length.

        Example:
            >>> mc = MultiCombination()
            >>> mc.init(indices=[10, 11, 12], weights=[1, 2, 1])
            >>> len(mc.items)
            2
            >>> mc.items[0].weight  # highest weight first
            2
            >>> mc.items[1].weight
            1
        """
        if len(indices) != len(weights):
            raise ValueError("Indices and weights must have the same size!")

        self.total_count = len(indices)

        weight_groups = defaultdict(list)
        for i, w in zip(indices, weights):
            weight_groups[w].append(i)

        self.items.clear()
        for weight in sorted(weight_groups.keys(), reverse=True):
            item = MultiCombination.Item(weight)
            item.indices = weight_groups[weight]
            self.items.append(item)

        K = self.total_count
        B = len(self.items)

        # Initialize ctr table
        self.ctr = [[0 for _ in range(B + 1)] for _ in range(K + 1)]
        for b in range(B + 1):
            self.ctr[0][b] = 1
        for k in range(1, K + 1):
            self.ctr[k][0] = 0

        for k in range(1, K + 1):
            for b in range(1, B + 1):
                index = B - b
                curr_max = min(len(self.items[index].indices), k)
                sum_val = 0
                for c in range(curr_max + 1):
                    sum_val += self.ctr[k - c][b - 1]
                self.ctr[k][b] = sum_val

    def get_choice_count(self, k: int) -> int:
        """
        Return the number of ways to choose `k` elements from the items.

        Args:
            k (int): Number of items to choose.

        Returns:
            int: Number of valid combinations of size `k`.

        Example:
            >>> mc = MultiCombination()
            >>> mc.init(indices=[1, 2, 3, 4], weights=[1, 1, 2, 3])
            >>> mc.get_choice_count(2)
            4
            >>> mc.get_choice_count(0)
            1
            >>> mc.get_choice_count(5)
            0
        """
        if k > self.total_count:
            logger.warning(f"Requested choice count for k={k} greater than total_count={self.total_count}")
            return 0
        count = self.ctr[k][len(self.items)]
        return count

    def get_single_choice(self, k: int, case_index: int) -> List[int]:
        """
        Get the `case_index`-th combination of `k` items from the items.

        Args:
            k (int): Number of items to select.
            case_index (int): Index of the desired combination (0-based).

        Returns:
            List[int]: List of selected indices.

        Raises:
            ValueError: If `case_index` is out of bounds.

        Example:
            >>> mc = MultiCombination()
            >>> mc.init(indices=[10, 11, 12], weights=[1, 2, 1])
            >>> mc.get_choice_count(2)
            2
            >>> mc.get_single_choice(2, 0)
            [11, 10]
            >>> mc.get_single_choice(2, 1)
            [10, 12]
        """

        max_index = self.ctr[k][len(self.items)]
        if not case_index < max_index:
            logger.error(f"Invalid case_index={case_index} >= max_index={max_index}")
            raise ValueError(f"Invalid case index: {case_index} not below {max_index}")

        result = []
        b = len(self.items)

        while k > 0:
            index = len(self.items) - b
            curr_max = min(len(self.items[index].indices), k)
            sum_val = 0
            for c in reversed(range(curr_max + 1)):
                current_count = self.ctr[k - c][b - 1]
                next_sum = sum_val + current_count
                if case_index < next_sum:
                    result.extend(self.items[index].indices[:c])
                    k -= c
                    b -= 1
                    case_index -= sum_val
                    break
                sum_val = next_sum
        return result
