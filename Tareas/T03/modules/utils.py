from itertools import tee


a = (i for i in range(10))
print(type(a))
(b, c)= tee(a)
print(b is type(a))
print(list(b))
print(list(b))
print(list(c))
print(list(c))
