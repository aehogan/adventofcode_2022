#!/usr/bin/python3

import numpy as np

f = open("data.dat", "r")

lines = [line.strip() for line in f.readlines()]

array = np.array([int(num) for num in lines], dtype=int)
indices = np.arange(len(array), dtype=int)

working_array = list(array.copy())
working_indices = list(indices.copy())

#print(array)
#print(indices)

print(array)
print()

for i, val in enumerate(array):
    j = np.argwhere(np.array(working_indices) == i)[0][0]

    working_array.pop(j)
    working_indices.pop(j)

    new_location = ( j + val )
    while new_location < 0:
        new_location += len(array)
        working_array = list(np.roll(working_array, 1))
        working_indices = list(np.roll(working_indices, 1))
    while new_location >= len(array):
        new_location -= len(array)
        working_array = list(np.roll(working_array, -1))
        working_indices = list(np.roll(working_indices, -1))

    working_array.insert(new_location, val)
    working_indices.insert(new_location, val)
    
    #print("i", i, "j", j, "val", val, "new_location", new_location)
    #print()
    #print(working_array)
    #print()
    

i = np.argwhere(np.array(working_array) == 0)[0][0]

print(i)
a = ( i + 1000 ) % len(working_array)
b = ( i + 2000 ) % len(working_array)
c = ( i + 3000 ) % len(working_array)
print(working_array[a],  working_array[b],  working_array[c])
print(working_array[a] + working_array[b] + working_array[c])

# 8369 is low




