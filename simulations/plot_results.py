from experiments_csv import plot_results

from matplotlib import pyplot as plt

_, subplots = plt.subplots(1,3, sharey=True)
for s in subplots:
     s.set_xlim(0,25)
     s.set_ylim(0,30)

# plot_results(plt, "results/partition_uniform_integers.csv", filter={"numbins":2}, 
#     xcolumn="numitems", ycolumn="runtime", zcolumn=["bitsperitem","algorithm"])
# plot_results(plt, "results/partition_uniform_integers.csv", filter={"numbins":2,"bitsperitem":48}, 
#      xcolumn="numitems", ycolumn="runtime", zcolumn=["algorithm"], mean=False)

# plot_results(subplots[0], "results/partition_uniform_integers.csv", filter={"bitsperitem":16}, 
#      xcolumn="numitems", ycolumn="diff", zcolumn=["algorithm"], mean=True)
# plot_results(subplots[1], "results/partition_uniform_integers.csv", filter={"bitsperitem":32}, 
#      xcolumn="numitems", ycolumn="diff", zcolumn=["algorithm"], mean=True)
# plot_results(subplots[2], "results/partition_uniform_integers.csv", filter={"bitsperitem":48}, 
#      xcolumn="numitems", ycolumn="diff", zcolumn=["algorithm"], mean=True)
# plt.savefig("results/partition_uniform_integers.png")


def plot_check_variants(filename:str):
     csv_filename = filename+".csv"
     output_filename = filename+".png"
     plot_results(subplots[0], csv_filename, filter={"bitsperitem":16, "use_lower_bound":True}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["objective"], mean=True, legend_properties={"size":6})
     plot_results(subplots[1], csv_filename, filter={"bitsperitem":32, "use_lower_bound":True}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["objective"], mean=True, legend_properties={"size":6})
     plot_results(subplots[2], csv_filename, filter={"bitsperitem":48, "use_lower_bound":True}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["objective"], mean=True, legend_properties={"size":6})
     plt.savefig(output_filename)

def plot_check_variants_3(filename:str):
     csv_filename = filename+".csv"
     output_filename = filename+".png"
     plot_results(subplots[0], csv_filename, filter={"bitsperitem":16, "use_heuristic_3":False}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["use_lower_bound", "use_heuristic_2", "use_heuristic_3"], mean=True, legend_properties={"size":6})
     plot_results(subplots[1], csv_filename, filter={"bitsperitem":32, "use_heuristic_3":False}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["use_lower_bound", "use_heuristic_2", "use_heuristic_3"], mean=True, legend_properties={"size":6})
     plot_results(subplots[2], csv_filename, filter={"bitsperitem":48, "use_heuristic_3":False}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["use_lower_bound", "use_heuristic_2", "use_heuristic_3"], mean=True, legend_properties={"size":6})
     plt.savefig(output_filename)

plot_check_variants_3("results/check_complete_greedy_variants_4")
