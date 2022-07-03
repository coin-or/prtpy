from experiments_csv import plot_results

from matplotlib import pyplot as plt
# plot_results(plt, "results/partition_uniform_integers.csv", filter={"numbins":2}, 
#     xcolumn="numitems", ycolumn="runtime", zcolumn=["bitsperitem","algorithm"])
# plot_results(plt, "results/partition_uniform_integers.csv", filter={"numbins":2,"bitsperitem":16}, 
#      xcolumn="numitems", ycolumn="runtime", zcolumn=["algorithm"], mean=True)
# plot_results(plt, "results/partition_uniform_integers.csv", filter={"numbins":2,"bitsperitem":48}, 
#      xcolumn="numitems", ycolumn="runtime", zcolumn=["algorithm"], mean=False)

_, subplots = plt.subplots(1,3, sharey=True)
# for s in subplots:
#      s.set_ylim(0,100)
plot_results(subplots[0], "results/check_complete_greedy_variants.csv", filter={"bitsperitem":16}, 
     xcolumn="numitems", ycolumn="runtime", zcolumn=["objective","use_lower_bound"], mean=True)
plot_results(subplots[1], "results/check_complete_greedy_variants.csv", filter={"bitsperitem":32}, 
     xcolumn="numitems", ycolumn="runtime", zcolumn=["objective","use_lower_bound"], mean=True)
plot_results(subplots[2], "results/check_complete_greedy_variants.csv", filter={"bitsperitem":48}, 
     xcolumn="numitems", ycolumn="runtime", zcolumn=["objective","use_lower_bound"], mean=True)
plt.savefig("results/check_complete_greedy_variants.png")
