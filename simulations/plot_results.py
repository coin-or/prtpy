from experiments_csv import plot_results

from matplotlib import pyplot as plt

_, subplots = plt.subplots(1,3, sharey=True)
for s in subplots:
     # s.set_xlim(0,25)
     s.set_ylim(0,30)

def plot_partition_algorithms(filename:str):
     csv_filename = filename+".csv"
     output_filename = filename+".png"
     plot_results(subplots[0], csv_filename, filter={"bitsperitem":16}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["algorithm"], mean=True, legend_properties={"size":6})
     plot_results(subplots[1], csv_filename, filter={"bitsperitem":32}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["algorithm"], mean=True, legend_properties={"size":6})
     plot_results(subplots[2], csv_filename, filter={"bitsperitem":48}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["algorithm"], mean=True, legend_properties={"size":6})
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

def plot_check_variants_5(filename:str):
     csv_filename = filename+".csv"
     output_filename = filename+".png"
     plot_results(subplots[0], csv_filename, filter={"bitsperitem":16, "use_heuristic_2":True, "use_lower_bound":False}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["objective", "use_heuristic_3"], mean=True, legend_properties={"size":6})
     plot_results(subplots[1], csv_filename, filter={"bitsperitem":32, "use_heuristic_2":True, "use_lower_bound":False}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["objective", "use_heuristic_3"], mean=True, legend_properties={"size":6})
     plot_results(subplots[2], csv_filename, filter={"bitsperitem":48, "use_heuristic_2":True, "use_lower_bound":False}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["objective", "use_heuristic_3"], mean=True, legend_properties={"size":6})
     plt.savefig(output_filename)

def plot_check_variants_dp(filename:str):
     csv_filename = filename+".csv"
     output_filename = filename+".png"
     plot_results(plt, csv_filename, filter={}, 
          xcolumn="numitems", ycolumn="runtime", zcolumn=["bitsperitem", "use_boolean_matrix"], mean=True, legend_properties={"size":6})
     plt.savefig(output_filename)

plot_partition_algorithms("results/partition_uniform_integers")
