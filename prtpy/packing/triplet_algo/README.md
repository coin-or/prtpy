## Triplet Packing Algorithms (triplet_algo/)

This module is a core part of the prtpy library and provides an extensible framework for solving the Triplet Packing Problem — a constrained grouping problem where items must be partitioned into triplets (groups of 3) while satisfying structural and optimization constraints.

### Problem Overview:
Given a list of items with associated weights (and optional grouping or capacity constraints), the goal is to assign them into triplets such  the sum of each triplet equals the given bin size.

This code implements two algorithms from the paper:
- Complete backtracking search for fair item allocation (default method).
- Local search heuristic for fair item allocation (enabled if `use_local_search_method=True`).

##  File Structure

| File                      | Purpose                                                                                      |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| `main.py`                 | Entry point to run the triplet planner and experiment with input data.                       |
| `triplet_planner.py`      | Coordinates the full triplet planning process (preprocessing, backtracking, local search).   |
| `problem.py`              | Encapsulates the input instance (items, weights, constraints).                               |
| `solution.py`             | Represents a candidate solution with methods to manipulate and evaluate triplets.            |
| `solution_checker.py`     | Validates solution correctness and feasibility.                                              |
| `triplet.py`              | Contains the `Triplet` class and utilities for creating and comparing triplets.              |
| `triplet_backtracker.py`  | Implements the recursive backtracking engine to search for feasible groupings.               |
| `triplet_local_search.py` | Performs local search optimization on an existing solution to improve infeasibility or cost. |
| `multi_combination.py`    | Provides logic for generating weighted combinations efficiently.                             |
| `models.py`               | Defines data classes and core enums used across components (e.g., status, error types).      |
| `solver.py`               | High-level solver that binds all modules into a unified interface.                           |
| `benchmark_maker.py`      | Utility to generate synthetic test instances for benchmarking.                               |
| `clock.py`                | Timer utilities for profiling and runtime limits.                                            |
| `backtrack_utils.py`      | Heuristic tools used in the backtracking search phase.                                       |


## Core Components

#### Problem

Defined in problem.py, it parses and stores the input data:

```
Problem(weights: List[int], group_constraints: Optional[Dict] = None)
```

#### TripletPlanner
The orchestrator in triplet_planner.py that manages:

Preprocessing: Identify duplicates, fixed triplets.

Search: Use triplet_backtracker to explore valid configurations.

Improvement: Apply triplet_local_search for refinements.

#### TripletBacktracker
A recursive solver that:

Branches on candidate triplets.

Tracks infeasibility, usage, and constraints.

Uses heuristics from backtrack_utils.py.

#### TripletLocalSearch
Attempts to improve a solution by swapping or replacing elements.

Can reduce infeasible triplets or balance groups.

### Running all Falkenaur T class cases

To run all benchmark tests on backtrack method:
```
python -m prtpy.packing.triplet_algo.main 
```

Features
- Modular architecture (problem, solver, local search)
- Supports multiple solving strategies
- Feasibility checks and solution validation
- Benchmarking and runtime tracking
- Designed for extensibility and experimental tuning

### Dev Notes

- Python 3.8+
- No external dependencies
- Internal utilities (clock, models, multi_combination) streamline performance and structure
- Includes support for large-scale triplet generation and arbitrary-precision indexing

### Author

Developed by Miriam Nagar
An implementation of the algorithms in:
    "Solution of Bin Packing Instances in Falkenauer T Class: Not So Hard",
    by György Dósa, András Éles, Angshuman Robin Goswami, István Szalkai, Zsolt Tuza (2025),
    https://www.mdpi.com/1999-4893/18/2/115#

The authors included c# source code, this is the converted version to python.
Programmer: Miriam Nagar.
