#!/usr/bin/python3

import numpy as np

buffer = []

len_to_look_for = 14

f = open("data.dat", "r")

for line in f.readlines():
    for idx, char in enumerate(line.strip()):
        buffer.append(char)
        buffer = buffer[-len_to_look_for:]
        unique = True
        if len(buffer) == len_to_look_for:
            for i in range(len_to_look_for):
                if buffer[i] in buffer[:i] + buffer[i+1:]:
                    unique = False
            if unique == True:
                print(idx+1)
                break
