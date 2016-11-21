#!/usr/bin/env python

"""SA.py: Description of what SA does"""
__author__ = "Karan Chawla"
__email__  = "karangc2@illinois.edu"
__version__= "0.2"

import numpy as np 
import math 
import matplotlib.pyplot as plt 

class SA():

	def __init__(self,)

	def update_temperature(T,k):
		return 0.99*T

	def get_neighbors(i,L):
		assert L>1 and i >=0 and i<L
		if i==0: 
			return [1]
		elif i == L-1 :
			return [L-2]
		else:
			return [i-1, i+1]

	def make_move(x, A, T):
    	nhb = random.choice(xrange(0, len(A))) # choose from all points

	    delta = A[nhb] - A[x]

    	if delta < 0:
        	return nhb
    	else:
        	p = math.exp(-delta / T)
        	return nhb if random.random() < p else x

    def simulated_annealing(A):
    	L = len(A)
   		x0 = random.choice(xrange(0, L))
    	T = 1.
    	k = 1

    	x = x0
    	x_best = x0

	    while T > 1e-3:
    	    x = make_move(x, A, T)
        	if(A[x] < A[x_best]):
            	x_best = x
        	T = update_temperature(T, k)
        	k += 1

    	print "iterations:", k
    	return x, x_best, x0

    def isminima_local(p,A):
    	return all(A[p] < A[i] for i in get_neighbors(p, len(A)))


