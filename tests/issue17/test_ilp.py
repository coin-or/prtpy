import prtpy

# items = [3984, 9928, 3636, 2852, 4957, 5366, 4456, 5905]
items = [7740, 489, 152, 3410, 9948, 7862, 8519, 3212, 8798, 4979, 2178, 5984, 2518, 3270, 7183]

answer1 = prtpy.partition(algorithm = prtpy.partitioning.ilp, numbins=2, items=items, objective=prtpy.obj.MinimizeLargestSum, model_filename="issue17a.lp", solution_filename="issue17a.sol")
print(answer1)
print([sum(bin) for bin in answer1])
print(sum(answer1[0]) - sum(answer1[1]))

items.sort()
answer2 = prtpy.partition(algorithm = prtpy.partitioning.ilp, numbins=2, items=items, objective=prtpy.obj.MinimizeLargestSum, model_filename="issue17b.lp", solution_filename="issue17b.sol")
print(answer2)
print([sum(bin) for bin in answer2])
print(sum(answer2[0]) - sum(answer2[1]))


