from experiments_csv import plot_results

from matplotlib import pyplot as plt
# plot_results(plt, "results/partition_uniform_integers.csv", filter={"numbins":2}, 
#     xcolumn="numitems", ycolumn="runtime", zcolumn=["bitsperitem","algorithm"])
plot_results(plt, "results/partition_uniform_integers.csv", filter={"numbins":2,"bitsperitem":16}, 
     xcolumn="numitems", ycolumn="runtime", zcolumn=["algorithm"], mean=True)
plot_results(plt, "results/partition_uniform_integers.csv", filter={"numbins":2,"bitsperitem":48}, 
     xcolumn="numitems", ycolumn="runtime", zcolumn=["algorithm"], mean=False)
