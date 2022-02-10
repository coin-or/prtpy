"""
Defines a Bins structure.
It can be used both during algorithms, and to return their results.

@author Erel Segal-Halevi
"""



# Bin string templates:
ITEM_NAMES = "{item}"
ITEM_SIZES = "{size}"
ITEM_NAMES_AND_SIZES = "{item}={size}"

class Bins:

    """
    >>> bins = Bins([11,22,33,44], 2)
    >>> bins.add_item_to_bin(0, 0)
    >>> bins.add_item_to_bin(1, 0)
    >>> bins.add_empty_bin()
    >>> bins.add_item_to_bin(2, 1)
    >>> bins.add_item_to_bin(3, 2)
    >>> bins
    Bin #0: 0=11,1=22: sum=33
    Bin #1: 2=33: sum=33
    Bin #2: 3=44: sum=44
    >>> bins.string_template = ITEM_SIZES
    >>> bins
    Bin #0: 11,22: sum=33
    Bin #1: 33: sum=33
    Bin #2: 44: sum=44
    >>> bins.string_template = ITEM_NAMES
    >>> bins
    Bin #0: 0,1: sum=33
    Bin #1: 2: sum=33
    Bin #2: 3: sum=44
    """

    def __init__(self, map_item_to_size:list, num_of_initial_bins:int=1, string_template=ITEM_NAMES_AND_SIZES) -> None:
        self.map_item_to_size = map_item_to_size
        self.bins = [ ]
        self.sums = [ ]
        self.string_template = string_template
        for _ in range(num_of_initial_bins):
            self.add_empty_bin()

    def add_empty_bin(self) -> None:
        self.bins.append([])
        self.sums.append(0)

    def add_item_to_bin(self, item_index:int, bin_index:int):
        self.bins[bin_index].append(item_index)
        self.sums[bin_index] += self.map_item_to_size[item_index]

    def bin_to_str(self, bin_index:int)->str:
        bin = self.bins[bin_index]
        return ",".join(
            [self.string_template.format(item=item, size=self.map_item_to_size[item]) 
            for item in bin])

    def __repr__(self)->str:
        return "\n".join([f"Bin #{i}: {self.bin_to_str(i)}: sum={self.sums[i]}" for i in range(len(self.bins))])



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))


