import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import random
import math
import json
from datetime import datetime
from behaviour import Behaviour,SIZE, behaviours

from species import Species

class MAP_Elite:
    def __init__(self,behaviour : Behaviour,n_bin: int = 20,  num_iterations: int = 5000 , pop_size: int = 10) -> None:
        self.archive = {}
        col_names = list(range(1, 42))
        col_names.append('geno')
        col_names.append('behaviour')
        col_names.append('fitness')
        self.archive_db = pd.DataFrame(columns=col_names)
        self.n_bin = n_bin
        self.num_iterations = num_iterations
        self.pop_size = pop_size
        self.behaviour = behaviour
        self.b_range = [behaviour.range1, behaviour.range2]
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
            f, b = self.fitness_fn(g,self.behaviour)
            self.add_to_archive(Species(g, b, f))
    
    def add_archive(self, pheno):
        b,f = self.fitness_fn(pheno,self.behaviour)
        p = self.compute_point_space(b)
        # self.add_to_archive(Species(pheno,b,f))
        self.add_archive_db(Species(pheno,b,f,p))

    def add_archive_db(self,species : Species) -> None:
        to_add = species.niche
        to_add.append(species.genotype)
        to_add.append(species.behavior)
        to_add.append(species.fitness)

        self.archive_db.loc[len(self.archive_db)] = to_add

    def compute_point_space(self, behaviours : list) -> list:
        point = []
        for i in range(len(behaviours)):
            b_range = self.behaviour.get_range_position(i)
            if behaviours[i] < b_range[1]: 
                x = math.floor((abs(b_range[0]) + behaviours[i]) * (self.n_bin -1)/(abs(b_range[1]) + abs(b_range[0])))
            else:
                x = self.n_bin -1
            point.append(x)
        return point
    
    def fitness(self, genotype):
        """
        Compute the fitness function and it's behaviour based on the genotype.
        """
        pass

    def generate_pfsm(self):
        pass

    def mutate(self,x):
        pass

    def select_population(self) -> list:
        rdm = self.archive_db["geno"].sample(self.pop_size)
        return rdm.values
    
    def map_elite(self):

        self.pop = self.select_population()
        for _ in tqdm(range(self.num_iterations)):
            # self.display_archive()

            #Compute the fitness function for each individual of the population
            for ind in range(self.pop_size):
                # Compute the fitness and behaviour
                b,f = self.fitness_fn(self.pop[ind],self.behaviour)
                p = self.compute_point_space(b)
                self.add_archive_db(Species(self.pop[ind],b,f,p))

            #Refill the population randomly and mutate the individual
            self.pop = self.select_population()
            self.mutate_fn(self.pop)

            coverage, mean = self.qd_scores()
            self.coverages += [coverage]
            self.means += [mean]


    def add_to_archive(self, species: Species):
        """
        Map the species behaviour into the archive,
        and store it only if it does not exist or its fitness value is higher than the previous species of the cell.
        """         
        if species.behavior[0] < self.b_range[0][1]: 
            x = math.floor((abs(self.b_range[0][0]) + species.behavior[0]) * (self.n_bin -1)/(abs(self.b_range[0][1]) + abs(self.b_range[0][0]) ))
        else:
            x = self.n_bin -1
        
        if species.behavior[1] < self.b_range[1][1]:
            y = math.floor((abs(self.b_range[1][0]) + species.behavior[1]) *(self.n_bin - 1)/(abs(self.b_range[1][1]) + abs(self.b_range[1][0])) )
        else:
            y = self.n_bin -1
        print(f"The new species is ({x},{y}) with a fitness of {species.fitness}")
        if (x, y) not in self.archive or self.archive[(x, y)].fitness < species.fitness:
            self.archive[(x,y)] = species
            species.niche = (x,y)

    def qd_scores(self):
        """
        Compute the coverage and the mean fitness of the archive
        """
        coverage = len(self.archive) / float(self.n_bin * self.n_bin)
        fit_list = [x.fitness for x in list(self.archive.values())]
        mean = sum(fit_list) / float(self.n_bin * self.n_bin)
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

    def fill_archive(self, b : Behaviour) -> dict:
        archive = {}
        fit = np.zeros((self.n_bin,self.n_bin))
        index1 = b.r1 if b.b1 == behaviours.PHI else behaviours.DUTY_FACTOR.value
        index2 = b.r2 if b.b2 == behaviours.PHI else behaviours.DUTY_FACTOR.value
        result = self.archive_db[[index1,index2,"geno","behaviour","fitness"]]
        for index, row in result.iterrows():
            species = Species(row["geno"],row["behaviour"],row["fitness"])
            x = row[index1]
            y = row[index2]
            if (x, y) not in self.archive or self.archive[(x, y)].fitness < species.fitness:
                archive[(x,y)] = species
        return archive
    
    def display_archive(self, b : Behaviour) -> None:
        """
        Utility function to display the archive
        """
        b_range = [b.range1, b.range2]
        fit = np.zeros((self.n_bin, self.n_bin))
        m_min = 1e10
        m_max = 0
        archive = self.fill_archive(b)
        for ((x,y), s) in archive.items():
            fit[x,y] = s.fitness
            if s.fitness < m_min:
                m_min = s.fitness
            if s.fitness > m_max:
                m_max = s.fitness

        plt.imshow(fit,cmap="viridis", vmin=0, vmax=20, extent=[b_range[0][0],b_range[0][1],b_range[1][1],b_range[1][0]])
        plt.colorbar()
        name_x = f"{b.b1.name} - {b.r1}" if b.b1 == behaviours.PHI else behaviours.DUTY_FACTOR.name
        name_y = f"{b.b2.name} - {b.r2}" if b.b2 == behaviours.PHI else behaviours.DUTY_FACTOR.name
        plt.xlabel(name_x)
        plt.ylabel(name_y)
        plt.title(f"Map-Elites with {self.num_iterations} iterations with features : {name_x} and {name_y}")
        plt.show()
        # fig.canvas.draw()

    def set_fitness(self,fitness_fn):
        self.fitness_fn = fitness_fn
    
    def set_mutate(self, mutate_fn):
        self.mutate_fn = mutate_fn

    def save_archive(self):
        # f = open(f'out/archive/{datetime.now().timestamp()}.json', 'w')
        with open(f'home/laurent/Documents/Polytech/MA2/thesis/out/archive/{str(datetime.now().timestamp()).replace(".","_")}.json','w') as file:
            json.dump(self.archive,file)
        