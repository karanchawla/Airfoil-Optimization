#!/usr/bin/env python

"""simulated_annealing.py: Description of what this does"""
__author__ = "Karan Chawla"
__email__  = "karangc2@illinois.edu"
__version__= "0.1"

#from __future__ import division, print_function
from os import remove
import numpy as np
from copy import copy
from string import ascii_uppercase
from random import choice
from xfoil import xfoil
from random import choice
import random
import math
import numpy as np 
import matplotlib.pyplot as plt
from airfoil_generators import parsec

Re = 1E6
LIMIT = 5
S = 12 
constraints = np.array((
#rle        x_pre/suc    d2ydx2_pre/suc  th_pre/suc
(.015,.05), (.3,.75),     (-2,.2),          (0,40)
))

class Particle():
    def __init__(self,constraints):
        self.constraints = constraints
        self.positions = np.ones(len(constraints), dtype = "float")
        #self.velocity = np.zeros(len(constraints) , dtype ="float") 
        # randomize positions and speeds
        self.randomize()
        #set current point as best 
        #self.global_best(float('inf'))

    def randomize(self):
        for i, (lowerbound,upperbound) in enumerate(self.constraints):
            self.positions[i] = np.random.uniform(lowerbound,upperbound)
            absrange = abs(lowerbound-upperbound)
            #self.velocity[i] = np.random.uniform(-absrange,absrange)

def construct_airfoil(*pts):
    k = {}
    k['rle'] = pts[0]
    k['x_pre'] = pts[1]
    # Thickness 21%
    k['y_pre'] = -.105
    k['d2ydx2_pre'] = -pts[2]
    # Trailing edge angle
    k['th_pre'] = pts[3]
    # Suction part
    k['x_suc'] = k['x_pre']
    k['y_suc'] = -k['y_pre']
    k['d2ydx2_suc'] = -k['d2ydx2_pre']
    k['th_suc'] = -k['th_pre']
    # Trailing edge x and y position
    k['xte'] = 1
    k['yte'] = 0
    return parsec.PARSEC(k)

def score_airfoil(airfoil):    
    # Make unique filename
    randstr = ''.join(choice(ascii_uppercase) for i in range(20))
    filename = "parsec_{}.dat".format(randstr)
    # Save coordinates
    with open(filename, 'w') as af:
        af.write(airfoil.get_coords_plain())
    # Let Xfoil do its magic
    polar = xfoil.oper_visc_alpha(filename, 0, Re,
                                  iterlim=80, show_seconds=0)
    try:
        remove(filename)
    except WindowsError:
        print("\n\n\n\nWindows was not capable of removing the file.\n\n\n\n")

    try:
        score = polar[0][0][2]
        print "Score: ", score
        # If it's not NaN
        if np.isfinite(score):
            print "Return score"
            return score
        else:
            print"Return None"
            return None
    except IndexError:
        print "Return None (IndexError)"
        return None

particle = [Particle(constraints) for i in xrange(0, LIMIT)]



def update_temperature(T, k):
    return .99*T

def get_neighbors(i, L):
    assert L > 1 and i >= 0 and i < L
    if i == 0:
        return [1]
    elif i == L - 1:
        return [L - 2]
    else:
        return [i - 1, i + 1]

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

def isminima_local(p, A):
    return all(A[p] < A[i] for i in get_neighbors(p, len(A)))

def rastrigin_nd_randnone(*xi):
    """
    Simulates airfoils that don't converge in Xfoil by randomly returning None
    """
    # Return None 20% of the time
    if np.random.rand() > .8:
        return None
    else:
        return rastrigin_nd(*xi)

def rastrigin_nd(*xi):
    """
    n-dimensional rastrigin function. Every argument should be a single
    value or meshgrid, and is another dimension.
    """
    return (10*len(xi)+ np.sum(a**2 - (10*np.cos(2*np.pi*a)) for a in xi))

def func(x):
    return math.sin((2 * math.pi / LIMIT) * x) + 0.001 * random.random()

    
def initialize(L):
    return map(rastrigin_nd, xrange(0, L))

def initialise_set(L):
    airfoil = []
    for i in range(L):
        airfoil.append(construct_airfoil(*particle[i].positions))
    for j in range(L): 
        x = map(score_airfoil,airfoil)
    print x 
    return x 
        

def main():
    A = initialise_set(LIMIT)

    local_minima = []
    for i in xrange(0, LIMIT):
        if(isminima_local(i, A)):
            local_minima.append([i, A[i]])

    x = 0
    y = A[x]
    for xi, yi in enumerate(A):
        if yi < y:
            x = xi
            y = yi
    global_minumum = x

    print "number of local minima: %d" % (len(local_minima))
    print "global minimum @%d = %0.3f" % (global_minumum, A[global_minumum])

    x, x_best, x0 = simulated_annealing(A)
    print "Solution is @%d = %0.3f" % (x, A[x])
    print "Best solution is @%d = %0.3f" % (x_best, A[x_best])
    print "Start solution is @%d = %0.3f" % (x0, A[x0])


main()