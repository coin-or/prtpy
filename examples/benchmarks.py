"""
Check the runtime of various methods.
"""
import numpy as np
from timeit import timeit

SIZE = 1000000
large_array = list(np.random.randint(1, 1000, SIZE))
print(timeit(lambda: large_array.sort(), number=10))
print(
    timeit(lambda: large_array.sort(key=lambda item: item), number=10)
)  # Takes 3 times more with the lambda
