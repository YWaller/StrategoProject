# -*- coding: utf-8 -*-

from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt
import os


m = Model("Setup Generator")
m.ModelSense = GRB.MAXIMIZE

#setup values for defense/offensive dictionary; assign 0-11 a score for being useful for defense
#just a percentage of units they kill, with a bonus or reduction as deemed necessary by experience playing
keys = [0,1,2,3,4,5,6,7,8,9,10,11]

initialvalues = list()
for i in range(1,12):
    initialvalues.append(round(i/12.0,3))
    
#modify as needed
#            flag   spy   2     3      4      5     6     7      8      9     10    bomb
ivsattack = [0.0, 0.166, 0.5, 0.333, 0.333, 0.417, 0.5, 0.583, 0.667, 0.75, 0.833, 0.0917]
    
attack=dict(zip(keys,ivsattack))

#modify as needed
#            flag   spy   2     3      4      5     6     7      8      9     10    bomb
ivsdefense = [0.0, 0.266, 0.18, 0.35, 0.333, 0.357, 0.4, 0.483, 0.567, 0.65, 0.733, 0.917]

defense=dict(zip(keys,ivsdefense))

#use a 3d matrix of binary variables to establish if going to fill a cell with a piece number
vars = m.addVars(3,10,12, vtype=GRB.BINARY, name='Grid')
m.update()
nrow=3
ncol=10

#set flag location
decisionmatrix = np.zeros((12,3,10))
flagx=0
flagy=4
decisionmatrix[0,flagx,flagy] = 1
for i in range(nrow):
    for j in range(ncol):
        for v in range(12):
            if decisionmatrix[v,i,j] == 1:
                vars[i,j,v].LB = 1

#one unit per square            
m.addConstrs((vars.sum(i,j,'*') == 1
                 for i in range(nrow)
                 for j in range(ncol)), name='V') #'*' is wildcard

#no column can have three bombs
m.addConstrs((vars.sum('*',j,11) <= 2 
              for j in range(ncol)), name='Bombs') #note the not implemented error is solved by using >= or such, just > not in gurobi; solution could be infinitesimally close to  >x but not x 

#no row can have all the bombs, not a necessary constraint but helps produce sane setups
m.addConstrs((vars.sum(x,'*',11) <= 5 
              for x in range(nrow)), name='Bombs') #note the not implemented error is solved by using >= or such, just > not in gurobi; solution could be infinitesimally close to  >x but not x 


#unit count constraints
m.addConstr((vars.sum('*','*',0) == 1),name='Flag')
m.addConstr((vars.sum('*','*',11) == 6),name='Bombs')
m.addConstr((vars.sum('*','*',1) == 1),name='Spy')
m.addConstr((vars.sum('*','*',2) == 7),name='Scout')
m.addConstr((vars.sum('*','*',3) == 5),name='Miner')
m.addConstr((vars.sum('*','*',4) == 2),name='Sergeant')
m.addConstr((vars.sum('*','*',5) == 2),name='Lieutenant')
m.addConstr((vars.sum('*','*',6) == 2),name='Captain')
m.addConstr((vars.sum('*','*',7) == 1),name='Major')
m.addConstr((vars.sum('*','*',8) == 1),name='Colonel')
m.addConstr((vars.sum('*','*',9) == 1),name='General')
m.addConstr((vars.sum('*','*',10) == 1),name='Marshal')

#weights, aw attack dw defense
aw=1.0
dw=1.0

#Left right bias
leb=1.0
rib=1.0

#left right offense bias
lab=1.0
rab=1.0

#left right defense bias
ldb=1.0
rdb=1.0

#effective distance of discouraging clustering, unimplemented
ed=2

#sums the variable's attack rating by row, lower rows being higher, and the defense rating for distance from flag
#16**(1/2) returns 1 because that's integer division, so use **(.5)
#manhattan distance produces significantly better results than euclidean.
m.setObjective(quicksum(vars[x,y,z] * attack[z]*(aw/(3-x)) + vars[x,y,z] * defense[z]*(dw**(abs(x-flagx)+abs(y-flagy))) for x in range(nrow) for y in range(ncol) for z in range(12))+quicksum(vars[x,y,z]*leb+defense[z]*ldb+attack[z]*rdb for x in range(nrow) for y in range(ncol/2) for z in range(12))+quicksum(vars[x,y,z]*rib+defense[z]*rdb+ attack[z]*rab for x in range(nrow) for y in range(5,ncol) for z in range(12)))               

m.update()

#quicksum((-(vars[x,y,z]**3-vars[x,y,z]**2)/20) for x in range(x0*ed) for y in range(y0*ed) for v in range(12) for i0 in range(1,3) for y0 in range(1,3))

#m.computeIIS()
#m.write("model.ilp") the IIS is very useful
m.optimize()

#piecenumbers = list((1,1,7,5,2,2,2,1,1,1,1,6))
#print(sum([a*b for a,b in zip(piecenumbers,ivsdefense)])+sum([a*b for a,b in zip(piecenumbers,ivsattack)])) 
#this should be the same as the old objective function result:
#m.setObjective(quicksum(vars[x,y,z] * attack[z]*aw + vars[x,y,z] * defense[z]*dw for x in range(nrow) for y in range(ncol) for z in range(12)))

solution = m.getAttr('X', vars)
endmatrix = np.zeros((12,3,10))
plotmatrix = np.zeros((3,10))
count = 0
for x in range(nrow):
    for y in range(ncol):
        for z in range(12):
            endmatrix[z,x,y] = solution[x,y,z]
            if endmatrix[z,x,y] == 1.0:
                plotmatrix[x,y] = z
                count += 1

print count #should be 30

plotmatrix = plotmatrix.astype(int)

#let's plot the setup
fig, ax = plt.subplots(figsize=(3,10))

min_val, max_val, diff = 0, 10, 1

#imshow portion
N_points = (max_val - min_val) / diff


ax.imshow(plotmatrix, interpolation='nearest', cmap="rainbow" ) #https://matplotlib.org/examples/color/colormaps_reference.html

#text portion
ind_array = np.arange(min_val, max_val, diff)
x, y = np.meshgrid(ind_array, ind_array)


gg = zip(x.flatten(), y.flatten())
    
# Write the text to correct positions; ignore the error it limits us at where we should stop plotwise. Is this lazy? You bet
try:
    for x_val, y_val in zip(x.flatten(), y.flatten()):
        c = "{0:2}".format(plotmatrix[y_val, x_val])
        ax.text(x_val, y_val, c, va='center', ha='center')
except:
    pass

    fig.set_size_inches(6,3)

#defaults to directory we're running the code from
i = 0
while os.path.exists("setup%s.png" % i):
    i += 1
    
plt.savefig("setup%s.png" % i, dpi=120)

plt.show()

#psuedocode made prior to above:

#constraints:
#can't have a column of the matrix be 0 to prevent having three bombs in one column
#must have the correct number of pieces

#calculating total offense score: multiplier for being in front row, mid row, back row, add em up for each square

#calculating total defense score: multiplier based on distance from flag. So if 10 has a defense value of .91 (11.0/12.0),
#it will see that score decrease based on distance from the flag. 1.0 for being 1 square away, .5 for being 9 away (1-(.0555*distance))
#decrease defensive score of bombs past 3 nearby, make it 3/4

#function to optimize will involve adding up total defensive and offensive lane scores, taking into account
#preferred lanes for this run (so lane 1 scores * 1, L2*.75, L3*.5 if you really wanted to bias it to lane 1)
#And a bias towards offense or defense if you want to make a more offensive versus defensive setup
