import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Clock:
    """
    Utility class for time measurement and formatting based on a monotonic clock start.

    Attributes:
        _start_time (float): The time when the Clock class was first loaded, used as a reference for elapsed time.
    """

    _start_time = time.perf_counter()

    @staticmethod
    def print_time(fraction_digits: int = 3) -> str:
        """
        Returns the current local datetime as a formatted string with optional fractional seconds.

        Args:
            fraction_digits (int): Number of decimal places to include for fractional seconds (0 to disable).

        Returns:
            str: Formatted datetime string, e.g. "2025.06.29 23:45:12.123".

        Example:
            >>> s = Clock.print_time(3)
            >>> isinstance(s, str)
            True
            >>> len(s) > 0
            True
        """
        now = datetime.now()
        base_time = now.strftime("%Y.%m.%d %H:%M:%S")
        if fraction_digits > 0:
            ns = now.timestamp() % 1
            frac = f" {ns:.{fraction_digits}f}"[1:]
            formatted = base_time + frac
        else:
            formatted = base_time
        return formatted

    @staticmethod
    def elapsed() -> float:
        """
        Returns the elapsed time in seconds since the Clock class was loaded.

        Uses a monotonic high-resolution timer.

        Returns:
            float: Elapsed time in seconds.
        """
        elapsed_time = time.perf_counter() - Clock._start_time
        return elapsed_time

    @staticmethod
    def benchmark_self(seconds: float):
        """
        Benchmarks the performance of the elapsed() method by counting
        how many times it can be called in the specified duration.

        Logs the iteration count and calls per second.

        Args:
            seconds (float): Duration in seconds to run the benchmark.
        """
        logger.info("Starting benchmark_self for %.2f seconds", seconds)
        count = 0
        end_time = Clock.elapsed() + seconds
        while Clock.elapsed() < end_time:
            count += 1
        ratio = count / seconds
        logger.info("Clock.benchmark(): %d iterations in %.2f seconds = %.2f/sec", count, seconds, ratio)
