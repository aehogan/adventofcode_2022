#!/usr/bin/python3

import numpy as np

data = np.loadtxt("data.dat", delimiter=",", dtype=int)

lava_bits = [[list(pt)] for pt in data]

def count_lava_bit_sides(lava_bit):
    sides = 6*len(lava_bit)
    shared_sides = 0

    for k, pt1 in enumerate(lava_bit):
        pt1 = np.array(pt1)
        for l, pt2 in enumerate(lava_bit):
            if k <= l:
                continue
            pt2 = np.array(pt2)
            if np.linalg.norm(pt1-pt2) == 1:
                shared_sides += 1
    
    sides -= 2 * shared_sides
                        
    return sides

def merge_once():
    global lava_bits
    print(len(lava_bits))
    for i, lava_bit in enumerate(lava_bits):
        for j, other_lava_bit in enumerate(lava_bits):
            if i == j:
                continue
            for k, pt1 in enumerate(lava_bit):
                pt1 = np.array(pt1)
                for l, pt2 in enumerate(other_lava_bit):
                    pt2 = np.array(pt2)
                    if np.linalg.norm(pt1-pt2) == 1:
                        merged_lava_bit = lava_bit + other_lava_bit
                        lava_bits.remove(lava_bit)
                        lava_bits.remove(other_lava_bit)
                        lava_bits.append(merged_lava_bit)
                        return True
    return False
    
while merge_once():
    pass

sum = 0
for lava_bit in lava_bits:
    sum += count_lava_bit_sides(lava_bit)
    print(lava_bit, count_lava_bit_sides(lava_bit))
print(sum)

