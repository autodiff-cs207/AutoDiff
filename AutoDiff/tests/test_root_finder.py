import pytest 
import math
from AutoDiff import DiffObj, Variable, Constant, VectorFunction
from AutoDiff import MathOps as mo
from AutoDiff.root_finder import ThreadWithReturnValue, vectorNewton

# @pytest.markfilterwarnings()
class TestRootFinder():
    def test_no_roots(self):        
        c5 = Constant('c5', 5)
        c5_v = VectorFunction([c5])

        x = Variable('x')
        sin_x = mo.sin(x)
        sin_x_c5 = sin_x + c5
        sin_x_c5_v = VectorFunction([sin_x_c5])

        x_sq = x ** 2
        x_sq_c5 = x_sq + c5
        x_sq_c5_v = VectorFunction([x_sq_c5])

        vector_list = [c5_v, sin_x_c5_v] #, x_sq_c5_v]

        for vector in vector_list:
            roots = vectorNewton(vector, verbose=False)
            assert len(roots) == 0


    # def test_single_root(self):
        

    # def test_multiple_roots(self):
    #     pass



# const5 = Constant('const5', 5)
# const3 = Constant('const3', 3)
# x = Variable('x')
# f_x =  const5 * x + const3
# vf_x = VectorFunction([f_x])

# tol = 1e-6
# roots = vectorNewton(vf_x, verbose=False)
# print(roots)
# assert abs(roots[0][0] - (-0.6)) < tol, "Root found was incorrect"


