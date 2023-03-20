from math import *
import random
import numpy as np
from map_elite import MAP_Elite

RANGE = 20

def rastrigin(ind, a=10.):
    """Rastrigin test function."""
    n = float(len(ind))
    return a * n + sum(x * x - a * cos(2. * pi * x) for x in ind),ind

def generate_random():
    return [random.uniform(-RANGE,RANGE),random.uniform(-RANGE,RANGE)]

def mutate(ind):
    return [clamp(ind[0] + random.uniform(-1,1),-RANGE,RANGE), clamp(ind[1] + random.uniform(-1,1),-RANGE,RANGE)]
def mutate_test(ind):
    return ind + np.random.normal(0, 0.1, len(ind))

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

if __name__ == '__main__':

    map_elite = MAP_Elite(b_range=[[-RANGE,RANGE],[-RANGE,RANGE]],width=30,height=30,num_iterations=1000,batch_size=100)
    map_elite.set_fitness(rastrigin)
    map_elite.set_mutate(mutate)
    map_elite.init_archive(10,generate=generate_random)
    map_elite.map_elite()

    map_elite.display_archive()
    map_elite.display_progress()
