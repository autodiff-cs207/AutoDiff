class DiffObj():
	def __init__(self,name,obj_type='variable',name_list=None,val_left=0,val_right=0,der_left=0,der_right=0):
		if name_list==None:
			self.name_list=[name]
		else:
			self.name_list=name_list
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
	def makePoly():
		pass
# /////////////////////////////////
# operator overloads
	def __add__(self,right):
		return DiffObj(name='add',obj_type='add',name_list=self.name_list+right.name_list,val_left=self,val_right=right)
	def __radd__(self,left):
		pass
# /////////////////////////////////
# member functions
	def get_var(self, name_dic={}):
		if self.obj_type=='add':
			if set(self.name_list)==set(name_dic.keys()) or set(self.name_list) < set(name_dic.keys()):
				return self.val_left.get_var(name_dic)+self.val_right.get_var(name_dic)
			else:
				raise Exception('dic name error')
		if self.obj_type=='scaler':
			return slef.var_left
		if self.obj_type=='variable':
			return name_dic[self.name]
	def det_der(self):
		pass

if __name__=='__main__':
	x=DiffObj.variable('x')
	y=DiffObj.variable('y')
	z=DiffObj.variable('z')
	w=x+y+z
	print(w.get_var({'x':1,'y':1,'z':1}))
	print(w.get_var({'x':2,'y':2,'z':2}))
	print(w.get_var({'x':4,'y':4,'z':4}))

	# print(z.get_der({'x':1,'y':1}))
	# print(z.get_der({'x':2,'y':2}))

	# z=DiffObj.makePoly(x,y)+y