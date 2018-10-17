class DiffObj():
	def __init__(self,name,obj_type='variable',name_list=None,val_left=0,val_right=0,der_left=0,der_right=0,degree=0):
		if name_list==None:
			self.name_list=[name]
		else:
			self.name_list=name_list
		self.degree=degree
		self.name=name
		self.obj_type=obj_type
		self.val_left=val_left
		self.val_right=val_right
		self.der_left=der_left
		self.der_right=der_right
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
		return DiffObj(name='poly',obj_type='poly',name_list=term.name_list,val_left=term,degree=degree)
		
# /////////////////////////////////
# operator overloads
	def __add__(self,right):
		return DiffObj(name='add',obj_type='add',name_list=self.name_list+right.name_list,val_left=self,val_right=right)
	def __radd__(self,left):
		pass
# /////////////////////////////////
# member functions
	def get_val(self, name_dic={}):
		if self.obj_type=='add':
			if set(self.name_list)==set(name_dic.keys()) or set(self.name_list) < set(name_dic.keys()):
				return self.val_left.get_val(name_dic)+self.val_right.get_val(name_dic)
			else:
				raise Exception('dic name error')
		if self.obj_type=='scaler':
			return self.var_left
		if self.obj_type=='variable':
			return name_dic[self.name]
		if self.obj_type=='poly':
			return pow(self.val_left.get_val(name_dic),self.degree)
	def det_der(self):
		pass

if __name__=='__main__':
	x=DiffObj.variable('x')
	y=DiffObj.variable('y')
	z=DiffObj.variable('z')
	w=x+y+z
	print(w.get_val({'x':1,'y':1,'z':1}))
	print(w.get_val({'x':2,'y':2,'z':2}))
	print(w.get_val({'x':3,'y':3,'z':3}))

	j=DiffObj.variable('j')
	j3=DiffObj.makePoly(j,degree=3)
	print(j3.get_val({'j':1}))
	print(j3.get_val({'j':2}))
	print(j3.get_val({'j':3}))

	j3andw=j3+x+y+z
	print(j3andw.get_val({'x':1,'y':1,'z':1,'j':1}))
	print(j3andw.get_val({'x':2,'y':2,'z':2,'j':2}))
	print(j3andw.get_val({'x':3,'y':3,'z':3,'j':3}))

	# print(z.get_der({'x':1,'y':1}))
	# print(z.get_der({'x':2,'y':2}))

	# z=DiffObj.makePoly(x,y)+y
