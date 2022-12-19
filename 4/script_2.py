#!/usr/bin/python3

import numpy as np

f = open("data.dat", "r")

num = 0

for line in f.readlines():
    split_line = line.strip().split(",")

    assignment_a = np.zeros(100)
    assignment_b = np.zeros(100)

    line_a = split_line[0].split("-")
    line_a = [int(numb) for numb in line_a]

    line_b = split_line[1].split("-")
    line_b = [int(numb) for numb in line_b]

    for i in range(line_a[0], line_a[1]+1):
        assignment_a[i] = 1

    for i in range(line_b[0], line_b[1]+1):
        assignment_b[i] = 1

    overlap = False
    for idx, val in enumerate(assignment_a):
        if val == 1 and assignment_b[idx] == 1:
            overlap = True

    if overlap:
        print(split_line)
        num += 1
    else:
        overlap = False
        for idx, val in enumerate(assignment_b):
            if val == 1 and assignment_a[idx] == 1:
                overlap = True

        if overlap:
            print(split_line)
            num += 1

print(num)

