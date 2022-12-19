#!/usr/bin/python3

import numpy as np

data = np.loadtxt("runlog.log", dtype=int)

#print(data)

diffs = []

for idx, row in enumerate(data):
    if idx == 0 or idx >= len(data) - 1:
        continue
    diffs.append(data[idx+1][1] - data[idx][1])
        
diffs = np.array(diffs)

#print(diffs)

num_to_compare = 50

first_couple_numbers = diffs[:num_to_compare]

for d_idx, d_val in enumerate(diffs):
    if d_idx == 0 or d_idx >= len(diffs) - num_to_compare:
        continue
    repeat = True
    for f_idx, f_val in enumerate(first_couple_numbers):
        if diffs[d_idx + f_idx] != first_couple_numbers[f_idx]:
            repeat = False
    if repeat:
        print(repeat, first_couple_numbers, d_idx)
