#!/usr/bin/python3

import numpy as np

x = np.loadtxt("data.dat")
x *= 811589153
indices = list(range(len(x)))
print(x, indices)

for _ in range(10):
    for i, num in enumerate(x):
        j = indices.index(i)
        indices.pop(j)
        indices.insert(int((num + j) % len(indices)), i)

y = x.copy()
for i, num in enumerate(x):
    y[indices.index(i)] = num

print(y, indices)
y = list(y)
i = y.index(0)

a = (i + 1000) % len(y)
b = (i + 2000) % len(y)
c = (i + 3000) % len(y)
print(y[a],  y[b],  y[c])
print(y[a] + y[b] + y[c])




