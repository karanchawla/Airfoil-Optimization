import numpy as np 
import math
import matplotlib.pyplot as plt
global nPop 
nPop = 50 #swarm size
global nVar
nVar = 5; #five dimensional space: number of unknown variables
varMin = -10 #lower bound
varMax = 10 #upper bound
varSize = np.array((1,nVar))  #matrix size of decision variables

#particle template
class particle:
	def __init__(self,position,velocity,cost,best_pos,best_cost,global_best,global_best_pos):
		self.position = np.ones((nPop,nVar))
		self.velocity = np.zeros((nPop,nVar))
		self.cost     = np.ones((nPop,1))
		self.best_pos = np.zeros((nPop,nVar))
		self.best_cost = np.ones((nPop,1))
		#self.global_best = np.ndarray((nPop,pow(math.e,6)))
		self.global_best = pow(10,6)
		self.global_best_pos = 0

#problem defintion
def objective_function(x):
	return np.multiply(x,x)		#cost function

#parameters of PSO
maxIt = 1000 #max iterations
w = 1. #inertia coeff
c1 = 2. #personal accelration coeff
c2 = 2. #global acc coeff
wdamp =0.99
#nitialization

swarm = particle(np.ones((nPop,nVar)),np.zeros((nPop,nVar)),0,np.ones((nPop,nVar)),np.ones((nPop,nVar)),0,0)


for i in range(nPop):
	#randomly initialise positions
	swarm.position[i] = np.random.uniform(varMin,varMax,varSize)
	swarm.velocity = np.zeros((nPop, nVar))
	#calculate cost
	swarm.cost[i] = objective_function(np.sum(swarm.position[i]))
	#update personal best
	swarm.best_pos[i] = swarm.position[i]
	swarm.best_cost[i] = swarm.cost[i]
	#update global best
	if (swarm.best_cost[i] <= swarm.global_best):
		swarm.global_best, swarm.global_best_pos = swarm.best_cost[i],i

#aray to hold best cost value for each iteration 
bestCosts = np.zeros((maxIt,1))
#main loop of  PSO
for it in range(maxIt):
	for i in range(nPop):
		swarm.velocity[i] = w*swarm.velocity[i] + c1*np.multiply((np.random.rand(1,nVar)),(swarm.best_pos[i]-swarm.position[i]))\
							+ c2* np.multiply(np.random.rand(1,nVar),(swarm.global_best_pos-swarm.best_pos[i]))

		swarm.position[i] += swarm.velocity[i]
		swarm.cost[i] = objective_function(np.sum(swarm.position[i]))
		if swarm.cost[i]<swarm.best_cost[i]:
			swarm.best_pos[i] = swarm.position[i]
			swarm.best_cost[i] = swarm.cost[i]

			if (swarm.best_cost[i] <= swarm.global_best):
				swarm.global_best, swarm.global_best_pos = swarm.best_cost[i],i
			
	#store best cost value and position
	bestCosts[it] = swarm.global_best
	#print "best_cost:",bestCosts[i], "iteration:",it

	#damping inertia 
	w = w*wdamp
#results
plt.xlabel('Iteration')
plt.ylabel('Best Cost')
plt.yscale('log')
plt.xscale('log')
plt.grid(True)
plt.plot(bestCosts)
plt.show()

#print [swarm.global_best,swarm.global_best_pos]

print np.ones((5,1))