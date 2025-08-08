from typing import Tuple
import logging

logger = logging.getLogger("trialgo.triplet")


class Triplet:
    """
    A class representing a triplet of integers, stored in descending order.

    Attributes:
        t (Tuple[int, int, int]): The ordered triplet (a, b, c) with a >= b >= c.

    Example:
        >>> t = Triplet(3, 1, 2)
        >>> t.get()
        (3, 2, 1)
        >>> t.a()
        3
        >>> t.b()
        2
        >>> t.c()
        1
        >>> t.sum()
        6
        >>> str(t)
        '{3, 2, 1}'
    """

    def __init__(self, v1: int, v2: int, v3: int):
        """
        Initialize the Triplet with three integers. The triplet is sorted in descending order.

        Args:
            v1 (int): First value.
            v2 (int): Second value.
            v3 (int): Third value.
        """
        self.set(v1, v2, v3)

    def get(self) -> Tuple[int, int, int]:
        """
        Return the current triplet.

        Returns:
            Tuple[int, int, int]: The triplet (a, b, c).

        >>> Triplet(5, 2, 4).get()
        (5, 4, 2)
        """
        return self.t

    def a(self) -> int:
        """
        Return the first (largest) value of the triplet.

        >>> Triplet(1, 9, 3).a()
        9
        """
        return self.t[0]

    def b(self) -> int:
        """
        Return the second value of the triplet.

        >>> Triplet(1, 9, 3).b()
        3
        """
        return self.t[1]

    def c(self) -> int:
        """
        Return the third (smallest) value of the triplet.

        >>> Triplet(1, 9, 3).c()
        1
        """
        return self.t[2]

    def sum(self) -> int:
        """
        Return the sum of all three values in the triplet.

        >>> Triplet(1, 2, 3).sum()
        6
        """
        return self.a() + self.b() + self.c()

    def __lt__(self, other: "Triplet") -> bool:
        """
        Less-than comparison based on lexicographical order of the triplet.

        >>> Triplet(3, 2, 1) < Triplet(4, 1, 1)
        True
        """
        return (self.a(), self.b(), self.c()) < (other.a(), other.b(), other.c())

    def set(self, v1: int, v2: int, v3: int):
        """
        Set the triplet values by sorting the input in descending order.

        Args:
            v1 (int): First value.
            v2 (int): Second value.
            v3 (int): Third value.

        >>> t = Triplet(0, 0, 0)
        >>> t.set(5, 1, 2)
        >>> t.get()
        (5, 2, 1)
        """
        values = sorted([v1, v2, v3], reverse=True)
        self.set_ordered(values[0], values[1], values[2])

    def set_ordered(self, a: int, b: int, c: int):
        """
        Set the triplet values directly, assuming they are already in descending order.

        Args:
            a (int): Largest value.
            b (int): Middle value.
            c (int): Smallest value.

        >>> t = Triplet(0, 0, 0)
        >>> t.set_ordered(7, 5, 2)
        >>> t.get()
        (7, 5, 2)
        """
        self.t: Tuple[int, int, int] = (a, b, c)

    def __str__(self) -> str:
        """
        Return a string representation of the triplet.

        >>> str(Triplet(3, 5, 4))
        '{5, 4, 3}'
        """
        return f"{{{self.a()}, {self.b()}, {self.c()}}}"

    def __repr__(self) -> str:
        """
        Return the official string representation of the triplet.

        >>> repr(Triplet(3, 2, 1))
        '{3, 2, 1}'
        """
        return str(self)
