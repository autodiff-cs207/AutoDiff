from AutoDiff.ad import DiffObj, Variable, VectorFunction
from AutoDiff.ad import MathOps as mo
import random
import numpy as np
import math
import root_finder

TOL=0.01

# add on denoise for single root finder
def denoise_root_finder(f):
	roots=[item[0] for item in root_finder.vectorNewton(VectorFunction([f]), verbose=False)]
	real_root=[]
	for i in roots:
		if len(real_root)==0:
			real_root.append(i)
		else:
			count=0
			for j in real_root:
				if abs(i-j)<TOL:
					count+=1
			if count==0:
				real_root.append(i)
	return real_root

def root_finder_multiple(list_of_f):
	final_list=[]
	root_list=[denoise_root_finder(f) for f in list_of_f]
	for candidates in root_list[0]:
		count=0
		for compare_group in root_list[1:]:
			for compare_item in compare_group:
				if abs(compare_item-candidates)<TOL:
					count+=1
					break
		if count==len(list_of_f)-1:
			final_list.append(candidates)
	return final_list

# quasi newton method

if __name__=='__main__':
	x = Variable('x')
	y = Variable('y')
	z = Variable('z')
	f_1 = (x-1)**2*(x-2)*2
	f_2 = (y-3)**3*(y-2)*4
	f_3 = (z-2)**3*(z-5)*4
	roots=root_finder_multiple([f_1,f_2,f_3])
	print(roots)
	