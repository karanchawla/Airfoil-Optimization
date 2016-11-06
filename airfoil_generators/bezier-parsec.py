from __future__ import division
import numpy as np
from airfoilgen_baseclass import ParametricAirfoil

def camber_points(gLe, xC, yC, aTe, zTe, b0, b2, b17):
	pL0 = np.zeros((2,1))
	pL1 = np.array((2,1))
	pL1[0][0] = b0
	pL1[0][1] = b0 * tan(gLe)

	pL2 = np.array([[b2],
					[yc]])

	pL3 = np.array([[xc],
					[yc]])

	pT1 = np.array([[( 3 * xC - yC * cot(gLe) )/2],
					[yc]])

	pT2 = np.array([[(-8 * yC * cot(gLe) + 13 * xC )/6],
					[5*yc/6]])

	pT3 = np.array([[b17],
					[zTe - (1 - b17) * tan(aTe) ]])

	pT4 = np.array([[1],
					[zTE]])

	points = np.array([pL0, pL1, pL2, pL3, pT1, pT2, pT3, pT4])
	return points

def thickness_points(rLe, xT, yT, bTe, dZTe, b8, b15 ):
	pL0 = np.zeros((2,1))
	pL1 = np.array((2,1))
	pL1[0][0] = 0
	pL1[0][1] = b8

	pL2 = np.array([[ -3 * b8**2 / (2 * rLe)],
        			[yT]])

    pL3 = np.array([[xT],
    				[yT]])

	pT1 = np.array([[ ( 7 * xT + 9 * b8**2 / (2 * rLe) ) / 4],
        			[yT]]) 

	pT2 =  np.array([[  3 * xT + 15 * b8**2 / (4 * rLe)],
        			[(yT + b8) / 2]]) 

	pT3 = np.array([[b15],
    				[dZTe + (1 - b15) * tan( bTe ) ]])

	pT4 = np.array([[1],
					[dZTe]])

	points = np.array([pL0, pL1, pL2, pL3, pT1, pT2, pT3, pT4])
	return points


class BezierParsec(ParametricAirfoil):

	def __init__(self,k):
		''' Takes a dictionary of coefficients'''
		self.k = k
