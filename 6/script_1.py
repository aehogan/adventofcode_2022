#!/usr/bin/python3

import numpy as np

buffer = []

f = open("data.dat", "r")

for line in f.readlines():
    for idx, char in enumerate(line.strip()):
        buffer.append(char)
        buffer = buffer[-4:]
        unique = True
        if len(buffer) == 4:
            for i in range(4):
                if buffer[i] in buffer[:i] + buffer[i+1:]:
                    unique = False
            if unique == True:
                print(idx+1)
                break
