import pandas as pd

# col_names = list(range(1, 42))
# col_names = [str(i) for i in col_names]
# col_names.append('geno')
# col_names.append('behaviour')
# col_names.append('fitness')
# archive_db = pd.DataFrame(columns=col_names)
# values = list(range(41))
# values.append("--fsm-config")
# values.append([1.0,0.2,0.6])
# values.append(3.0)
# archive_db.loc[len(archive_db)] = values
# print(matching_rows)
# values = list(range(41))
# values.append("--fsm-config")
# values.append([1.0,0.2,0.6])
# values.append(4.0)
# archive_db.loc[len(archive_db)] = values
# values = list(range(41))
# values.append("--fsm-config")
# values.append([1.0,0.2,0.6])
# values.append(5.0)
# archive_db.loc[len(archive_db)] = values
# print(archive_db.columns)
# # rdm = archive_db["geno"].sample(3)
# print(archive_db[[2,3,"geno"]])


import ast
from functools import partial
import multiprocessing
import subprocess
from behaviour import Behaviour,behaviours
from simulation import Simulation
from main import fitness
import re

# pfsms =[
#     "--fsm-config --nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.70 --s1 2 --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1 --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.50 --n3x1 2 --c3x1 5 --p3x1 0.62"
#     ,"--fsm-config --nstates 4 --s0 2 --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.28 --s1 4 --att1 3.57 --n1 3 --n1x0 1 --c1x0 4 --w1x0 6.31 --p1x0 8 --n1x1 0 --c1x1 2 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 1 --c2x0 0 --p2x0 0.95 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.60 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77",
#     "--fsm-config --nstates 4 --s0 2  --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.7 --s1 2  --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 1 --c2x0 0 --p2x0 0.95 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.6 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77",
#     "--fsm-config --nstates 4 --s0 2  --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.28 --s1 4 --att1 3.5700000000000003 --n1 3 --n1x0 1 --c1x0 4 --w1x0 6.31 --p1x0 8 --n1x1 0 --c1x1 2 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 0 --c2x0 3 --w2x0 0.0 --p2x0 6 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.6 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77",
#     "--fsm-config --nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.77 --n0x1 2 --c0x1 0 --p0x1 0.7 --s1 2  --n1 3 --n1x0 0 --c1x0 4 --w1x0 14.01 --p1x0 9 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 11.77 --p1x2 3 --s2 1  --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.77 --p2x0 4 --s3 4 --att3 4.3500000000000005 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.5 --n3x1 2 --c3x1 1 --p3x1 0.3"
# ]
# behaviour = Behaviour(behaviours.DUTY_FACTOR,behaviours.DUTY_FACTOR)
# # sim = Simulation(behaviour=behaviour)
# # sim.run_simulation_std_out()
# test = []

# fitness_fn_with_behaviour = partial(fitness,behaviour = behaviour)
# with multiprocessing.Pool() as pool:
#     results = pool.map(fitness_fn_with_behaviour, pfsms)
# print("the result are \n", results[0][1])

# db = pd.read_csv("save-300iter.csv")
# value = [35,27,27,24,22,20,19,18,13,13,11,8,7,6,6,5,5,4,4,3,27,27,22,22,19,18,17,17,15,14,11,8,7,5,5,5,4,4,4,4,34]
# print(len(db))
# print(db.loc[db["1"]==39])
# # matching_rows = db.loc[' & '.join([f'(db["{col}"]== {val})' for col, val in zip(db.columns[:41], value)])]
# # matching_rows = db[(db.iloc[:, :41] == value).all(axis=1)]
# # row_exists = db.iloc[:, :41].isin().iloc[0]).all(axis=1).any()
# # row_exists = db[db.apply(lambda x: x.equals(pd.DataFrame([39], columns=db.columns[:1]).iloc[0]), axis=1)]
# # print(matching_rows.index[0])
# print(db.iloc[0]['fitness'])

# val = [0.6520735817813579, 0.5523403023452463, 0.3659521917740265, 0.3285535710694365, 0.32631688639252476, 0.31914092116098325, 0.25276507652033664, 0.24461881633345287, 0.24136051113501972, 0.20701223515855424, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 1.0, 1.0, 0.9763731621533396, 0.8480855483613915, 0.5371496542636469, 0.4610846524772533, 0.4326233938986869, 0.4162829913382828, 0.32620554065718216, 0.13678040543824208, 0.12389038571298285, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 1.0, 1.0, 1.0, 1.0, 1.0, 0.703348015879769, 0.5766372139672586, 0.45009698939590526, 0.368030094624154, 0.265878569407545, 0.18806800545226887, 0.14685497600841188, 0.08815278299932652, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 1.0, 0.8515065637000483, 0.7240126999893763, 0.529783628300412, 0.5063428350505013, 0.4327743020469157, 0.22173589338319838, 0.16079129512497797, 0.15086617052335105, 0.11375570858281722, 0.08713083826332711, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.009999999999999995, 0.8748324118331746, 0.8748324118331746, 0.8085336074641987, 0.8085336074641987, 0.7907368719580303, 0.7907368719580303, 0.7687449289875586, 0.7435808314648171, 0.730784119607298, 0.6774947053923654, 0.6774947053923654, 0.6388187702622543, 0.621862585123182, 0.6185754298629427, 0.6185754298629427, 0.5921319743004512, 0.5294616550002491, 0.4400444759584925, 0.4400444759584925, 0.4005322280893593, 0.0425]
# print(len(val))

# df = pd.read_csv("/home/laurent/Documents/Polytech/MA2/thesis/save-300iter_possible-dup.csv")

# print(df["fitness"].value_counts().sort_index())

# dic = {
#     "Name" : ["Laurent","Laurent","Laurent", "Sebastien", "Sebastien", "Sebastien"],
#     "Day" : ["Lundi","Mardi","Mercredi","Lundi","Mardi","Mercredi"],
#     "quantity" : [1,2,3,4,5,6],
#     "price" : [10,10,10,10,10,10]
# }

# df = pd.DataFrame(dic)

# print(df.groupby(['Name',"Day"]).apply(lambda x: x["quantity"] * x["price"]))

from genetic.genetic import Genetic
pfsm = "--fsm-config --nstate 2 --s0 4 --att0 5 --n0 1 --n0x0 0 --c0x0 2 -p0x0 0.5 --s1 0 --rwm1 20"
g = Genetic()
print(g.toGenotype(pfsm))
print(len(g.toGenotype(pfsm)))