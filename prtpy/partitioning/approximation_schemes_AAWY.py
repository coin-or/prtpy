
from typing import Callable


# def mainAlgorithm(epsilon:float, jobs: list[int], numbrOfMachines:int, f: Callable)->list[list[int]]:
#     # """
#     # "Approximation Schemes for Scheduling on Parallel Machines", by Noga Alon, Yossi Azar, Gerhard J. Woeginger and Tal Yadid,
#     #  (1975), https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1099-1425(199806)1:1%3C55::AID-JOS2%3E3.0.CO;2-J
#     # main algorithm in the artical (page.9): accepts list of jobs and number of machines 
#     # and creates a schedule for the machines s.t, we process all the jobs and minimize sum(f(C_i)) 
#     # when C_i is the compilition time of machine #i (0<i<number_of_machines+1)
#     # f(x) is a given convex function.
#     # the gerenteed result is that the diffenence between the algorithm output and the optimal schedul (that minimize sum(f(C_i)) )
#     # is <= epsilon * OPT"

#     # Example 1: 
#     # >>> mainAlgorithm(0.1,[124000,34000,54768,115256,89765,43124,107,23047,200101,78900,65432,101436,52422,17642],2,lambda x:x**2)
#     # [[124000,54768,89765,78900,101436,52422,17642],[34000,115256,43124,107,23047,200101,65432]]
    
#     # Example 2: 
#     # >>> mainAlgorithm(0.5,[426,666,846,8500,3300,1546,985,103,674,131,124,564,135],2,lambda x:x)
#     # [[426,666,846,8500,3300,1546,985,103,674,131,124,564,135][]]

#     # Example 3:
#     # >>> mainAlgorithm(0.5,[107,7502,684,12123,450,4663,1985,4102,1052,407,310,113,200,23,1012,41,126,5100],4,lambda x:x**2)
#     # [[107,4663,1985,4102,407,113],[7502,23,1012,41,5100],[684,450,1052,310,200,126],[12123]]
#     # """
#     return [[0]]

# def ConvertJobs(jobs: list[int], L: int, lambda_star:int)->list[float]:
#     # """
#     # "this algorithm convert every job p_j to its corresponding job p_j#"
#     # >>> ConvertJobs([124000,34000,54768,115256,89765,43124,107,23047,200101,78900,65432,101436,52422,17642],500000,500)
#     # [124000,34000,54768,115256,89766,43124,1000,23048,200102,78900,65432,101436,52422,17642]
#     # """
#     """
#     "this algorithm convert every job p_j to its corresponding job p_j#"
#     >>> ConvertJobs([124000,34000,54768,115256,89765,43124,107,23047,200101,78900,65432,101436,52422,17642],500000,500)
#     [0]
#     """
#     return [0]    
    

# def IP(ConvertedJobs: list[float], numbrOfMachines:int, f: Callable)->list[list[float]]:
#     # """
#     # "partition the  converted jobs into numbrOfMachines parts in an optimal way such that we minimize sum(f(C_i))"
#     # >>> IP([124000,34000,54768,115256,89766,43124,1000,23048,200102,78900,65432,101436,52422,17642],2,lambda x:x**2)
#     # [[124000,54768,89766,78900,101436,52422,17642],[34000,115256,43124,1000,23048,200102,65432]]
#     # """
#     """
#     "partition the  converted jobs into numbrOfMachines parts in an optimal way such that we minimize sum(f(C_i))"
#     >>> IP([124000,34000,54768,115256,89766,43124,1000,23048,200102,78900,65432,101436,52422,17642],2,lambda x:x**2)
#     [[0]]
#     """
#     return [[0]]

# def deconvertJobs(partition: list[list[float]], L: int, lambda_star:int)->list[list[int]]:
#     # """
#     # "this algorithm deconvert the partition of the converted jobs into a new parition of the original jobs
#     # >>> deconvertJobs([[124000,54768,89766,78900,101436,52422,17642],[34000,115256,43124,1000,23048,200102,65432]], 500000,500)
#     # [[124000,54768,89765,78900,101436,52422,17642],[34000,115256,43124,107,23047,200101,65432]]
#     # """
#     """
#     "this algorithm deconvert the partition of the converted jobs into a new parition of the original jobs
#     >>> deconvertJobs([[124000,54768,89766,78900,101436,52422,17642],[34000,115256,43124,1000,23048,200102,65432]], 500000,500)
#     [[0]]
#     """
#     return [[0]]

# if __name__ == "__main__":
#     import doctest
#     print(doctest.testmod())    