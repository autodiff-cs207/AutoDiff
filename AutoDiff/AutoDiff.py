import math

class DiffObj():
    OVERLOADED_OPERATORS = ['add', 'subtract', 'multiply', 'divide',
            'power', 'neg']
    def __init__(self, name_list, operator, operand_list):
        self.name_list = name_list
        self.operator = operator
        self.operand_list = operand_list
    def get_val(self, value_dict):
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
        return MathOps.getUnaryOperator('sin', obj)
    @classmethod
    def cos(cls, obj):
        return MathOps.getUnaryOperator('cos', obj)
    @classmethod
    def tan(cls,obj):
        return MathOps.getUnaryOperator('tan', obj)
    @classmethod
    def log(cls, obj):
        return MathOps.getUnaryOperator('log', obj)
    def get_val(self, value_dict):
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

    def get_der(self, value_dict, with_respect_to=None):
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

        if len(df) == 0: df = {'' : 0}
        return df
