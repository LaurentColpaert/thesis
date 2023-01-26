from qdpy import algorithms, containers, benchmarks, plots
import os
import numpy as np
import matplotlib.pyplot as plt

# Create container and algorithm. Here we use MAP-Elites, by illuminating a Grid container by evolution.
grid = containers.Grid(shape=(100,100), max_items_per_bin=1, fitness_domain=((0., 10.),), features_domain=((0., 10.), (0., 10.)))
algo = algorithms.RandomSearchMutPolyBounded(grid, budget=100000, batch_size=500,
        dimension=3, optimisation_task="maximisation")

# Create a logger to pretty-print everything and generate output data files
logger = algorithms.AlgorithmLogger(algo)

# Define evaluation function
eval_fn = algorithms.partial(benchmarks.illumination_rastrigin_normalised,
        nb_features = len(grid.shape))

# Run illumination process !
best = algo.optimise(eval_fn)

# Print results info
print(algo.summary())

# Plot the results
# plots.default_plots_grid(logger)

# Create plot of the performance grid
plot_path = os.path.join("performancesGrid.pdf")
plots.plotGridSubplots(grid.quality_array[... ,0], plot_path, plt.get_cmap("nipy_spectral_r"), grid.features_domain, grid.fitness_domain[0], nbTicks=None)
print("\nA plot of the performance grid was saved in '%s'." % os.path.abspath(plot_path))

max_activity = np.max(grid.activity_per_bin)
plots.plotGridSubplots(grid.activity_per_bin, plot_path, plt.get_cmap("Reds", max_activity), grid.features_domain, [0, max_activity], nbTicks=None)


