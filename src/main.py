from qdpy import algorithms, containers, benchmarks, plots
from qdpy.base import ParallelismManager

import os,math
import numpy as np
import matplotlib.pyplot as plt
from functools import partial


plot_path = os.path.join("out/")

def eval_fn(ind):
    """An example evaluation function. It takes an individual as input, and returns the pair ``(fitness, features)``,
       where ``fitness`` and ``features`` are sequences of scores.
    """
    normalization = sum(ind)
    k = 10.
    score = 1. - sum(( math.cos(k * ind[i]) * math.exp(-(ind[i]*ind[i])/2.) for i in range(len(ind)))) / float(len(ind))
    fit0 = sum((x * math.sin(abs(x) * 2. * math.pi) for x in ind)) / normalization
    fit1 = sum((x * math.cos(abs(x) * 2. * math.pi) for x in ind)) / normalization
    features = list(ind[:])
    features = (fit0, fit1)
    return (score,), features

# Define the number of dimensions
n_dim = 3

# Create container and algorithm. Here we use MAP-Elites, by illuminating a Grid container by evolution.
grid = containers.Grid(shape=(64,64), max_items_per_bin=1, fitness_domain=((-math.pi, math.pi),), features_domain=((0., 1.), (0., 1.)))
algo = algorithms.RandomSearchMutPolyBounded(grid, budget=30000, batch_size=500,
        dimension=n_dim, optimisation_task="minimisation", name = "MapElite")

# Create a logger to pretty-print everything and generate output data files
logger = algorithms.AlgorithmLogger(algo,log_base_path=plot_path)

fitness_fn = partial(eval_fn,n_dim)
# Run illumination process !
with ParallelismManager("none") as pMgr:
        best = algo.optimise(eval_fn, executor = pMgr.executor, batch_mode=False) # Disable batch_mode (steady-state mode) to ask/tell new individuals without waiting the completion of each batch

# Print results info
print(algo.summary())

# Plot the results
# plots.default_plots_grid(logger)
# Create plot of the performance grid
plot_path = os.path.join("out/performancesGrid.pdf")
plots.plotGridSubplots(grid.quality_array[... ,0], plot_path, plt.get_cmap("nipy_spectral_r"), grid.features_domain, grid.fitness_domain[0], nbTicks=None)
print("\nA plot of the performance grid was saved in '%s'." % os.path.abspath(plot_path))

max_activity = np.max(grid.activity_per_bin)
plots.plotGridSubplots(grid.activity_per_bin, plot_path, plt.get_cmap("Reds", max_activity), grid.features_domain, [0, max_activity], nbTicks=None)


