from experiments_csv import single_plot_results, multi_plot_results
from matplotlib import pyplot as plt


# single_plot_results(
#      "results/dynamic_programming_variants_1.csv", save_to_file=True,
#      filter={}, 
#      x_field="numitems", y_field="runtime", z_field=["bitsperitem", "use_boolean_matrix"], mean=True, 
#      legend_properties={"size":6}, xlim=(0,30), ylim=(0,30))

# multi_plot_results(
#      "results/complete_greedy_variants_5.csv", save_to_file=True,
#      filter={"use_heuristic_2":True, "use_lower_bound":False}, 
#      x_field="numitems", y_field="runtime", z_field=["objective", "use_heuristic_3"], mean=True, 
#      subplot_field = "bitsperitem", subplot_rows=1, subplot_cols=3, sharey=True, 
#      legend_properties={"size":6}, ylim=(0,30))

# multi_plot_results(
#      "results/complete_greedy_variants_6.csv", save_to_file=True,
#      filter={}, 
#      x_field="numitems", y_field="runtime", z_field=["use_lower_bound", "use_set_of_seen_states"], mean=True, 
#      subplot_field = "bitsperitem", subplot_rows=1, subplot_cols=3, sharey=True, sharex=True,
#      legend_properties={"size":6}, ylim=(0,30))

# multi_plot_results(
#      "results/partition_uniform_integers.csv", save_to_file=True,
#      filter={}, 
#      x_field="numitems", y_field="runtime", z_field=["algorithm"], mean=True, 
#      subplot_field = "bitsperitem", subplot_rows=1, subplot_cols=3, sharey=True, 
#      legend_properties={"size":6}, xlim=(0,30), ylim=(0,30))

# multi_plot_results(
#      "results/complete_greedy_variants_7.csv", save_to_file=True,
#      filter={}, 
#      x_field="numitems", y_field="runtime", z_field=["use_lower_bound", "use_fast_lower_bound", "use_set_of_seen_states", "use_dynamic_programming"], mean=True, 
#      subplot_field = "bitsperitem", subplot_rows=1, subplot_cols=3, sharey=True, sharex=True,
#      legend_properties={"size":6}, ylim=(0,30))

# multi_plot_results(
#      "results/karmarkar_karp_variants_1.csv", save_to_file=True,
#      filter={}, 
#      x_field="numitems", y_field="runtime", z_field="algorithm", mean=True, 
#      subplot_field = "bitsperitem", subplot_rows=2, subplot_cols=3, sharey=True, sharex=True,
#      legend_properties={"size":6}, ylim=(0,30), xlim=(0,30))

multi_plot_results(
     "results/complete_greedy_variants_8.csv", save_to_file=True,
     filter={}, 
     x_field="numitems", y_field="runtime", z_field=["use_lower_bound", "use_fast_lower_bound", "use_set_of_seen_states", "use_dynamic_programming"], mean=True, 
     subplot_field = "bitsperitem", subplot_rows=1, subplot_cols=3, sharey=True, sharex=True,
     legend_properties={"size":6}, ylim=(0,30))

