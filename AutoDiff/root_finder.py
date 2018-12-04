import api
from threading import Thread
import random
import numpy as np

# create a thread object that returns the thread results
# adapted from kindall on stackoverflow
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=()):
        Thread.__init__(self, group, target, name, args)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

# one-dimensional Newton's method
def newton(input_function,tolerance=1e-5, num_starting_vals = 20, 
	starting_val_range = (-1000,1000), starting_val_list=[], verbose=True):

	# find one root 
	def find_root(f,starting_val, max_iter,tol):
		val_dict = {'x' : starting_val}
		error_list = []
		fx = f.get_val(val_dict)
		i = 0

		# if we haven't done too many iterations and we're still greater than our tolerance 
		while i < max_iter and abs(fx) > tol:
			i+=1

			# make a list of errors so we can check Newton's method is working
			error_list += [abs(fx)]

			# get derivative, move to new point
			try:
				dx = f.get_der(val_dict)['x']
				val_dict['x'] = val_dict['x'] - fx/dx
				new_fx = f.get_val(val_dict)
				fx = new_fx
			# avoid dividing by zero 
			except:
				print("Tried to divide by zero!")
				return
		return (val_dict['x'], f.get_val(val_dict), i,error_list)

	# function takes value and list, returns true if value is within diff_tol of any value
	# in the list, false otherwise.
	def is_close_list(val, lst, diff_tol=1e-6):
		for ele in lst:
			if abs(val-ele) < diff_tol:
				return True
		return False 

	f = input_function	

	# adjust starting value list to agree with number of requested starting values 
	while len(starting_val_list)<num_starting_vals:
		starting_val_list.append(random.randint(starting_val_range[0],starting_val_range[1]))

	max_iter = 10000 #maybe user should be able to choose this? 
	results = []
	roots = []

	# start threads 
	for i in range(len(starting_val_list)):
		thread = ThreadWithReturnValue(target=find_root, 
			args=(f,starting_val_list[i],max_iter,tolerance))
		thread.start()
		full_result = thread.join()

		# if didn't catch exception in find_root 
		if full_result:
			root_result = full_result[0]

			# check if root already in list 
			if (not is_close_list(root_result, roots)):
				roots.append(root_result)
				results.append(full_result)

	# for testing, choose verbose 
	if verbose:
		return results
	else:
		return roots


def quasi_newton(input_function,tolerance):
	pass


def multiple_function_root_finder(input_function, lr=0.01, adadelta=False):
	pass


if __name__ == "__main__":
	x=api.Variable('x')
	y=api.Variable('y')

	# answer is [0,2,-3]
	single_function_to_solve=x**api.Constant('a_1', 3)+x**api.Constant('a_2', 2)-api.Constant('a_3', 6)*x
	answer_for_single=single_function_root_finder(single_function_to_solve)
	answer_for_single=single_function_root_finder(single_function_to_solve,adadelta=True)


	# answer is [(x=1,y=4),(x=2,y=3)]
	function_1=x*y-api.Constant('b_1', 4)*x-api.Constant('b_2', 2)*y+api.Constant('b_3', 8)
	function_2=x*y-api.Constant('c_1', 3)*x-api.Constant('c_2', 1)*y+api.Constant('c_3', 3)
	multiple_function_to_solve=[function_1,function_2]
	answer_for_multiple=multiple_function_root_finder(multiple_function_to_solve)
	answer_for_multiple=multiple_function_root_finder(multiple_function_to_solve,adadelta=True)