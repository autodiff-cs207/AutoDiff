import math

class DiffObj(object):
    '''
    All functions will be represented by an instance of this class DiffObj, or by instances of
    classes which inherit from DiffObj (e.g. class Variable, class Constant etc.) DiffObj enforces
    that each class which inherits from it, must implement two functions:

    CLASS FUNCTIONS
    ==================
    The functions get_val and get_der are exposed to the user, that is, a user of our package can
    call these functions.

    (1) get_val:        This is used to evaluate the function represented by a DiffObj instance at
                        a particular point.
                        
    (2) get_der:        This is used to evalate the gradient of the function repreesnted by a DiffObj
                        instance, at a particular point.

    CLASS ATTRIBUTES
    ================
    The attributes are not meant to be used by an end-user of our package, and they are meant for internal
    computation.

    name_list:          A list of strings, where each item in the list represents the variables inside
                        the function represented by this DiffObj. E.g. for f(x,y) = x + y, the name_list
                        for a DiffObj representing f will be ['x', 'y'] (assuming the x.name_list = ['x']
                        and y.name_list = ['y'].
    operator:           A single string representing the "operator". By default, DiffObj assumes that it
                        represents two DiffObj's connected by an binary operator such as 'add'. However, 
                        we use the same definition for unary operators such as negation or cosine.
    operand_list:       A list of two DiffObjs, which together with self.operator, comprise this instance
                        of DiffObj.
    '''
    OVERLOADED_OPERATORS = ['add', 'subtract', 'multiply', 'divide',
            'power', 'neg']
    def __init__(self, name_list, operator, operand_list):
        self.name_list = name_list
        self.operator = operator
        self.operand_list = operand_list
    def get_val(self, value_dict):
        '''
        INPUT
        ======
        value_dict:     A dictionary, whose keys are strings representing variables which feature
                        in the formula represented by this DiffObj. The values at those keys are
                        the values at which the formula representing this DiffObj will be evaluated.

                        E.g. For a DiffObj which represents the function f(x,y) = x + y, the value_dict
                        argument may look like value_dict = {'x': 10, 'y': 5}
        OUTPUT
        ======

        DOCTEST
        ======
        >>> z=x+y
        >>> z.get_val({'x':1,'y':1})
        2


        result:         A floating point number, which equals the evaluation of the function
                        represented by this DiffObj, at the variable values given by val_dict.
        '''
        if self.operator not in DiffObj.OVERLOADED_OPERATORS:
            raise ValueError('{} is not a supported operator'.format(self.operator))
        if self.operator == 'add':
            return self.operand_list[0].get_val(value_dict) + self.operand_list[1].get_val(value_dict)
        elif self.operator == 'subtract':
            return self.operand_list[0].get_val(value_dict) - self.operand_list[1].get_val(value_dict)
        elif self.operator == 'multiply':
            return self.operand_list[0].get_val(value_dict)*self.operand_list[1].get_val(value_dict)
        elif self.operator == 'divide':
            try:
                result = self.operand_list[0].get_val(value_dict)/self.operand_list[1].get_val(value_dict)
                return result
            except:
                raise ValueError('Division by zeros is not allowed')
        elif self.operator == 'power':
            return self.operand_list[0].get_val(value_dict)**self.operand_list[1].get_val(value_dict)
        elif self.operator == 'neg':
            return -self.operand_list[0].get_val(value_dict)

    def get_der(self, value_dict, with_respect_to=None):
        '''
        INPUT
        ======
        value_dict:         A dictionary, whose keys are strings representing variables which feature
                            in the formula represented by this DiffObj. The values at those keys are
                            the values at which the gradient of formula representing this DiffObj will 
                            be evaluated.
                            
                            E.g. For a DiffObj which represents the function f(x,y) = x + y, the value_dict
                            argument may look like value_dict = {'x': 10, 'y': 5}
        OUTPUT
        ======
        result:             A dictionary, whose keys are strings representing variables which feature 
                            in the formula represented by this DiffObj. The value associated withe each
                            key is a floating point number which is the partial derivative of this DiffObj 
                            with respect to that variable.
        with_respect_to:    A list of strings representing variables, with respect to which we want the 
                            gradient of this DifObj. By default, if this list is not provided, then the
                            gradient with respect to all variables featuring in the DiffObj is returned.

        DOCTEST
        ======
        >>> z=x+y
        >>> z.get_der({'x':0,'y':0})
        {'y': 1, 'x': 1}

        '''
        if not with_respect_to: with_respect_to = self.name_list
        df = {}
        op1, op2 = self.operand_list[0], self.operand_list[1]
        op1_val = op1.get_val(value_dict)
        op2_val = op2.get_val(value_dict)

        if self.operator == 'add':
            for w in with_respect_to:
                dw = op1.get_der(value_dict, [w])[w] + op2.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'subtract':
            for w in with_respect_to:
                dw = op1.get_der(value_dict, [w])[w] - op2.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'multiply':
            for w in with_respect_to:
                dw = op1.get_der(value_dict, [w])[w]*op2_val + op2.get_der(value_dict, [w])[w]*op1_val
                df[w] = dw
        elif self.operator == 'divide':
            try:
                one_by_op2_val = 1.0/op2_val
            except:
                raise ValueError('Division by zero is not allowed')
            for w in with_respect_to:
                dw = (op2_val*op1.get_der(value_dict, [w])[w] - op1_val*op2.get_der(value_dict, [w])[w])/(op2_val**2)
                df[w] = dw
        elif self.operator == 'power':
            func_val = op1_val**op2_val
            for w in with_respect_to:
                try:
                    dw = func_val*((op2_val/op1_val)*op1.get_der(value_dict, [w])[w] + 
                            math.log(op1_val)*op2.get_der(value_dict, [w])[w])
                except:
                    raise ValueError('Derivative is only defined for positive Base in an Exponentiation.')
                df[w] = dw
        elif self.operator == 'neg':
            for w in with_respect_to:
                dw = -op1.get_der(value_dict, [w])[w]
                df[w] = dw
        if len(df) == 0: df = {'' : 0}
        return df

    def getBinaryOperator(self, other, operator_name):
        try:
            other_name_list = other.name_list
            if operator_name == 'neg': other_name_list = []
            return DiffObj(self.name_list + other_name_list,
                    operator_name, [self, other])
        except:
            raise TypeError('Operands need to be of type DiffObj.')

    def __neg__(self):
        '''
        Overloads negation for objects of type DiffObj.
        INPUT
        =====
        Takes a single AutoDiff object (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):

        a = AutoDiff object

        -a

        which uses our __neg__ method.
        a.__neg__()
        
        OUTPUT
        ======
        result:         A DiffObj, for which DiffObj.operator_name is 'neg', DiffObj.operand_list 
                        contains [a,a], and DiffObj.name_list is same as the original name_list of a.
                        
        '''
        return self.getBinaryOperator(self, 'neg')
    def __add__(self, other):
        '''
        Overloads the add operator such that it works for DiffObj objects.

        INPUT
        =====
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):
    
        a = AutoDiff object
        b = AutoDiff object

        a + b

        which uses our __add__ method:

        a.__add__(b)

        OUTPUT
        ======
        Returns a DiffObj, where the DiffObj.name_list is the concatination of a.name_list and b.name_list,
        DiffObj.operator_name is 'add', and DiffObj.operand_list is [a,b].

        When get_val is called on the resulting DiffObj, as in DiffObj.get_val(val_dict), the sum
        DiffObj.operand_list[0].get_val(val_dict) + DiffObj.operand_list[1].get_val(val_dict) is returned.
        In other words, DiffObj.get_val(val_dict) returns the sum of the operands after
        their values are evaluated individually with respect to their own value dictionaries.

        '''
        return self.getBinaryOperator(other, 'add')
    def __sub__(self, other):
        '''
        Overloads the subtract operator such that it works for DiffObj objects.

        INPUT
        =====
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):

        a = AutoDiff object
        b = AutoDiff object

        a - b

        which uses our __sub__ method:

        a.__sub__(b)

        OUTPUT
        ======
        Returns a DiffObj, where the DiffObj.name_list is the concatination of a.name_list and b.name_list,
        DiffObj.operator_name is 'subtract', and DiffObj.operand_list is [a,b].

        When get_val is called on the resulting DiffObj, as in DiffObj.get_val(val_dict), the difference
        DiffObj.operand_list[0].get_val(val_dict) - DiffObj.operand_list[1].get_val(val_dict) is returned.
        In other words, DiffObj.get_val(val_dict) returns the difference of the operands after
        their values are evaluated individually with respect to their own value dictionaries.

        '''
        return self.getBinaryOperator(other, 'subtract')
    def __mul__(self, other):
        '''
        Overloads the multiply operator such that it works for DiffObj objects.

        INPUT
        =====
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):

        a = AutoDiff object
        b = AutoDiff object

        a * b

        which uses our __mul__ method:

        a.__mul__(b)

        OUTPUT
        ======  
        Returns a DiffObj, where the DiffObj.name_list is the concatination of a.name_list and b.name_list,
        DiffObj.operator_name is 'multiply', and DiffObj.operand_list is [a,b].

        When get_val is called on the resulting DiffObj, as in DiffObj.get_val(val_dict), the product
        DiffObj.operand_list[0].get_val(val_dict) * DiffObj.operand_list[1].get_val(val_dict) is returned.
        In other words, DiffObj.get_val(val_dict) returns the product of the operands after
        their values are evaluated individually with respect to their own value dictionaries.
        '''
        return self.getBinaryOperator(other, 'multiply')
    def __truediv__(self, other):
        '''
        Overloads the division operator such that it works for DiffObj objects.

        INPUT
        =====
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):

        a = AutoDiff object
        b = AutoDiff object

        a / b

        which uses our __truediv__ method:

        a.__truediv__(b)

        OUTPUT
        ======
        Returns a DiffObj, where the DiffObj.name_list is the concatination of a.name_list and b.name_list,
        DiffObj.operator_name is 'divide', and DiffObj.operand_list is [a,b].

        When get_val is called on the resulting DiffObj, as in DiffObj.get_val(val_dict), the division
        DiffObj.operand_list[0].get_val(val_dict) / DiffObj.operand_list[1].get_val(val_dict) is returned.
        In other words, DiffObj.get_val(val_dict) returns the division of the operands after
        their values are evaluated individually with respect to their own value dictionaries.

        '''
        return self.getBinaryOperator(other, 'divide')
    def __pow__(self, other):
        '''
        Overloads the power operator such that it works for DiffObj objects.
        INPUT
        =====
        self, other:        Two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, 
                            AutoDiff.Variable, or AutoDiff.MathOps

        Example Usage:
        If a and b are two AutoDiff Objects. Then a**b will use our __pow__ method.


        OUTPUT
        ======
        result:             A DiffObj where DiffObj.name_list is the concatenation of a.name_list and 
                            b.name_list, DiffObj.operator_name is 'power', and DiffObj.operand_list is
                            [a,b].

        '''
        return self.getBinaryOperator(other, 'power')
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    
   
class Variable(DiffObj):
    def __init__(self, var_name):
        self.var_name = var_name
        super(Variable, self).__init__([var_name], None, None)
    
    def get_val(self, value_dict):
        if self.var_name not in value_dict:
            raise ValueError('You have not provided a value for {}'.format(self.var_name))
        try:
            temp = value_dict[self.var_name] + 0.0
        except:
            raise TypeError('Only integer and float types are accepted as values.')
        return value_dict[self.var_name]
    
    def get_der(self, value_dict, with_respect_to=None):
        if not with_respect_to:
            return {self.var_name : 1}
        else:
            der_dict = {}
            for w in with_respect_to:
                der_dict[w] = int(w == self.var_name)
            return der_dict

class Constant(DiffObj):
    def __init__(self, const_name, const_val):
        super(Constant, self).__init__([], None, None)
        self.const_name = const_name
        self.const_val = const_val
        self.name_list = []
    def get_val(self, value_dict):
        return self.const_val
    def get_der(self, value_dict, with_respect_to=None):
        if not with_respect_to:
            return {'' : 0}
        der_dict = {}
        for w in with_respect_to:
            der_dict[w] = 0
        return der_dict

class MathOps(DiffObj):
    '''
    This class inherits from the DiffObj class. It implements non-elementary unary functions 
    including: sin, cos, tan, log, exp.

    INSTANTIATION
    ===============
    If a is of type DiffObj, then the invoking the constructor as follows will return an 
    object b of type MathOps:

    b = MathOps.sin(a)

    CLASS ATTRIBUTES
    ================
    The attributes are not meant to be used by an end-user of our package, and they are meant for internal
    computation.

    name_list:          A list of strings, where each item in the list represents the variables inside
                        the function represented by this DiffObj. E.g. for f(x,y) = x + y, the name_list
                        for a DiffObj representing f will be ['x', 'y'] (assuming the x.name_list = ['x']
                        and y.name_list = ['y'].
    operator:           A string, such as 'sin' or 'log', which represents one of the unary math operators
                        implemented by this class.
    operand_list:       A list of length 1 containing the DiffObj which the user has passed as an argument
                        to one of the classmethods of MathOps.

    '''
    def __init__(self, name_list, operator, operand):
        super(MathOps, self).__init__(name_list, 
                operator, operand)
    @classmethod
    def getUnaryOperator(cls, operator, obj):
        try:
            name_list = obj.name_list
            return MathOps(name_list, operator, [obj]) 
        except:
            raise TypeError('Only objects of type DiffObj are permitted.')
    @classmethod
    def sin(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the sine function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'sin' and whose operand is
                    the DiffObj on which the user had called this sin function.
        '''
        return MathOps.getUnaryOperator('sin', obj)
    @classmethod
    def cos(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the cos function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'cos' and whose operand is
                    the DiffObj on which the user had called this cos function.
        '''
        return MathOps.getUnaryOperator('cos', obj)
    @classmethod
    def tan(cls,obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the tan function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'sin' and whose operand is
                    the DiffObj on which the user had called this tan function.
        '''

        return MathOps.getUnaryOperator('tan', obj)
    @classmethod
    def log(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the natural log function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'sin' and whose operand is
                    the DiffObj on which the user had called this log function.
        '''

        return MathOps.getUnaryOperator('log', obj)
    @classmethod
    def exp(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the natural exponentiation function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'sin' and whose operand is
                    the DiffObj on which the user had called this exp function.
        '''

        return MathOps.getUnaryOperator('exp', obj)
    def get_val(self, value_dict):
        '''
        INPUT
        ======
        value_dict:     A dictionary, whose keys are strings representing variables which feature
                        in the formula represented by this DiffObj. The values at those keys are
                        the values at which the formula representing this DiffObj will be evaluated.

                        E.g. For a DiffObj which represents the function f(x,y) = x + y, the value_dict
                        argument may look like value_dict = {'x': 10, 'y': 5}
        OUTPUT
        ======
        result:         A floating point number, which equals the evaluation of the function
                        represented by this DiffObj, at the variable values given by val_dict.
        '''
 
        operand_val = self.operand_list[0].get_val(value_dict)
        if self.operator == 'sin':
            return math.sin(operand_val)
        elif self.operator == 'cos':
            return math.cos(operand_val)
        elif self.operator == 'tan':
            result = math.tan(operand_val)
            return result
        elif self.operator == 'log':
            try:
                result = math.log(operand_val)
                return result
            except:
                raise ValueError('Only positive values are permitted with log.')
        elif self.operator == 'exp':
            result = math.exp(operand_val)
            return result

    def get_der(self, value_dict, with_respect_to=None):
        '''
        INPUT
        ======
        value_dict:         A dictionary, whose keys are strings representing variables which feature
                            in the formula represented by this DiffObj. The values at those keys are
                            the values at which the gradient of formula representing this DiffObj will 
                            be evaluated.
                            
                            E.g. For a DiffObj which represents the function f(x,y) = x + y, the value_dict
                            argument may look like value_dict = {'x': 10, 'y': 5}
        OUTPUT
        ======
        result:             A dictionary, whose keys are strings representing variables which feature 
                            in the formula represented by this DiffObj. The value associated withe each
                            key is a floating point number which is the partial derivative of this DiffObj 
                            with respect to that variable.
        with_respect_to:    A list of strings representing variables, with respect to which we want the 
                            gradient of this DifObj. By default, if this list is not provided, then the
                            gradient with respect to all variables featuring in the DiffObj is returned.
        '''
 
        if not with_respect_to: with_respect_to = self.name_list
        df = {}
        op1 = self.operand_list[0]
        if self.operator == 'sin':
            for w in with_respect_to:
                dw = math.cos(op1.get_val(value_dict))*op1.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'cos':
            for w in with_respect_to:
                dw = -math.sin(op1.get_val(value_dict))*op1.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'tan':
            sec_x = 1.0/math.cos(op1.get_val(value_dict))
            for w in with_respect_to:
                dw = (sec_x**2)*op1.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'log':
            try:
                one_by_var = 1.0/op1.get_val(value_dict)
            except:
                raise ValueError('Log cannot be evaluated at 0.')
            for w in with_respect_to:
                dw = one_by_var*op1.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'exp':
            func_val = math.exp(op1.get_val(value_dict))
            for w in with_respect_to:
                dw = func_val*op1.get_der(value_dict, [w])[w]
                df[w] = dw

        if len(df) == 0: df = {'' : 0}
        return df

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'x': Variable('x'),'y':Variable('y')})