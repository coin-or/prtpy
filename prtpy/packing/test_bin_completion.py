from prtpy import BinsKeepingContents, BinsKeepingSums
import pytest
from prtpy.packing import bin_completion

algorithm = bin_completion.bin_completion


# In this test we will check cases where we need only 1 bin to store the items:
def test_fits_one_bin():
    assert algorithm(BinsKeepingContents(), binsize=5, items=[1, 1, 1, 1, 1]).bins == [[1, 1, 1, 1, 1]]
    assert algorithm(BinsKeepingContents(), binsize=10, items=[10]).bins == [[10]]
    assert algorithm(BinsKeepingContents(), binsize=15, items=[1, 2, 3, 4, 5]).bins == [[5, 4, 3, 2, 1]]
    assert algorithm(BinsKeepingContents(), binsize=10, items=[1, 2, 3]).bins == [[3, 2, 1]]
    assert algorithm(BinsKeepingContents(), binsize=3, items=[1, 2, 0, 0]).bins == [[2, 1]]

# In this test we will check cases where there are no item with weight so no bins are necessary:
def test_zero_bins():
    assert algorithm(BinsKeepingContents(), binsize=1, items=[]).bins == []
    assert algorithm(BinsKeepingContents(), binsize=1, items=[0]).bins == []
    assert algorithm(BinsKeepingContents(), binsize=1, items=[0, 0, 0, 0]).bins == []
    assert algorithm(BinsKeepingContents(), binsize=0, items=[]).bins == []
    assert algorithm(BinsKeepingContents(), binsize=0, items=[0]).bins == []
    assert algorithm(BinsKeepingContents(), binsize=0, items=[0, 0, 0, 0]).bins == []

# In this test we will check a variety of cases such as small items and a large number of items or bins:
def test_variant_examples():
    assert algorithm(BinsKeepingContents(), binsize=100, items=[99, 99, 99, 99, 99]).bins == [[99], [99], [99], [99], [99]]
    assert algorithm(BinsKeepingContents(), binsize=100, items=[3, 9, 12, 15]).bins == [[15, 12, 9, 3]]
    assert algorithm(BinsKeepingContents(), binsize=100, items=[99, 90, 60, 30, 10]).bins == [[99], [90, 10], [60, 30]]
    assert algorithm(BinsKeepingContents(), binsize=100, items=[100, 99, 98, 97, 96, 95, 94, 0, 1, 2, 3, 4, 5, 6]).bins == \
                                                                 [[100], [99, 1], [98, 2], [97, 3], [96, 4], [95, 5], [94, 6]]
    assert algorithm(BinsKeepingContents(), binsize=100, items=[5, 11, 14, 39, 42, 81, 0, 0]).bins == [[81, 14, 5], [42, 39, 11]]
    assert algorithm(BinsKeepingContents(), binsize=100,
                          items=[100, 98, 96, 93, 0, 91, 87, 81, 0, 59, 58, 55, 50, 43, 22, 21, 20, 15, 14, 10, 8, 6, 5, 4, 3, 1]).bins == \
                                [[100], [98], [96, 4], [93, 6, 1], [91, 8], [87, 10, 3], [81, 15], [59, 22, 14, 5], [58, 21, 20], [55, 43], [50]]

# In this test we will check that the algorithm function raises an error when one or more of the items is bigger than
# the bin capacity:
def test_raise_big_numbers():
    with pytest.raises(ValueError):
        algorithm(BinsKeepingContents(), binsize=1, items=[1, 2, 3])
        algorithm(BinsKeepingContents(), binsize=2, items=[10])
        algorithm(BinsKeepingContents(), binsize=3, items=[1, 2, 3, 4])
        algorithm(BinsKeepingContents(), binsize=4, items=[5, 6, 7])
        algorithm(BinsKeepingContents(), binsize=100, items=[200, 0])
        algorithm(BinsKeepingContents(), binsize=200, items=[1, 2, 300, 0, 0])

# In this test we will check that the algorithm function raises an error when the input includes items that are not
# of number type:
def test_raise_wrong_input():
    with pytest.raises(ValueError):
        algorithm(BinsKeepingContents(), binsize=100, items=[1, 2, "aaa"])
        algorithm(BinsKeepingContents(), binsize=100, items=['c'])
        algorithm(BinsKeepingContents(), binsize=100, items=['1', '2', '3', '4'])
        algorithm(BinsKeepingContents(), binsize=100, items=["Avshalom", "Tehila"])
        algorithm(BinsKeepingContents(), binsize=100, items=["One Hundred"])
        algorithm(BinsKeepingContents(), binsize=100, items=[[1,2]])
        algorithm(BinsKeepingContents(), binsize=100, items=['@', '#', '$'])