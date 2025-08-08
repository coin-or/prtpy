from typing import List
import logging

logger = logging.getLogger(__name__)


class Problem:
    """
    A class representing a triplet-based weight partitioning problem.

    Attributes:
        weights (List[int]): List of positive integer weights.
        binsize (int): Optional value used for validating triplet sums.

    Example usage:

        >>> p = Problem()
        >>> p.init([3, 3, 6], 12)
        >>> p.get_weights()
        [3, 3, 6]
        >>> p.get_n()
        1
        >>> p.to_string()
        '[3,3,6]'
    """

    def __init__(self):
        """
        Initialize an empty Problem instance.
        """
        self.weights: List[int] = []
        logger.debug("Problem instance created")

    def read(self, path: str):
        """
        Read weights from a plain-text file where each line contains one integer.

        Args:
            path (str): Path to the input file.

        Raises:
            RuntimeError: If the file is not found or the weights are invalid.
        """
        logger.info("Reading problem from file: %s", path)
        try:
            with open(path, "r") as file:
                self.weights = [int(line.strip()) for line in file if line.strip()]
            logger.debug("Weights loaded: %s", self.weights)
        except FileNotFoundError:
            logger.error("Problem input file not found: %s", path)
            raise RuntimeError(f"Problem input file not found: {path}")
        self.check()

    def read_benchmark_format(self, path: str):
        """
        Read weights from a benchmark format file.

        The first line is the number of weights N.
        The second line is the expected triplet sum.
        The next N lines are the weights.

        Args:
            path (str): Path to the benchmark file.

        Raises:
            RuntimeError: If the file is invalid, not found, or the sum check fails.
        """
        logger.info("Reading benchmark format from file: %s", path)
        try:
            with open(path, "r") as file:
                lines = [int(line.strip()) for line in file if line.strip()]
            logger.debug("Benchmark lines read: %s", lines)
        except FileNotFoundError:
            logger.error("Benchmark input file not found: %s", path)
            raise RuntimeError(f"Problem input file not found: {path}")

        if len(lines) < 2:
            logger.error("Benchmark file too short: %d lines", len(lines))
            raise RuntimeError("Benchmark file must contain at least two lines for N and triplet sum.")

        N = lines[0]
        triplet_sum = lines[1]
        self.weights = lines[2 : 2 + N]
        logger.debug("Parsed N=%d, triplet_sum=%d, weights=%s", N, triplet_sum, self.weights)
        self.check()
        self.check_triplet_sum(triplet_sum)

    def init(self, weights: List[int], binsize: int):
        """
        Initialize the problem with a given weight list and binsize.

        Args:
            weights (List[int]): List of integer weights.
            binsize (int): Expected sum of each triplet.

        Raises:
            RuntimeError: If validation fails.
        """
        logger.info("Initializing Problem with weights and binsize")
        self.weights = weights
        self.binsize = binsize
        logger.info("Weights: %s", weights)
        logger.info("Binsize: %d", binsize)
        self.check()
        self.check_triplet_sum(self.binsize)

    def check_triplet_sum(self, triplet_sum: int):
        """
        Check that the total sum of weights matches expected total
        from the given triplet sum and number of triplets.

        Args:
            triplet_sum (int): Expected sum per triplet.

        Raises:
            RuntimeError: If the total sum does not match.
        """
        actual = sum(self.weights)
        expected = triplet_sum * (len(self.weights) // 3)
        logger.debug("Checking triplet sum: actual=%d, expected=%d", actual, expected)
        if actual != expected:
            logger.error("Triplet sum mismatch: %d vs %d", actual, expected)
            raise RuntimeError(f"Total sum mismatch, actual vs expected: {actual} vs {expected}")
        logger.info("Triplet sum check passed")

    def check(self):
        """
        Perform basic validity checks on weights:
        - All weights must be positive.
        - Number of weights must be a multiple of 3.

        Raises:
            RuntimeError: If validation fails.
        """
        logger.debug("Performing weight checks: %s", self.weights)
        if any(w <= 0 for w in self.weights):
            logger.error("Non-positive weight found: %s", self.weights)
            raise RuntimeError(f"Non-positive weight found in: {self.weights}")
        if len(self.weights) % 3 != 0:
            logger.error("Weight count not divisible by 3: %d", len(self.weights))
            raise RuntimeError(f"Weight count not a multiple of three: {len(self.weights)}")
        logger.info("Basic weight checks passed")

    def get_weights(self) -> List[int]:
        """
        Return the list of weights.

        Returns:
            List[int]: The list of weights.

        >>> Problem().init([1,2,3], 6)
        >>> Problem().get_weights()  # Note: will be empty here due to fresh instance
        []
        """
        return self.weights

    def get_n(self) -> int:
        """
        Return the number of triplets.

        Returns:
            int: Number of triplets (length of weights divided by 3).

        >>> p = Problem()
        >>> p.init([3, 3, 6, 2, 2, 8], 12)
        >>> p.get_n()
        2
        """
        return len(self.weights) // 3

    def to_string(self) -> str:
        """
        Return a string representation of the weights list.

        Returns:
            str: A comma-separated string of weights.

        >>> p = Problem()
        >>> p.init([1, 2, 3], 6)
        >>> p.to_string()
        '[1,2,3]'
        """
        return "[" + ",".join(str(w) for w in self.weights) + "]"
