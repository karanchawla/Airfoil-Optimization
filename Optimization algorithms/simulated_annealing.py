#!/usr/bin/env python

"""simulated_annealing.py: Description of what this does"""
__author__ = "Karan Chawla"
__email__  = "karangc2@illinois.edu"
__version__= "0.1"

import random
import math
LIMIT = 100000

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

def func(x):
    return math.sin((2 * math.pi / LIMIT) * x) + 0.001 * random.random()
    
def initialize(L):
    return map(func, xrange(0, L))

def main():
    A = initialize(LIMIT)

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