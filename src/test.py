# import pandas as pd

# col_names = list(range(1, 42))
# col_names.append('geno')
# col_names.append('behaviour')
# col_names.append('fitness')
# archive_db = pd.DataFrame(columns=col_names)
# values = list(range(41))
# values.append("--fsm-config")
# values.append([1.0,0.2,0.6])
# values.append(1.0)
# archive_db.loc[len(archive_db)] = values
# values = list(range(41))
# values.append("--fsm-config")
# values.append([1.0,0.2,0.6])
# values.append(1.0)
# archive_db.loc[len(archive_db)] = values
# values = list(range(41))
# values.append("--fsm-config")
# values.append([1.0,0.2,0.6])
# values.append(1.0)
# archive_db.loc[len(archive_db)] = values
# print(archive_db.columns)
# # rdm = archive_db["geno"].sample(3)
# print(archive_db[[2,3,"geno"]])

import random
from genetic.genetic import Genetic
from main import mutate
g = Genetic()

l = []
random.seed(0)
for _ in range(10):
        binary_string = ''.join([str(random.randint(0, 1)) for _ in range(622)])
        l.append(g.toPhenotype(binary_string))
pfsms =[
    "--fsm-config --nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.70 --s1 2 --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1 --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.50 --n3x1 2 --c3x1 5 --p3x1 0.62",
    "--fsm-config --nstates 4 --s0 2 --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.28 --s1 4 --att1 3.57 --n1 3 --n1x0 1 --c1x0 4 --w1x0 6.31 --p1x0 8 --n1x1 0 --c1x1 2 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 1 --c2x0 0 --p2x0 0.95 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.60 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77",
    "--fsm-config --nstates 4 --s0 2  --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.7 --s1 2  --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 1 --c2x0 0 --p2x0 0.95 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.6 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77",
    "--fsm-config --nstates 4 --s0 2  --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.28 --s1 4 --att1 3.5700000000000003 --n1 3 --n1x0 1 --c1x0 4 --w1x0 6.31 --p1x0 8 --n1x1 0 --c1x1 2 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 0 --c2x0 3 --w2x0 0.0 --p2x0 6 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.6 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77",
    "--fsm-config --nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.77 --n0x1 2 --c0x1 0 --p0x1 0.7 --s1 2  --n1 3 --n1x0 0 --c1x0 4 --w1x0 14.01 --p1x0 9 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 11.77 --p1x2 3 --s2 1  --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.77 --p2x0 4 --s3 4 --att3 4.3500000000000005 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.5 --n3x1 2 --c3x1 1 --p3x1 0.3"
        ]


for p in l:
    print(len(g.toGenotype(p)))

pfsm = mutate(l)
for p in pfsm:
    print(len(g.toGenotype(p)))

# print(l[2])

# p = "--fsm-config --nstates 3 --s0 0 --rwm0 26 --s1 2  --s2 2  --n2 1 --n2x0 0 --c2x0 2 --p2x0 0.19" 

# print(len(g.toGenotype(p,True)))

# # p = "--fsm-config --nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.70 --s1 2 --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1 --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.50 --n3x1 2 --c3x1 5 --p3x1 0.62"


# # print(len(g.toGenotype(p,True)))

# print(g.chain)