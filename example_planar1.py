import simulate_planar as sp
import random

n_trials = 100
success_count = 0

size=6
tSteps=1
p=0.05
pLie=0.0

random.seed(0)


for i in range(n_trials):
    x,z = sp.run3Drandom(size,tSteps,p,pLie)

    if x==1 and z==1: success_count+=1


print 'lattice size: ',size
print 'time steps: ', tSteps
print 'random errors applied with probability p=',p
print 'lying stabilizer measurements with pLie ',pLie
print 
print success_count,' /',n_trials,' were successfully decoded: ',success_count
