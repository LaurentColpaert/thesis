import numpy as np
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import random

from species import Species

class MAP_Elite:
    def __init__(self, num_iterations: int = 50 , batch_size: int = 500) -> None:
        self.archive = {}
        self.height = 0
        self.width = 0
        self.num_iterations = num_iterations
        self.batch_size = batch_size

        #To plot the progress
        self.coverages = []
        self.means = []

    def init_archive(self, size : int):
        archive = {}
        for _ in range(size):
            g = self.generate_pfsm()
            f, b = self.fitness(g)
            self.add_to_archive(archive, Species(g, b, f))
        return archive
    
    def fitness(self, genotype):
        """
        Compute the fitness function and it's behaviour based on the genotype.
        """
        pass

    def mutate(self):
        pass

    def map_elite(self):
        for _ in tqdm(range(self.num_iterations)):
            # self.display_archive()
            for _ in range(self.batch_size):
                # Pick an existing random point in the archive
                x = random.choice(list(self.archive.values()))
                # Mutate it
                g = self.mutate()
                # Compute the fitness and behaviour
                f,b = self.fitness(g)

                self.add_to_archive(Species(g,b,f))
        coverage, mean = self.qd_scores()
        self.coverages += [coverage]
        self.means += [mean]


    def add_to_archive(self, species: Species):
        """
        Map the species behaviour into the archive,
        and store it only if it does not exist or its fitness value is higher than the previous species of the cell.
        """
        n = species.behavior * np.array([self.height, self.width])
        x,y = min(round(n[0]), self.height-1), min(round(n[1]), self.width-1)
        if (x, y) not in self.archive or self.archive[(x, y)].fitness < species.fitness:
            self.archive[(x,y)] = species
            species.niche = (x,y)

    def qd_scores(self):
        """
        Compute the coverage and the mean fitness of the archive
        """
        coverage = len(self) / float(self.height * self.width)
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
        for ((x,y), s) in self.items():
            fit[x,y] = s.fitness
            if s.fitness < m_min:
                m_min = s.fitness
            if s.fitness > m_max:
                m_max = s.fitness
        plt.imshow(np.array(fit))
        plt.clim(m_min, m_max)

        # fig.canvas.draw()
        return m_min, m_max