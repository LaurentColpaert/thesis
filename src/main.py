from math import *
import time
from genetic.genetic import Genetic
from map_elite import MAP_Elite

from simulation import Simulation

pfsms =[
    "--fsm-config --nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.70 --s1 2 --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1 --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.50 --n3x1 2 --c3x1 5 --p3x1 0.62",
    "--fsm-config --nstates 4 --s0 2 --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.28 --s1 4 --att1 3.57 --n1 3 --n1x0 1 --c1x0 4 --w1x0 6.31 --p1x0 8 --n1x1 0 --c1x1 2 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 1 --c2x0 0 --p2x0 0.95 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.60 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77",
    "--fsm-config --nstates 4 --s0 2  --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.7 --s1 2  --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 1 --c2x0 0 --p2x0 0.95 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.6 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77",
    "--fsm-config --nstates 4 --s0 2  --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.28 --s1 4 --att1 3.5700000000000003 --n1 3 --n1x0 1 --c1x0 4 --w1x0 6.31 --p1x0 8 --n1x1 0 --c1x1 2 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 0 --c2x0 3 --w2x0 0.0 --p2x0 6 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.6 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77",
    "--fsm-config --nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.77 --n0x1 2 --c0x1 0 --p0x1 0.7 --s1 2  --n1 3 --n1x0 0 --c1x0 4 --w1x0 14.01 --p1x0 9 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 11.77 --p1x2 3 --s2 1  --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.77 --p2x0 4 --s3 4 --att3 4.3500000000000005 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.5 --n3x1 2 --c3x1 1 --p3x1 0.3"
        ]
# pfsms =[
#     "--fsm-config --nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.70 --s1 2 --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1 --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.50 --n3x1 2 --c3x1 5 --p3x1 0.62"       ]

def fitness(phenotype):
    print("El phenotype is ", phenotype)
    sim = Simulation()
    sim.pfsm = phenotype
    b,f = sim.run_simulation()
    return b,f

def generate_random():
    pass

def mutate(pop: list):
    genetic = Genetic()

    #Transform into genotype to allow mutation and crossover
    pop = [genetic.toGenotype(i) for i in pop]

    new_pop = []
    for i in range(len(pop)):
        print(i)
        if i == len(pop)-1:
            g1,g2 = genetic.crossover(pop[i],pop[-1])
        else:
            g1,g2 = genetic.crossover(pop[i],pop[i+1])
        new_pop.extend((g1, g2))
    new_pop = [genetic.mutate(geno) for geno in new_pop]
    return [genetic.toPhenotype(geno) for geno in new_pop]
    

def fill_archive(m_e : MAP_Elite):
    for pheno in pfsms:
        m_e.add_archive(pheno)


if __name__ == '__main__':
    #TODO : try with a bigger number of bins
    m_e = MAP_Elite(b_range=[[0,1],[0,1]],num_iterations=25,pop_size=len(pfsms),height=40,width=40)
    m_e.set_fitness(fitness)
    fill_archive(m_e)
    print("[ARCHIVED] : initialized")
    m_e.set_mutate(mutate)

    m_e.map_elite()
    m_e.display_archive()
    m_e.display_progress()
    m_e.save_archive()

    # sim = Simulation()
    # sim.read_file()
    # print(sim.swarm_pos[-20:])
    # print(len(sim.swarm_pos))
    # print(sim.compute_features())


    

    