#!/usr/bin/python3

import numpy as np

f = open("data.dat", "r")

lines = f.readlines()

forest = []

for line in lines:
    line = line.strip()
    row = []
    for number in line:
        row.append(int(number))
    forest.append(row)

forest = np.array(forest)

visibility = np.zeros_like(forest)

def is_visible(forest, i, j):
    check_height = forest[i][j]

    visible_from_top = True
    idx = i - 1
    while idx >= 0:
        if forest[idx][j] >= check_height:
           visible_from_top = False
        idx -= 1

    visible_from_bottom = True
    idx = i + 1
    while idx < len(forest):
        if forest[idx][j] >= check_height:
           visible_from_bottom = False
        idx += 1

    visible_from_left = True
    idx = j - 1
    while idx >= 0:
        if forest[i][idx] >= check_height:
           visible_from_left = False
        idx -= 1

    visible_from_right = True
    idx = j + 1
    while idx < len(forest):
        if forest[i][idx] >= check_height:
           visible_from_right = False
        idx += 1

    if visible_from_left or visible_from_right or visible_from_top or visible_from_bottom:
        visible = True
    else:
        visible = False

    return visible

for i, row in enumerate(forest):
    for j, tree_height in enumerate(row):
        if is_visible(forest, i, j):
            visibility[i, j] = 1

visibility[:,0] = 1
visibility[:,-1] = 1
visibility[0,:] = 1
visibility[-1,:] = 1

total_vis = 0

for i, row in enumerate(forest):
    for j, tree_height in enumerate(row):
        if visibility[i, j] == 1:
            total_vis += 1



print(forest)
print(visibility)
print(total_vis)

