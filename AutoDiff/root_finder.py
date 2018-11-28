import api

def single_function_root_finder(input_function, lr=0.01, adadelta=False):
	# When value of function < 0 then optimize the function towards > 0 and vise versa
	# ends until the value of the function becomes stable
	# when adadelta is set Ture, change lr (learning rate) according to a set of rules that you define
	# root finding process should include random initializing params and vairables in order to find all roots
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