import numpy as np

a = np.array([1,2,3])
b = np.array([4,5,6])

# print(a)
# print(b)

c = np.array([a,b])
print(c)
# d = np.hsplit(c, len(a))
# print(d)
print(np.reshape(c, (len(a),-1)))
