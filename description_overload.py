
'''
overloaded operators: 

__add__
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


__mult__
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


__sub__
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

__trudiv__
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

