#!/usr/bin/env python

"""PSO.py: Description of what PSO does"""
__author__ = "Karan Chawla"
__email__  = "karangc2@illinois.edu"
__version__= "0.1"

import numpy as np 
import math
import matplotlib.pyplot as plt

	
def PSO(problem,params,display):

	global nPop 
	nPop = 50 #swarm size
	global nVar
	#nVar = 5; #five dimensional space: number of unknown variables
	nVar = problem.nVar
	#varMin = -10 #lower bound
	varMin = problem.varMin
	#varMax = 10 #upper bound
	varMax = problem.varMax
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

	'''#problem defintion
	def objective_function(x):
		return np.multiply(x,x)		#cost function'''

	#parameters of PSO
	maxIt = 1000 #max iterations
	maxIt = params.maxIt
	#w = 1. #inertia coeff
	w = params.w 
	#c1 = 2. #personal accelration coeff
	c1 = params.c1
	#c2 = 2. #global acc coeff
	c2 =  params.c2
	#wdamp =0.99
	wdamp = params.wdamp
	#nitialization

	swarm = particle(np.ones((nPop,nVar)),np.zeros((nPop,nVar)),0,np.ones((nPop,nVar)),np.ones((nPop,nVar)),0,0)


	for i in range(nPop):
		#randomly initialise positions
		swarm.position[i] = np.random.uniform(varMin,varMax,varSize)
		swarm.velocity = np.zeros((nPop, nVar))
		#calculate cost
		swarm.cost[i] = problem.costFunction((np.sum(swarm.position[i]))/nVar)
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

			#apply lower and upper bound limits

			swarm.cost[i] = problem.costFunction((np.sum(swarm.position[i]))/nVar)
			if swarm.cost[i]<swarm.best_cost[i]:
				swarm.best_pos[i] = swarm.position[i]
				swarm.best_cost[i] = swarm.cost[i]

				if (swarm.best_cost[i] <= swarm.global_best):
					swarm.global_best, swarm.global_best_pos = swarm.best_cost[i],i
			plt.scatter(sum(swarm.position[i])/nVar,it)	
		
		#store best cost value and position
		bestCosts[it] = swarm.global_best
		#print "best_cost:",bestCosts[i], "iteration:",it


		#damping inertia for the population
		w = w*wdamp

	#results
	#display is the flag for showing iteration information
	if display==True:
		plt.xlabel('Iteration')
		plt.ylabel('Position')
		#plt.yscale('log')
		#plt.xscale('log')
		plt.grid(True)
		#plt.plot(bestCosts)
		plt.show()
		

	return [swarm.global_best,swarm.global_best_pos,swarm.position[swarm.global_best_pos]]

#defining the problem and parameters
class problem: 
	def __init__(self,nVar,varMin,varMax):
		self.nVar = nVar
		self.varMin = varMin
		self.varMax = varMax
	#define your cost function 
	def costFunction(self,x): 
		self.x = x
		print np.multiply(x,x)
		return (np.multiply(x,x))


class params: 
	def __init__(self,maxIt,nPop,w,wdamp,c1,c2):
		self.maxIt = maxIt
		self.nPop = nPop
		self.w = w
		self.wdamp = wdamp
		self.c1 = c1
		self.c2 = c2

		
#calling PSO
p1 = problem(5,-10,10)
params1 = params(100,50.,1.,0.99,2.,2.)
result = PSO(p1,params1,True)

print result