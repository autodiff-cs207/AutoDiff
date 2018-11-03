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
            return self.operand_list[0].get_val(value_dict)/self.operand_list[1].get_val(value_dict)

    def get_der(self, value_dict):
        raise NotImplementedError
    
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
    def __div__(self, other):
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
    def get_der(self):
        pass
