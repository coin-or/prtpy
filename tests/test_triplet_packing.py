"""
An implementation of the algorithms in:
    "Solution of Bin Packing Instances in Falkenauer T Class: Not So Hard",
    by György Dósa, András Éles, Angshuman Robin Goswami, István Szalkai, Zsolt Tuza (2025),
    https://www.mdpi.com/1999-4893/18/2/115#

Programmer: Miriam Nagar.
Date: 2025-04.
"""

from typing import List, Tuple
import random
from prtpy.binners import BinnerKeepingContents, printbins
import logging
from prtpy.packing.triplet_packing import triplet_packing
from prtpy.packing.triplet_algo.models import SolverData
import pytest
import numpy.testing as npt


Falkenauer_t_test_cases = [
    {"item_num": 60,
    "bin_size": 1000,
    "items": [
        495, 474, 473, 472, 466, 450, 445, 444, 439, 430,
        419, 414, 410, 395, 372, 370, 366, 366, 366, 363,
        361, 357, 355, 351, 350, 350, 347, 320, 315, 307,
        303, 299, 298, 298, 292, 288, 287, 283, 275, 275,
        274, 273, 273, 272, 272, 271, 269, 269, 268, 263,
        262, 261, 259, 258, 255, 254, 252, 252, 252, 251
    ],
    "result": [
    [361, 339, 300], [376, 369, 255], [382, 366, 252],
    [396, 340, 264], [396, 347, 257], [399, 304, 297],
    [402, 333, 265], [403, 308, 289], [409, 314, 277],
    [411, 307, 282], [412, 334, 254], [423, 319, 258],
    [426, 313, 261], [444, 305, 251], [447, 302, 251],
    [462, 280, 258], [465, 275, 260], [468, 270, 262],
    [473, 267, 260], [475, 269, 256]]},
    {
    "item_num": 60,
    "bin_size": 1000,
    "items": [
        498, 252, 250, 498, 251, 251, 494, 252, 254, 482,
        260, 258, 482, 259, 259, 479, 267, 254, 476, 267, 
        257, 464, 267, 269, 459, 276, 265, 436, 288, 276, 
        430, 288, 282, 429, 305, 266, 401, 281, 318, 400, 
        308, 292, 398, 284, 318, 390, 308, 302, 378, 326, 
        296, 369, 328, 303, 367, 339, 294, 362, 345, 293
    ],
    "result": [
    [498, 252, 250], [498, 251, 251], [494, 252, 254],
    [482, 260, 258], [482, 259, 259], [479, 267, 254],
    [476, 267, 257], [464, 267, 269], [459, 276, 265],
    [436, 288, 276], [430, 288, 282], [429, 305, 266],
    [401, 281, 318], [400, 308, 292], [398, 284, 318],
    [390, 308, 302], [378, 326, 296], [369, 328, 303],
    [367, 339, 294], [362, 345, 293]]
    },
    {
        "item_num": 60,
        "bin_size": 1000,
        "items": [
            495, 493, 485, 478, 477, 462, 461, 459, 456, 451,
            429, 426, 414, 405, 391, 378, 375, 371, 369, 368,
            367, 361, 357, 354, 347, 345, 332, 316, 298, 297,
            293, 293, 281, 281, 278, 278, 277, 277, 275, 273,
            270, 268, 265, 265, 263, 263, 262, 261, 261, 258,
            258, 257, 256, 255, 255, 254, 254, 252, 250, 250
        ],
        "result": [
            [495, 254, 251], [493, 255, 252], [485, 258, 257],
            [478, 258, 264], [477, 261, 262], [462, 261, 277],
            [461, 263, 276], [459, 265, 276], [456, 265, 279],
            [451, 268, 281], [429, 270, 301], [426, 273, 301],
            [414, 275, 311], [405, 277, 318], [391, 278, 331],
            [378, 278, 344], [375, 281, 344], [371, 281, 348],
            [369, 293, 338], [368, 293, 339]
        ]
    },
    {
        "item_num": 249,
        "bin_size": 1000,
        "items": [
            499, 498, 493, 491, 489, 489, 489, 488, 487, 484,
            480, 479, 478, 472, 471, 467, 466, 463, 463, 463,
            461, 453, 450, 447, 445, 444, 443, 440, 438, 438,
            435, 433, 433, 431, 425, 425, 425, 422, 420, 419,
            418, 414, 413, 412, 411, 407, 405, 404, 404, 403,
            403, 400, 399, 394, 394, 389, 388, 386, 385, 384,
            384, 382, 382, 381, 381, 380, 379, 379, 378, 377,
            376, 376, 374, 374, 371, 370, 367, 366, 365, 365,
            363, 363, 362, 361, 360, 358, 357, 356, 353, 353,
            352, 352, 350, 350, 346, 345, 343, 343, 342, 338,
            336, 335, 335, 334, 333, 330, 330, 329, 329, 328,
            326, 324, 323, 321, 320, 320, 319, 317, 315, 315,
            314, 313, 313, 312, 312, 312, 310, 310, 309, 308,
            307, 307, 307, 305, 304, 304, 301, 301, 300, 300,
            300, 299, 299, 299, 297, 297, 297, 297, 295, 295,
            294, 294, 293, 293, 291, 290, 289, 289, 288, 287,
            286, 285, 285, 283, 283, 283, 282, 281, 280, 279,
            279, 279, 279, 278, 276, 276, 276, 276, 276, 275,
            275, 274, 274, 274, 273, 273, 273, 273, 271, 270,
            270, 270, 269, 268, 268, 268, 267, 267, 265, 265,
            264, 263, 263, 263, 263, 262, 262, 261, 261, 260,
            260, 260, 260, 259, 259, 259, 259, 259, 258, 258,
            258, 257, 257, 255, 255, 255, 254, 254, 254, 253,
            253, 253, 252, 252, 252, 252, 252, 252, 252, 252,
            252, 251, 251, 251, 250, 250, 250, 250, 250
        ],
        "result": [
            [499, 251, 250], [498, 252, 250], [493, 257, 250],
            [491, 259, 250], [489, 261, 250], [489, 262, 249],
            [489, 263, 248], [488, 265, 247], [487, 266, 247],
            [484, 268, 248], [480, 270, 250], [479, 270, 251],
            [478, 271, 251], [472, 272, 256], [471, 273, 256],
            [467, 274, 259], [466, 275, 259], [463, 276, 261],
            [463, 276, 261], [463, 277, 260], [461, 279, 260],
            [453, 287, 260], [450, 288, 262], [447, 289, 264],
            [445, 290, 265], [444, 291, 265], [443, 294, 263],
            [440, 294, 266], [438, 295, 267], [438, 297, 265],
            [435, 297, 268], [433, 297, 270], [433, 297, 270],
            [431, 299, 270], [425, 299, 276], [425, 299, 276],
            [425, 300, 275], [422, 301, 277], [420, 301, 279],
            [419, 301, 280], [418, 304, 278], [414, 304, 282],
            [413, 305, 282], [412, 308, 280], [411, 308, 281],
            [407, 309, 284], [405, 312, 283], [404, 312, 284],
            [404, 313, 283], [403, 313, 284], [403, 315, 282],
            [400, 315, 285], [399, 317, 284], [394, 320, 286],
            [394, 320, 286], [389, 321, 290], [388, 323, 289],
            [386, 324, 290], [385, 326, 289], [384, 328, 288],
            [384, 329, 287], [382, 329, 289], [382, 330, 288],
            [381, 330, 289], [381, 333, 286], [380, 334, 286],
            [379, 335, 286], [379, 336, 285], [378, 338, 284],
            [377, 342, 281], [376, 343, 281], [376, 343, 281]
        ]
    },
]


not_allocatable_test_case = [
    {"item_num": 60,
    "bin_size": 1000,
    "items": [
        333, 333, 333, 333, 333, 333, 333, 333, 333, 333,
        333, 333, 333, 333, 333, 333, 333, 333, 333, 333,
        333, 333, 333, 333, 333, 333, 333, 333, 333, 333,
        333, 333, 333, 333, 333, 333, 333, 333, 333, 333,
        333, 333, 333, 333, 333, 333, 333, 333, 333, 333,
        333, 333, 333, 333, 333, 333, 333, 333, 333, 353,
    ]},
]


def _generate_items_and_put_into_bins(seed: int, bin_size: int, items_num: int):
    DEFAULT_BIN_SIZE = 1000
    DEFAULT_ITEM_NUM = 60

    if bin_size < 50:
        logging.warning(f"Bin size too small: {bin_size}")
        bin_size = DEFAULT_BIN_SIZE
        logging.info(f"changed bin size to: {bin_size}")
        

    if items_num < 3:
        logging.warning(f"Items num too small: {items_num}")
        items_num = DEFAULT_ITEM_NUM
        logging.info(f"changed items num to: {items_num}")

    random.seed(seed)
    upper_bnd: int = round(bin_size / 2)
    lower_bnd: int = round(bin_size / 4)

    binner = BinnerKeepingContents()
    # Determine number of bins (1 for every 3 items)
    numbins = items_num // 3
    bins = binner.new_bins(numbins)

    item_list = []
    for i in range(items_num // 3):
        item_1 = random.randint(lower_bnd, upper_bnd)
        item_2 = random.randint(lower_bnd, upper_bnd)
        item_3 = bin_size - (item_1 + item_2)
        item_list.extend([item_1, item_2, item_3])

        # Add items to bins
        triplet = [item_1, item_2, item_3]
        bin_index = i
        for item in triplet:
            binner.add_item_to_bin(bins, item, bin_index)

    return item_list, bins


def create_random_allocatable_item_list(
    bin_size: int = 1000, items_num: int = 60
) -> Tuple[List, BinnerKeepingContents]:
    SEED = 97

    return _generate_items_and_put_into_bins(SEED, bin_size, items_num)


def create_random_not_allocatable_item_list(
    bin_size: int = 1000, items_num: int = 60
) -> List:
    SEED = 71

    item_list, bins = _generate_items_and_put_into_bins(SEED, bin_size, items_num)
    # add one to the last item in order to make it not allocatable
    bins[1][-1][-1] += 1
    item_list[-1] += 1
    return item_list, bins


def check_item_list_is_valid(bin_size: int, bins: List) -> bool:
    ITEMS_PER_BIN_SIZE = 3
    if len(bins) == 0:
        return False
    for bin in bins:
        triplet_sum = sum(bin)
        if triplet_sum != bin_size:
            return False

    return True


def test_creation_random_not_allocatable_item_list():
    bin_size = 1200
    _, bins = create_random_not_allocatable_item_list(bin_size)
    _, triplets = bins  # bins = sums, Triplets list
    assert not check_item_list_is_valid(bin_size, triplets)


def test_creation_random_allocatable_item_list():
    bin_size = 1200
    _, bins = create_random_allocatable_item_list(bin_size)
    _, triplets = bins  # bins = sums, Triplets list
    assert check_item_list_is_valid(bin_size, triplets)


def assert_triplet_packing_valid_result(result, binsize):
    _ , triplets_result = result

    for tri in triplets_result:
        assert len(tri) == 3, f"Expected 3 items per bin, got {len(tri)}"
        assert sum(tri) == binsize, f"Bin sum mismatch: got {sum(tri)} instead of {binsize}"


def test_randomized_items_packing_allocation():
    bin_sizes = [1000]
    item_nums = [60, 99]

    for b_size, item_num in zip(bin_sizes, item_nums):
        item_list, bins = create_random_allocatable_item_list(b_size, item_num)
        sums, triplets = bins
        assert check_item_list_is_valid(b_size, triplets)

        # backtrack
        bin_result = triplet_packing(BinnerKeepingContents(), binsize=b_size, items=item_list)
        assert_triplet_packing_valid_result(bin_result, b_size)

        # local search
        bin_result = triplet_packing(BinnerKeepingContents(), binsize=b_size, items=item_list, use_local_search=True)
        assert_triplet_packing_valid_result(bin_result, b_size)


def test_items_packing_allocation():
    
    for item in Falkenauer_t_test_cases:
        b_size = item["bin_size"]
        item_list = item["items"]

        # backtrack
        bin_result = triplet_packing(BinnerKeepingContents(), binsize=b_size, items=item_list)
        assert_triplet_packing_valid_result(bin_result, b_size)

        # local search
        bin_result = triplet_packing(BinnerKeepingContents(), binsize=b_size, items=item_list, use_local_search=True)
        assert_triplet_packing_valid_result(bin_result, b_size)


def test_invalid_input_throws_exception():
    for func in [triplet_packing]:
        item_list, _ = create_random_not_allocatable_item_list()

        with pytest.raises(RuntimeError):
            # Total sum mismatch, actual vs expected: 20001 vs 20000
            func(BinnerKeepingContents(), binsize=1000, items=item_list)

        with pytest.raises(TypeError):
            # invalid item
            func(BinnerKeepingContents(), binsize=1000, items=[])

        with pytest.raises(TypeError):
            # Invalid binner value
            func(binner=5, binsize=1000, items=item_list)

        with pytest.raises(RuntimeError):
            func(BinnerKeepingContents(), binsize=-5, items=item_list)

        with pytest.raises(RuntimeError):
            # Non-positive weight found in: [400, -100, 200]
            func(BinnerKeepingContents(), binsize=500, items=[400, -100, 200])

        with pytest.raises(RuntimeError):
            # Weight count not a multiple of three: 4
            func(BinnerKeepingContents(), binsize=1000, items=[400, 600, 200, 50])



def test_no_solution_local_search():
    for item in not_allocatable_test_case:
        b_size = item["bin_size"]
        item_list = item["items"]

        with pytest.raises(SolverData.Error):
            triplet_packing(BinnerKeepingContents(), binsize=b_size, items=item_list, use_local_search=True)


def test_no_solution_backtrack():
    for item in not_allocatable_test_case:
        b_size = item["bin_size"]
        item_list = item["items"]
        
        with pytest.raises(SolverData.Error):
            triplet_packing(BinnerKeepingContents(), binsize=b_size, items=item_list)