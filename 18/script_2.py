#!/usr/bin/python3

import numpy as np

data = np.loadtxt("data.dat", delimiter=",", dtype=int)

lava_bits = [[list(pt)] for pt in data]

UNKNOWN     = 0b0000
TRAPPED_AIR = 0b0011
FREE_AIR    = 0b0111
LAVA        = 0b1101

SOMETHING_MASK = 0b0001

# data & 0b0001 = something
# data & 0b0010 = air of sometype
# data & 0b1000 = lava

def get_trapped_pockets():
    global lava_bits
    flat_lava_bits = np.array([item for sublist in lava_bits for item in sublist], dtype=int)

    xlo = np.min(flat_lava_bits[:, 0])
    xhi = np.max(flat_lava_bits[:, 0])
    ylo = np.min(flat_lava_bits[:, 1])
    yhi = np.max(flat_lava_bits[:, 1])
    zlo = np.min(flat_lava_bits[:, 2])
    zhi = np.max(flat_lava_bits[:, 2])
    
    flat_lava_bits[:, 0] -= xlo
    flat_lava_bits[:, 1] -= ylo
    flat_lava_bits[:, 2] -= zlo
    
    xlen = xhi-xlo+1
    ylen = yhi-ylo+1
    zlen = zhi-zlo+1
    
    map_3d = np.zeros((xlen, ylen, zlen), dtype=int)
    
    map_3d[0, :, :] = FREE_AIR
    map_3d[xlen-1, :, :] = FREE_AIR
    map_3d[:, 0, :] = FREE_AIR
    map_3d[:, ylen-1, :] = FREE_AIR
    map_3d[:, :, 0] = FREE_AIR
    map_3d[:, :, zlen-1] = FREE_AIR

    for lava_bit in flat_lava_bits:
        map_3d[lava_bit[0], lava_bit[1], lava_bit[2]] = LAVA
    
    keep_looping = True
    while keep_looping:
        keep_looping = False
        for i, yz_plane in enumerate(map_3d):
            for j, z_row in enumerate(yz_plane):
                for k, ele in enumerate(z_row):
                    if ele & SOMETHING_MASK:
                        continue
                    #print(ele, i, j, k)
                    #print()
                    up      = np.array((i, j, k+1), dtype=int)
                    down    = np.array((i, j, k-1), dtype=int)
                    left    = np.array((i, j+1, k), dtype=int)
                    right   = np.array((i, j-1, k), dtype=int)
                    forward = np.array((i+1, j, k), dtype=int)
                    back    = np.array((i-1, j, k), dtype=int)
                    directions = [up, down, left, right, forward, back]
                    for direction in directions:
                        if direction[0] < 0 or direction[0] > xlen or \
                           direction[1] < 0 or direction[1] > ylen or \
                           direction[2] < 0 or direction[2] > zlen:
                            continue
                        if map_3d[direction[0], direction[1], direction[2]] == FREE_AIR:
                            map_3d[i, j, k] = FREE_AIR
                            keep_looping = True
                            break
    
    trapped_air_bits = []
    
    for i, yz_plane in enumerate(map_3d):
        for j, z_row in enumerate(yz_plane):
            for k, ele in enumerate(z_row):
                if ele == UNKNOWN:
                    map_3d[i, j, k] = TRAPPED_AIR
                    trapped_air_bits.append([i, j, k])
    
    return [trapped_air_bits]

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
    
def count_air_bit_sides(air_bit):
    sides = 6*len(air_bit)
    shared_sides = 0

    for k, pt1 in enumerate(air_bit):
        pt1 = np.array(pt1)
        for l, pt2 in enumerate(air_bit):
            if k <= l:
                continue
            pt2 = np.array(pt2)
            if np.linalg.norm(pt1-pt2) == 1:
                shared_sides += 1
    
    sides -= 2 * shared_sides
                        
    return sides

def merge_once_lava():
    global lava_bits
    for i, lava_bit in enumerate(lava_bits):
        print(len(lava_bits))
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
    
def merge_once_air():
    global trapped_air_bits
    for i, lava_bit in enumerate(trapped_air_bits):
        for j, other_lava_bit in enumerate(trapped_air_bits):
            if i == j:
                continue
            for k, pt1 in enumerate(lava_bit):
                pt1 = np.array(pt1)
                for l, pt2 in enumerate(other_lava_bit):
                    pt2 = np.array(pt2)
                    if np.linalg.norm(pt1-pt2) == 1:
                        merged_lava_bit = lava_bit + other_lava_bit
                        trapped_air_bits.remove(lava_bit)
                        trapped_air_bits.remove(other_lava_bit)
                        trapped_air_bits.append(merged_lava_bit)
                        return True
    return False
    
while merge_once_lava():
    pass

sum = 0
print("- lava -")
print(lava_bits)
for lava_bit in lava_bits:
    sum += count_lava_bit_sides(lava_bit)
    print(lava_bit, count_lava_bit_sides(lava_bit))

trapped_air_bits = get_trapped_pockets()

while merge_once_air():
    pass

print("- air -")
print(trapped_air_bits)

for air_bit in trapped_air_bits:
    sum -= count_air_bit_sides(air_bit)
    print(air_bit, count_air_bit_sides(air_bit))

print(sum)

