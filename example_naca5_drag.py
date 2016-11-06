"""
An example to show how to combine NACA5 airfoil_generator and XFOIL
"""

from airfoil_generators.naca5series import NACA5
from xfoil.xfoil import oper_visc_cl
import os

import matplotlib.pyplot as plt 
import numpy as np 

Re = 1000000
Cl = 0.2

drags = np.zeros((5,3))

for i in range(1,6):
	if i==1:
		mld = 210
	elif i==2:
		mld = 220
	elif i==3:
		mld = 230
	elif i==4:
		mld = 240 
	else: 
		mld = 250
	
	if mld == 210:
		m = .0580
		k1 = 361.40
		p = 0.05
	elif mld ==220:
		m = .1260
		k1 = 51.640
		p = 0.10
	elif mld == 230:
		m = .2025
		k1 = 15.957
		p = .15
	elif mld == 240:
		m = .2900
		k1 = 6.643
		p = 0.20
	elif mld == 250:
		m = .3910
		k1 = 3.23
		p = .25
	for t in range(13,16):
		airfoil = NACA5(mld,t)

		temp_af_filename = "temp_airfoil_{}{}.dat".format(mld,t)

		with open(temp_af_filename,'w') as af:
			af.write(airfoil.get_coords_plain())

		polar = oper_visc_cl(temp_af_filename, Cl, Re, iterlim=1000)

		try:
			drags[i-1][t-13] = polar[0][0][2]
		except IndexError:
			raise Warning("Shit! XFOIL didn't converge on NACA{}{} at Cl={}.".format(mld,t,Cl))

		xl, yl, xu, yu, xc, yc = airfoil.get_coords()
		def translated_plt(x, y, *args):
			plt.plot(x*0.8 + (t-12.9), y*0.8 + (i-0.5) , *args)
		translated_plt(xl, yl, 'w')
		translated_plt(xu, yu, 'w')
		translated_plt(xc, yc, 'w--')

		os.remove(temp_af_filename)

print drags
plt.pcolor(drags, cmap=plt.cm.RdBu)

plt.xlabel("Location of max. camber $p$")
plt.ylabel("Max. camber $m$")

cbar = plt.colorbar()
cbar.ax.set_ylabel("Drag coefficient $C_d$")

plt.tight_layout()
plt.yticks( (.5,1.5,2.5,3.5,4.5), ("210t", "220t", "230t", "240t", "250t") )
plt.xticks( (.5,1.5,2.5), ("mld13", "mld14", "mld15") )
plt.show()
