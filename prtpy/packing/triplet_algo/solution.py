from typing import List
from .triplet import Triplet
import logging

logger = logging.getLogger(__name__)


class Solution:
    """
    Represents a collection of triplets forming a solution.

    Attributes:
        triplets (List[Triplet]): The list of triplets contained in the solution.

    Methods:
        add(t: Triplet): Adds a triplet to the solution.
        get_triplets() -> List[Triplet]: Returns the list of triplets.
        sort(): Sorts the triplets in descending order.
        to_string() -> str: Returns a concatenated string representation of sorted triplets.
    """

    def __init__(self):
        """
        Initializes an empty Solution instance.

        >>> sol = Solution()
        >>> sol.get_triplets()
        []
        """
        self.triplets: List[Triplet] = []

    def add(self, t: Triplet):
        """
        Adds a triplet to the solution.

        Args:
            t (Triplet): The triplet to add.

        >>> sol = Solution()
        >>> sol.add((1,2,3))
        >>> sol.get_triplets()
        [(1, 2, 3)]
        """
        self.triplets.append(t)

    def get_triplets(self) -> List[Triplet]:
        """
        Returns the list of triplets in the solution.

        Returns:
            List[Triplet]: The triplets stored in the solution.

        >>> sol = Solution()
        >>> sol.add((1,2,3))
        >>> sol.get_triplets()
        [(1, 2, 3)]
        """
        return self.triplets

    def sort(self):
        """
        Sorts the triplets in descending order (based on tuple comparison).

        >>> sol = Solution()
        >>> sol.add((1,2,3))
        >>> sol.add((4,5,6))
        >>> sol.sort()
        >>> sol.get_triplets()
        [(4, 5, 6), (1, 2, 3)]
        """
        logger.debug("Sorting triplets")
        self.triplets.sort(reverse=True)
        logger.debug("Triplets sorted")

    def to_string(self) -> str:
        """
        Returns a concatenated string representation of the sorted triplets.

        Returns:
            str: String concatenation of all triplets.

        >>> sol = Solution()
        >>> sol.add((1,2,3))
        >>> sol.add((4,5,6))
        >>> s = sol.to_string()
        >>> '(1, 2, 3)' in s and '(4, 5, 6)' in s
        True
        """
        self.sort()
        result = "".join(str(t) for t in self.triplets)
        return result

    def __str__(self):
        """Returns the string representation of the solution (same as to_string)."""
        return self.to_string()

    def __repr__(self):
        """Returns the official string representation."""
        return str(self)
