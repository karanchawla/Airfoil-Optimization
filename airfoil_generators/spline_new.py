import numpy as np
from math import * 
import matplotlib.pyplot as plt 

def spline(ta_u,ta_l,tb_u,tb_l,alpha_b,alpha_c):
	u = np.linspace(0,1,1000)
	x_u = []
	y_u = []
	x_l = []
	y_l = []
	temp_var1 = np.array([[1,0,0,0],[0,0,1,0],[-3,3,-2,-1],[2,-2,1,1]])
	A = [0,0]
	B = [1,0]
	TA_u = [(ta_u*cos(-pi/2)),ta_u*abs(sin(-pi/2))]
	TB_u = [(tb_u*cos(-((alpha_c+alpha_b)*pi/180))),(tb_u*sin(-((alpha_b+alpha_c)*pi/180)))] 
	TA_l = [(ta_l*cos(-pi/2)),ta_l*(sin(-pi/2))]
	TB_l = [(tb_l*cos(-((alpha_c)*pi/180))),(tb_l*sin(-((alpha_c)*pi/180)))] 

	for j in range(2):
		temp_var =  np.array([[A[j]],[B[j]],[TA_u[j]],[TB_u[j]]]) #control points for x and y coords
		temp_var_coord = np.dot(temp_var1,temp_var)
		for i in range(len(u)):
			temp_var4 = [1,u[i],u[i]**2, pow(u[i],3)]
			if j==1:
				x_u.append(np.dot(temp_var4,temp_var_coord)) #calculate x coords
			else:
				y_u.append(np.dot(temp_var4,temp_var_coord)) #calculate y coords

	for j in range(2):
		temp_var =  np.array([[A[j]],[B[j]],[TA_l[j]],[TB_l[j]]]) #control points for x and y coords
		temp_var_coord = np.dot(temp_var1,temp_var)
		for i in range(len(u)):
			temp_var4 = [1,u[i],u[i]**2, pow(u[i],3)]
			if j==1:
				x_l.append(np.dot(temp_var4,temp_var_coord)) #calculate x coords
			else:
				y_l.append(np.dot(temp_var4,temp_var_coord)) #calculate y coords

	plt.xlim(0,1)
	plt.ylim(-.2,.2)
	plt.plot(y_u,x_u,'r') #plot the spline
	plt.plot(y_l,x_l,'b')
	plt.show()
	return 0

ta_u = 0.1584
ta_l = 0.1565
tb_u = 2.1241
tb_l = 1.8255
alpha_c = 3.8270
alpha_b = 11.6983

spline(ta_u,ta_l,tb_u,tb_l,alpha_b,alpha_c)