import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from qdpy.algorithms import *
from qdpy.containers import *
from qdpy.benchmarks import *
from qdpy.base import *
from qdpy.plots import *
from qdpy import tools

import os
import numpy as np
import random
from functools import partial
import yaml


def eval_fn(ind):
    """An example evaluation function. It takes an individual as input, and returns the pair ``(fitness, features)``, where ``fitness`` and ``features`` are sequences of scores."""
    normalization = sum(ind)
    k = 10.
    score = 1. - sum(( math.cos(k * ind[i]) * math.exp(-(ind[i]*ind[i])/2.) for i in range(len(ind)))) / float(len(ind))
    fit0 = sum((x * math.sin(abs(x) * 2. * math.pi) for x in ind)) / normalization
    fit1 = sum((x * math.cos(abs(x) * 2. * math.pi) for x in ind)) / normalization
    features = (fit0, fit1)
    return (score,), features


def complex_rastrigin():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None, help="Numpy random seed")
    parser.add_argument('-p', '--parallelismType', type=str, default='concurrent', help = "Type of parallelism to use (none, concurrent, scoop)")
    parser.add_argument('-c', '--configFile', type=str, default='/home/laurent/Documents/Polytech/MA2/thesis/src/conf/rastrigin.yaml', help = "Path of the configuration file")
    parser.add_argument('-o', '--outputDir', type=str, default='/home/laurent/Documents/Polytech/MA2/thesis/out', help = "Path of the output log files")
    args = parser.parse_args()


    # Retrieve configuration from configFile
    config = yaml.safe_load(open(args.configFile))
    print("Retrieved configuration:")
    print(config)
    print("\n------------------------\n")

    # Find where to put logs
    log_base_path = config.get("log_base_path", ".") if args.outputDir is None else args.outputDir

    # Find random seed
    if args.seed is not None:
        seed = args.seed
    elif "seed" in config:
        seed = config["seed"]
    else:
        seed = np.random.randint(1000000)

    # Update and print seed
    np.random.seed(seed)
    random.seed(seed)
    print("Seed: %i" % seed)


    # Create containers and algorithms from configuration 
    factory = Factory()
    assert (
        "containers" in config
    ), "Please specify configuration entry 'containers' containing the description of all containers."
    factory.build(config["containers"])
    assert (
        "algorithms" in config
    ), "Please specify configuration entry 'algorithms' containing the description of all algorithms."
    factory.build(config["algorithms"])
    assert (
        "main_algorithm_name" in config
    ), "Please specify configuration entry 'main_algorithm' containing the name of the main algorithm."
    algo = factory[config["main_algorithm_name"]]
    container = algo.container

    # Define evaluation function
    eval_fn = partial(illumination_rastrigin_normalised, nb_features = len(container.shape))

    # Create a logger to pretty-print everything and generate output data files
    logger = TQDMAlgorithmLogger(algo, log_base_path=log_base_path, config=config)

    # Run illumination process !
    with ParallelismManager(args.parallelismType) as pMgr:
        best = algo.optimise(eval_fn, executor = pMgr.executor, batch_mode=False) # Disable batch_mode (steady-state mode) to ask/tell new individuals without waiting the completion of each batch


    # Print results info
    print("\n------------------------\n")
    print(algo.summary())

    # Transform the container into a grid, if needed
    if isinstance(container, containers.Grid):
        grid = container
    else:
        print("\n{:70s}".format("Transforming the container into a grid, for visualisation..."), end="", flush=True)
        grid = container.to_grid(container.shape, features_domain=container.features_domain)
        print("\tDone !")
    print(grid.summary())

    # Create plot of the performance grid
    plot_path = os.path.join(log_base_path, "performancesGrid.pdf")
    plotGridSubplots(grid.quality_array[... ,0], plot_path, plt.get_cmap("nipy_spectral_r"), grid.features_domain, grid.fitness_domain[0], nbTicks=None)
    print("\nA plot of the performance grid was saved in '%s'." % os.path.abspath(plot_path))

    plot_path = os.path.join(log_base_path, "activityGrid.pdf")
    max_activity = np.max(grid.activity_per_bin)
    plotGridSubplots(grid.activity_per_bin, plot_path, plt.get_cmap("Reds", max_activity), grid.features_domain, [0, max_activity], nbTicks=None)

# MODELINE "{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker


if __name__ == "__main__":
    complex_rastrigin()
 