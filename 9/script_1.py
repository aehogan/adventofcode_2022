#!/usr/bin/python3

import numpy as np

head_loc = np.zeros(2, dtype=int)
tail_loc = np.zeros(2, dtype=int)

f = open("data.dat", "r")

tail_has_visited = [np.copy(tail_loc)]

def update_tail():
    if np.abs(head_loc[0] - tail_loc[0]) <= 1 and np.abs(head_loc[1] - tail_loc[1]) <= 1: # touching, no need to update tail
        pass
    elif head_loc[0] != tail_loc[0] and head_loc[1] != tail_loc[1]: # go diagonal
        if head_loc[1] > tail_loc[1]:
            tail_loc[1] = tail_loc[1] + 1
        else:
            tail_loc[1] = tail_loc[1] - 1
        if head_loc[0] > tail_loc[0]:
            tail_loc[0] = tail_loc[0] + 1
        else:
            tail_loc[0] = tail_loc[0] - 1
    elif head_loc[0] == tail_loc[0]: # up/down
        if head_loc[1] > tail_loc[1]:
            tail_loc[1] = tail_loc[1] + 1
        else:
            tail_loc[1] = tail_loc[1] - 1
    elif head_loc[1] == tail_loc[1]: # left/right
        if head_loc[0] > tail_loc[0]:
            tail_loc[0] = tail_loc[0] + 1
        else:
            tail_loc[0] = tail_loc[0] - 1
    return

for line in f.readlines():
    split_line = line.split()
    direction = split_line[0]
    steps = int(split_line[1])
    print(direction, steps, head_loc, tail_loc)
    for i in range(steps):
        if direction == "R":
            head_loc[0] += 1
        elif direction == "L":
            head_loc[0] -= 1
        elif direction == "U":
            head_loc[1] += 1
        elif direction == "D":
            head_loc[1] -= 1
        update_tail()
        if np.any([np.all(tail_loc == item) for item in tail_has_visited]):
            pass
        else:
            tail_has_visited.append(np.copy(tail_loc))

print(head_loc, tail_loc)
print(len(tail_has_visited))
