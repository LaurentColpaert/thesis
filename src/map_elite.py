import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import math

from species import Species

class MAP_Elite:
    def __init__(self,b_range,height: int = 20, width: int = 20,  num_iterations: int = 50 , batch_size: int = 500) -> None:
        self.archive = {}
        self.height = height
        self.width = width
        self.num_iterations = num_iterations
        self.batch_size = batch_size
        self.b_range = b_range

        #To plot the progress
        self.coverages = []
        self.means = []

        #Functions
        self.fitness_fn = self.fitness
        self.mutate_fn = self.mutate


    def init_archive(self, size : int, generate):
        for _ in range(size):
            g = generate()
            f, b = self.fitness_fn(g)
            self.add_to_archive(Species(g, b, f))
    
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
        for i in tqdm(range(self.num_iterations)):
            # if i % 100 == 0:
                # print(f"Step {i}")
            # self.display_archive()
            for _ in range(self.batch_size):
                # Pick an existing random point in the archive
                x = random.choice(list(self.archive.values()))
                # Mutate it
                g = self.mutate_fn(x.genotype)
                # print("g is ", g)
                # Compute the fitness and behaviour
                f,b = self.fitness_fn(g)

                self.add_to_archive(Species(g,b,f))
            coverage, mean = self.qd_scores()
            self.coverages += [coverage]
            self.means += [mean]


    def add_to_archive(self, species: Species):
        """
        Map the species behaviour into the archive,
        and store it only if it does not exist or its fitness value is higher than the previous species of the cell.
        """        

        if species.behavior[0] != self.b_range[0][1]: 
            x = math.floor((abs(self.b_range[0][0]) + species.behavior[0]) * (self.width -1)/(abs(self.b_range[0][1]) + abs(self.b_range[0][0]) ))
        else:
            x = self.width -1
        
        if species.behavior[1] != self.b_range[1][1]:
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
        fig = plt.figure(figsize=(5,3))
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
        plt.show()
        # fig.canvas.draw()
        return m_min, m_max
    
    def set_fitness(self,fitness_fn):
        self.fitness_fn = fitness_fn
    
    def set_mutate(self, mutate_fn):
        self.mutate_fn = mutate_fn