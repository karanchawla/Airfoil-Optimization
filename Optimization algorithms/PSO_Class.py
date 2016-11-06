#!/usr/bin/env python

"""PSO.py: Description of what PSO does"""
__author__ = "Karan Chawla"
__email__  = "karangc2@illinois.edu"
__version__= "0.2"

import numpy as np 
import math
import matplotlib.pyplot as plt

class Particle():

	def __init__(self,constraints):
		self.constraints = constraints
		self.positions = np.ones(len(constraints), dtype = "float")
		self.velocity = np.zeros(len(constraints) , dtype ="float") 
		# randomize positions and speeds
		self.randomize()
		#set current point as best 
		self.global_best(float('inf'))

	def new_best(self,score):
		self.bestscore = score
		self.best_pos = self.pts

	def randomize(self):
		for i, (lowerbound,upperbound) in enumerate(self.constraints):
			self.positions[i] = np.random.uniform(lowerbound,upperbound)
			absrange = abs(lowerbound-upperbound)
			self.velocity[i] = np.random.uniform(-absrange,absrange)

	def update(self, global_best,omega, theta_p, theta_g):
		self.oldpositions  = copy(self.positions)
        self.oldvelocity = copy(self.velocity)

        r_p,r_g = np.random.uniform(0,1), np.random.uniform(0,1)

        self.velocity = omega*self.velocity+ theta_p*np.multiply(r_p,(self.best_pos-self.position))\
								+ theta_g* np.multiply(r_g,self.global_best-self.best_pos)

		self._boundvelocity()
		self.position += self.velocity
		self._boundposition()

	def _boundposition(self):

		for i, (lowerbound,upperbound) in enumerate(self.constraints):
			pt = self.positions[i]
            if pt < lowerbound: self.positions[i] = lowerbound
            if pt > upperbound: self.positions[i] = upperbound

	def _boundvelocity(self):
        '''Restrict speeds to -range<v<range'''
		for i, (lowerbound, upperbound) in enumerate(self.constraints):
	        spd = self.velocity[i]
            absrange = abs(upperbound-lowerbound)
            if spd < -absrange: self.velocity[i] = -absrange
            if spd >  absrange: self.velocity[i] =  absrange

    def PSO(self,global_best,B,a):
    	self.oldpositions = copy(self.positions)
    	self.oldvelocity = copy(self.velocity)

    	for i, pt in enumerate(self.positions):
    		mu, sigma = 0,1
    		e = np.random.normal(mu,sigma)
    		c = self.constraints[i]
    		L = abs(c[1]-c[0])
    		self.positions[i] = (1-B)*L*pt + B*L*global_best[i] + a*L*e
    	self._boundposition

    