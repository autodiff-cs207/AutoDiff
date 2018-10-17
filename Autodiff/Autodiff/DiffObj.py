class DiffObj():
	def __init__(self,name,obj_type='variable',name_list=None,term_left=0,term_right=0,degree=0):
		if name_list==None:
			self.name_list=[name]
		else:
			self.name_list=name_list
		self.degree=degree
		self.name=name
		self.obj_type=obj_type
		self.term_left=term_left
		self.term_right=term_right
# /////////////////////////////////
# factory methods
	@staticmethod
	def scaler():
		pass
	@staticmethod
	def variable(name):
		return DiffObj(name=name,obj_type='variable')
	@staticmethod
	def vector():
		pass
	@staticmethod
	def makePoly(term,degree=0):
		return DiffObj(name='poly',obj_type='poly',name_list=term.name_list,term_left=term,degree=degree)
		
# /////////////////////////////////
# operator overloads
	def __add__(self,right):
		return DiffObj(name='add',obj_type='add',name_list=self.name_list+right.name_list,term_left=self,term_right=right)
	def __radd__(self,left):
		pass
	def __mul__(self,right):
		pass
	def __rmul__(self,left):
		pass
	def __pow__(self,left):
		pass
# /////////////////////////////////
# member functions
	def get_val(self, name_dic):
		if self.obj_type=='add':
			if set(self.name_list)==set(name_dic.keys()) or set(self.name_list) < set(name_dic.keys()):
				return self.term_left.get_val(name_dic)+self.term_right.get_val(name_dic)
			else:
				raise Exception('In get_val: variable needed not found')
		if self.obj_type=='scaler':
			return self.var_left
		if self.obj_type=='variable':
			return name_dic[self.name]
		if self.obj_type=='poly':
			return pow(self.term_left.get_val(name_dic),self.degree)
		if self.obj_type=='mul':
			pass
	def get_der(self,name_needed,name_dic):
		if name_needed not in self.name_list:
			return 0
		if self.obj_type=='add':
			return self.term_left.get_der(name_needed,name_dic)+self.term_right.get_der(name_needed,name_dic)
		if self.obj_type=='variable':
			return 1
		if self.obj_type=='scaler':
			pass
		if self.obj_type=='poly':
			return self.degree*pow(self.term_left.get_val(name_dic),self.degree-1)*self.term_left.get_der(name_needed,name_dic)
		if self.obj_type=='mul':
			pass

if __name__=='__main__':

	x=DiffObj.variable('x')
	y=DiffObj.variable('y')
	z=DiffObj.variable('z')
	w=x+y+z
	print('for function x+y+z, the value at: {\'x\':1,\'y\':1,\'z\':1}')
	print(w.get_val({'x':1,'y':1,'z':1}))
	print('for function x+y+z, the value at: {\'x\':2,\'y\':2,\'z\':2}')
	print(w.get_val({'x':2,'y':2,'z':2}))
	print('for function x+y+z, the value at: {\'x\':3,\'y\':3,\'z\':3}')
	print(w.get_val({'x':3,'y':3,'z':3}))

	j=DiffObj.variable('j')
	j3=DiffObj.makePoly(j,degree=3)
	print('for function j^3, the value at: {\'j\':1}')
	print(j3.get_val({'j':1}))
	print('for function j^3, the value at: {\'j\':2}')
	print(j3.get_val({'j':2}))
	print('for function j^3, the value at: {\'j\':3}')
	print(j3.get_val({'j':3}))

	j3andw=j3+x+y+z
	print('for function j^3+x+y+z, the value at: {\'x\':1,\'y\':1,\'z\':1,\'j\':1}')
	print(j3andw.get_val({'x':1,'y':1,'z':1,'j':1}))
	print('for function j^3+x+y+z, the value at: {\'x\':2,\'y\':2,\'z\':2,\'j\':2}')
	print(j3andw.get_val({'x':2,'y':2,'z':2,'j':2}))
	print('for function j^3+x+y+z, the value at: {\'x\':3,\'y\':3,\'z\':3,\'j\':3}')
	print(j3andw.get_val({'x':3,'y':3,'z':3,'j':3}))

# /////////////////////////////////

	x=DiffObj.variable('x')
	y=DiffObj.variable('y')
	z=DiffObj.variable('z')
	w=x+y+z

	print('for function x+y+z, the derivative of x at: {\'x\':1,\'y\':1,\'z\':1}')
	print(w.get_der('x',{'x':1,'y':1,'z':1}))
	print('for function x+y+z, the derivative of x at: {\'x\':2,\'y\':2,\'z\':2}')
	print(w.get_der('x',{'x':2,'y':2,'z':2}))
	print('for function x+y+z, the derivative of x at: {\'x\':2,\'y\':2,\'z\':2}')
	print(w.get_der('x',{'x':3,'y':3,'z':3}))

	j=DiffObj.variable('j')
	j4=DiffObj.makePoly(j,degree=4)
	print('for function j^4, the derivative of j at: {\'j\':1}')
	print(j3.get_der('j',{'j':1}))
	print('for function j^4, the derivative of j at: {\'j\':2}')
	print(j3.get_der('j',{'j':2}))
	print('for function j^4, the derivative of j at: {\'j\':3}')
	print(j3.get_der('j',{'j':3}))

	j4andw=j4+x+y+z+j+j+j
	print('for function j^4+x+y+z+j+j+j, the derivative of j at: {\'x\':1,\'y\':1,\'z\':1,\'j\':1}')
	print(j4andw.get_der('j',{'x':1,'y':1,'z':1,'j':1}))
	print('for function j^4+x+y+z+j+j+j, the derivative of j at: {\'x\':2,\'y\':2,\'z\':2,\'j\':2}')
	print(j4andw.get_der('j',{'x':2,'y':2,'z':2,'j':2}))
	print('for function j^4+x+y+z+j+j+j, the derivative of j at: {\'x\':3,\'y\':3,\'z\':3,\'j\':3}')
	print(j4andw.get_der('j',{'x':3,'y':3,'z':3,'j':3}))