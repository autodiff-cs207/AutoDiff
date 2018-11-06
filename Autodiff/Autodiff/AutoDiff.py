import math

class DiffObj():
    SUPPORTED_OPERATORS = ['add', 'subtract', 'multiply', 'divide',
            'power']
    def __init__(self, name_list, operator, operand_list):
        self.name_list = name_list
        self.operator = operator
        self.operand_list = operand_list
    def get_val(self, value_dict):
        if self.operator not in DiffObj.SUPPORTED_OPERATORS:
            print('{} is not a supported operator'.format(self.operator))
            return
        if self.operator == 'add':
            return self.operand_list[0].get_val(value_dict) + self.operand_list[1].get_val(value_dict)
        elif self.operator == 'subtract':
            return self.operand_list[0].get_val(value_dict) - self.operand_list[1].get_val(value_dict)
        elif self.operator == 'multiply':
            return self.operand_list[0].get_val(value_dict)*self.operand_list[1].get_val(value_dict)
        elif self.operator == 'divide':
            return self.operand_list[0].get_val(value_dict)/self.operand_list[1].get_val(value_dict)
        elif self.operator == 'power':
            return self.operand_list[0].get_val(value_dict)**self.operand_list[1].get_val(value_dict)

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
            for w in with_respect_to:
                dw = (op2_val*op1.get_der(value_dict, [w])[w] - op1_val*op2.get_der(value_dict, [w])[w])/(op2_val**2)
                df[w] = dw
        elif self.operator == 'power':
            func_val = op1_val**op2_val
            for w in with_respect_to:
                dw = func_val*((op2_val/op1_val)*op1.get_der(value_dict, [w])[w] + 
                        math.log(op1_val)*op2.get_der(value_dict, [w])[w])
                df[w] = dw
        if len(df) == 0: df = {'' : 0}
        return df

    def getBinaryOperator(self, other, operator_name):
        try:
            other_name_list = other.name_list
            return DiffObj(self.name_list + other_name_list,
                    operator_name, [self, other])
        except AttributeError:
            print('Operands need to be of type DiffObj.')

    def __add__(self, other):
        return self.getBinaryOperator(other, 'add')
    def __sub__(self, other):
        return self.getBinaryOperator(other, 'subtract')
    def __mul__(self, other):
        return self.getBinaryOperator(other, 'multiply')
    def __truediv__(self, other):
        return self.getBinaryOperator(other, 'divide')
    def __pow__(self, other):
        return self.getBinaryOperator(other, 'power')
    
   
class Variable(DiffObj):
    def __init__(self, var_name):
        self.var_name = var_name
        super(Variable, self).__init__([var_name], None, None)
    
    def get_val(self, value_dict):
        if self.var_name not in value_dict:
            print('You have not provided a value for {}'.format(self.var_name))
            return
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
        except AttributeError:
            print('Only objects of type DiffObj are permitted.')
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
            return math.tan(operand_val)
        elif self.operator == 'log':
            return math.log(operand_val)

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
            for w in with_respect_to:
                dw = (1.0/math.cos(op1.get_val(value_dict))**2)*op1.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'log':
            for w in with_respect_to:
                dw = 1.0/op1.get_val(value_dict)*op1.get_der(value_dict, [w])[w]
                df[w] = dw

        if len(df) == 0: df = {'' : 0}
        return df
