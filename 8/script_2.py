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

scenic_score = np.zeros_like(forest)

def get_scenic_score(forest, i, j):
    check_height = forest[i][j]

    score_from_top = 0
    idx = i - 1
    while idx >= 0:
        score_from_top += 1
        if forest[idx][j] >= check_height:
           break
        idx -= 1

    score_from_bottom = 0
    idx = i + 1
    while idx < len(forest):
        score_from_bottom += 1
        if forest[idx][j] >= check_height:
           break
        idx += 1

    score_from_left = 0
    idx = j - 1
    while idx >= 0:
        score_from_left += 1
        if forest[i][idx] >= check_height:
           break
        idx -= 1

    score_from_right = 0
    idx = j + 1
    while idx < len(forest):
        score_from_right += 1
        if forest[i][idx] >= check_height:
           break
        idx += 1

    return score_from_top * score_from_bottom * score_from_left * score_from_right

for i, row in enumerate(forest):
    for j, tree_height in enumerate(row):
        scenic_score[i][j] = get_scenic_score(forest, i, j)

scenic_score[:,0] = 0
scenic_score[:,-1] = 0
scenic_score[0,:] = 0
scenic_score[-1,:] = 0

highest_score = -1

for i, row in enumerate(scenic_score):
    for j, score in enumerate(row):
        if score > highest_score:
            highest_score = score



print(forest)
print(scenic_score)
print(highest_score)

