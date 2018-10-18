1- What are the core data structures?

There are three core data structures in our implementation: 
1) The list of names that is stored in every Diffobj instance to indicate the component of the instance. Eg. for the equation w=sin(x)+y, the name list of variable x is ['x'], the name list of variable y is ['y'] and the name list of function w is ['w','x','y']. For more details, please look into the test examples in the [DiffObj.py] directly.

2) The dictionary of names that is passed through instances during the process of calculating values and derivatives. Eg. w.get_val(dic) need to pass in a dictionary indicating the values of each instance. And this dictionary of names and values will be used for further calculations in the connecting instances. For more details, please look into the test examples in the [DiffObj.py] directly.

3) The tree structured linkage between instances. We use tree structure to keep the relationships between variables and functions. Eg, for the equation w=sin(x)+y, node w will have two pointers(references) pointing to x and y. So when calculating the value and derivatives of w, we can refer to x and y easily in a top down fashion. For more details, please look into the test examples in the [DiffObj.py] directly.

2- What classes will you implement?

For right now, our experiment tries gather everything into a single class: Diffobj for the sake of quick experiment. In the future, we planed to decompose Diffobj into several classes including:

Member Classes:
--DiffObj base class
--Variable(Diffobj)
--Scaler(Diffobj)
--Vector(Diffobj)
--Matrix(Diffobj)
--Poly(Diffobj)
--Sin(Diffobj)
--Cos(Diffobj)
--Other classes

Extension Classes (Includes but not constrained to):
--BackProp
--Reverse
--Mixed

Application Classes
--AppMock

etc

3- What method and name attributes will your classes have?

As we have implemented:

Factory functions returning various kinds of instances:
--Diffobj.scaler()
--Diffobj.variable()
--Diffobj.vector()
--Diffobj.matrix()

--__add__
--__radd__
--Diffobj.add()
--__minus__
--__rminus__
--Diffobj.minus()
--__pow__
--Diffobj.makePoly()
--__mul__
--__rmul__
--Diffobj.mul()
--Diffobj.sin()
--Diffobj.asin()
--Diffobj.cos()
--Diffobj.acos()
--Diffobj.tan()
--Diffobj.atan()

etc

Main Functions Methods

--Diffobj.get_val
--Diffobj.get_der

4- What external dependencies will you rely on?

We mainly depend on numpy
But may have other dependencies when our development goes further

5- How will you deal with elementary functions like sin and exp?

We have gaven very good explanation in our demo code in [Diffobj.py]. The elementary function such as sin and exp(poly in our code) is designed as Factory functions in our implementations. The Diffobj.sin or Diffobj.exp will mainly receive an Diffobj instance as argument and return a father Diffobj instance pointing to the argument instance. The generated father instance will be labeled as sin or exp and will perform accordingly according to their special type. The type information are stored in the Diffobj instance.