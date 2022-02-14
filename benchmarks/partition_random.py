import prtpy, numpy as np
from typing import Callable


def partition_random_items(
    algorithm: Callable,
    numbins: int,
    numitems: int,
    minvalue: int,
    maxvalue: int,
    objective: prtpy.obj.Objective = prtpy.obj.MinimizeDifference,
    outputtype: prtpy.out.OutputType = prtpy.out.Partition,
):
    prtpy.partition(
        algorithm=algorithm,
        numbins=numbins,
        items=np.random.randint(minvalue, maxvalue, numitems),
        objective=objective,
        outputtype=outputtype,
    )
