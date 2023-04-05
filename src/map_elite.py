import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import math
import json
from datetime import datetime

from species import Species

class MAP_Elite:
    def __init__(self,b_range,height: int = 20, width: int = 20,  num_iterations: int = 5000 , pop_size: int = 10) -> None:
        self.archive = {}
        self.height = height
        self.width = width
        self.num_iterations = num_iterations
        self.pop_size = pop_size
        self.b_range = b_range

        #To plot the progress
        self.coverages = []
        self.pop = []
        self.means = []

        #Functions
        self.fitness_fn = self.fitness
        self.mutate_fn = self.mutate


    def init_archive(self, size : int, generate):
        for _ in range(size):
            g = generate()
            f, b = self.fitness_fn(g)
            self.add_to_archive(Species(g, b, f))
    
    def add_archive(self, pheno):
        b,f = self.fitness_fn(pheno)
        self.add_to_archive(Species(pheno,b,f))

    def fitness(self, genotype):
        """
        Compute the fitness function and it's behaviour based on the genotype.
        """
        pass

    def generate_pfsm(self):
        pass

    def mutate(self,x):
        pass

    def map_elite(self):
        self.pop = [random.choice(list(self.archive.values())).genotype for _ in range(self.pop_size)]
        for _ in tqdm(range(self.num_iterations)):
            # self.display_archive()

            #Compute the fitness function for each individual of the population
            for ind in range(self.pop_size):
                # Compute the fitness and behaviour
                b,f = self.fitness_fn(self.pop[ind])
                self.add_to_archive(Species(self.pop[ind],b,f))

            #Refill the population randomly and mutate the individual
            self.pop = [random.choice(list(self.archive.values())).genotype for _ in range(self.pop_size)]
            self.mutate_fn(self.pop)

            coverage, mean = self.qd_scores()
            self.coverages += [coverage]
            self.means += [mean]


    def add_to_archive(self, species: Species):
        """
        Map the species behaviour into the archive,
        and store it only if it does not exist or its fitness value is higher than the previous species of the cell.
        """ 
        print(species.behavior)       
        
        if species.behavior[0] < self.b_range[0][1]: 
            x = math.floor((abs(self.b_range[0][0]) + species.behavior[0]) * (self.width -1)/(abs(self.b_range[0][1]) + abs(self.b_range[0][0]) ))
        else:
            x = self.width -1
        
        if species.behavior[1] < self.b_range[1][1]:
            y = math.floor((abs(self.b_range[1][0]) + species.behavior[1]) *(self.height - 1)/(abs(self.b_range[1][1]) + abs(self.b_range[1][0])) )
        else:
            y = self.height -1

        if (x, y) not in self.archive or self.archive[(x, y)].fitness < species.fitness:
            self.archive[(x,y)] = species
            species.niche = (x,y)

    def qd_scores(self):
        """
        Compute the coverage and the mean fitness of the archive
        """
        coverage = len(self.archive) / float(self.height * self.width)
        fit_list = [x.fitness for x in list(self.archive.values())]
        mean = sum(fit_list) / float(self.height * self.width)
        return coverage, mean
    
    def display_progress(self):
        plt.figure(figsize=(5,3))
        plt.subplot(1, 2, 1)
        plt.plot(self.coverages)
        plt.title("coverage")

        plt.subplot(1,2, 2)
        plt.plot(self.means)
        plt.title("mean fitness")
        plt.show()

    def display_archive(self):
        """
        Utility function to display the archive
        """
        fit = np.zeros((self.height, self.width))
        m_min = 1e10
        m_max = 0
        for ((x,y), s) in self.archive.items():
            fit[x,y] = s.fitness
            if s.fitness < m_min:
                m_min = s.fitness
            if s.fitness > m_max:
                m_max = s.fitness
        plt.imshow(np.array(fit))
        plt.clim(m_min, m_max)
        
        # plt.xlim(self.b_range[0][0],self.b_range[0][1])
        # plt.ylim(self.b_range[1][0],self.b_range[1][1])
        plt.show()
        # fig.canvas.draw()
        return m_min, m_max
    
    def set_fitness(self,fitness_fn):
        self.fitness_fn = fitness_fn
    
    def set_mutate(self, mutate_fn):
        self.mutate_fn = mutate_fn

    def save_archive(self):
        # f = open(f'out/archive/{datetime.now().timestamp()}.json', 'w')
        # with open(f'../out/archive/{datetime.now().timestamp()}.json','w') as file:
        # json.dump(self.archive,f)
        pass