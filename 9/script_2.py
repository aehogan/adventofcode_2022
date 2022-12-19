#!/usr/bin/python3

import numpy as np

knots = np.zeros((10, 2), dtype=int)

f = open("data.dat", "r")

board = np.zeros((2000, 2000), dtype=int)

def update_knot(knot1, knot2):
    if np.abs(knot1[0] - knot2[0]) <= 1 and np.abs(knot1[1] - knot2[1]) <= 1: # touching, no need to update tail
        pass
    elif knot1[0] != knot2[0] and knot1[1] != knot2[1]: # go diagonal
        if knot1[1] > knot2[1]:
            knot2[1] = knot2[1] + 1
        else:
            knot2[1] = knot2[1] - 1
        if knot1[0] > knot2[0]:
            knot2[0] = knot2[0] + 1
        else:
            knot2[0] = knot2[0] - 1
    elif knot1[0] == knot2[0]: # up/down
        if knot1[1] > knot2[1]:
            knot2[1] = knot2[1] + 1
        else:
            knot2[1] = knot2[1] - 1
    elif knot1[1] == knot2[1]: # left/right
        if knot1[0] > knot2[0]:
            knot2[0] = knot2[0] + 1
        else:
            knot2[0] = knot2[0] - 1
    return

for line in f.readlines():
    split_line = line.split()
    direction = split_line[0]
    steps = int(split_line[1])
    print(direction, steps, knots)
    for i in range(steps):
        if direction == "R":
            knots[0][0] += 1
        elif direction == "L":
            knots[0][0] -= 1
        elif direction == "U":
            knots[0][1] += 1
        elif direction == "D":
            knots[0][1] -= 1

        for j in range(1,len(knots)):
            update_knot(knots[j-1], knots[j])

        board[1000+knots[9][0]][1000+knots[9][1]] = 1

values, counts = np.unique(board, return_counts=True)

print(knots)
print(board)
print(values, counts)

