"""
Produce an optimal partition by solving an integer linear program (ILP).

Programmer: Erel Segal-Halevi
Since: 2022-02

Credit: Rob Pratt, https://or.stackexchange.com/a/6115/2576
"""


import mip

items = [11.,11.,11.,11.,22.]
bins = [0,1]
model = mip.Model("partition")
counts: dict = {
    item: [model.add_var(var_type=mip.INTEGER) for bin in bins] for item in items
}  # The variable counts[i][j] determines how many times item i appears in bin j.
bin_sums = [
    sum([counts[item][bin] * item for item in items]) for bin in bins
]

# Construct the list of constraints:
counts_are_non_negative = [counts[item][bin] >= 0 for bin in bins for item in items]
each_item_in_one_bin = [
    sum([counts[item][bin] for bin in bins]) == 1 for item in items
]
bin_sums_in_ascending_order = [bin_sums[1] >= bin_sums[0]]

for constraint in counts_are_non_negative + each_item_in_one_bin + bin_sums_in_ascending_order: 
        model += constraint

model.objective = mip.maximize(bin_sums[0])


# Solve the ILP:
model.verbose = 1
status = model.optimize()
print("status: ", status)

# Construct the output:
for bin in bins:
    for item in items:
        count_item_in_bin = int(counts[item][bin].x)
        if count_item_in_bin>0:
            print(f"bin {bin} contains item {item}")

