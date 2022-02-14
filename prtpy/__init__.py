import pathlib

HERE = pathlib.Path(__file__).parent
__version__ = (HERE / "VERSION").read_text().strip()

import prtpy.outputtypes as out
import prtpy.objectives as obj
from prtpy.partition import partition


class exact:  # Algorithms that return the exact optimal partition
    from prtpy.complete_greedy import optimal as cg
    from prtpy.complete_greedy import optimal as complete_greedy
    from prtpy.dp import optimal as dp
    from prtpy.dp import optimal as dynamic_programming
    from prtpy.ilp import optimal as ilp
    from prtpy.ilp import optimal as integer_programming


class approx:  # Algorithms that return an approximately-optimal partition
    from prtpy.greedy import greedy
