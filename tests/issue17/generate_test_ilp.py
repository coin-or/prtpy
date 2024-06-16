from numpy.random import seed
from numpy.random import randint
import prtpy

if __name__=="__main__":

    seed(1)

    for _ in range(1000):
        for i in range(1, 10):
            original_values = randint(0, 10000, i)
            answer1 = prtpy.partition(algorithm = prtpy.partitioning.ilp, numbins=2, items=original_values, objective=prtpy.obj.MaximizeSmallestSum)
            diff1 = abs(sum(answer1[0]) - sum(answer1[1]))
            original_values.sort()
            answer2 = prtpy.partition(algorithm = prtpy.partitioning.ilp, numbins=2, items=original_values, objective=prtpy.obj.MaximizeSmallestSum)
            diff2 = abs(sum(answer2[0]) - sum(answer2[1]))
            
            if diff1 != diff2:
                print("\n\nFound example at ", i, ":")
                print("One answer with a diff of ", diff1, ":")
                print(answer1[0])
                print(answer1[1])
                print("\nThe other answer with a diff of ", diff2, ":")
                print(answer2[0])
                print(answer2[1])
