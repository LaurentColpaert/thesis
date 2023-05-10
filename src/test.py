import numpy as np
from behaviour import Behaviour, behaviours
from genetic.genetic import Genetic
from simulation import Mission, Simulation
import random
# pfsm = "--fsm-config --nstates 2 --s0 2  --n0 1 --n0x0 0 --c0x0 3 --w0x0 4.8 --p0x0 4 --s1 4 --att1 0.49 --n1 1 --n1x0 0 --c1x0 1 --p1x0 0.29 "
# sim = Simulation(Behaviour(behaviours.AAC,behaviours.AAC),Mission.AAC, visualization=False)
# fea = []
# sim.pfsm = pfsm
# for _ in range(20):
#     b,f = sim.run_simulation()
#     fea.append(f)

# print(f)
# print("mean", sum(f)/len(f))
from tqdm import tqdm
def mutate(pop: list):
    genetic = Genetic()

    #Transform into genotype to allow mutation and crossover
    pop = [genetic.toGenotype(i) for i in pop]

    new_pop = []
    for i in range(len(pop)):
        if i == len(pop)-1:
            g1,g2 = genetic.crossover(pop[i],pop[-1])
        else:
            g1,g2 = genetic.crossover(pop[i],pop[i+1])
        new_pop.extend((g1, g2))
    new_pop = [genetic.mutate(geno,0.075) for geno in new_pop]
    return [genetic.toPhenotype(geno) for geno in new_pop]


iteration = 10
size = 10
pfsms = []
n = 622
genetic = Genetic()
temp_list = []
for _ in range(size):
    binary_string = ''.join([str(random.randint(0, 1)) for _ in range(n)])
    pfsms.append(genetic.toPhenotype(binary_string))
    temp_list.append(genetic.toPhenotype(binary_string))

for i in tqdm(range(iteration)):
    new_list = mutate(pop=temp_list)
    new_list = random.sample(new_list, size)
    # new_list = random.sample(pfsms, 32)
    pfsms.extend(new_list)
    temp_list = new_list


print(len(pfsms))
print(len(np.unique(np.array(pfsms))))