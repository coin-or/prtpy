from .benchmark_maker import BenchmarkMaker
from .clock import Clock
import logging
import sys

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    """
    Entry point for running all benchmarks.

    Measures and logs the total elapsed time for benchmark execution,
    and handles any exceptions by logging error details.
    """
    main_start_t = Clock.elapsed()

    try:
        logger.info("Performing all benchmark tests...")
        BenchmarkMaker.perform_all()
        logger.info("All benchmark tests completed successfully.")
    except Exception as exc:
        logger.exception(f"Exception occurred during benchmark execution: {exc}")
    finally:
        main_end_t = Clock.elapsed()
        main_elapsed = main_end_t - main_start_t
        logger.info(f"Total time elapsed: {main_elapsed} seconds")
