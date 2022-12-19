#!/usr/bin/python3

import numpy as np

f = open("data.dat", "r")

calories = []

current_elf_inventory = []

for line in f.readlines():
    if line == "\n":
        current_elf_calories = np.sum(np.array(current_elf_inventory))
        current_elf_inventory = []
        calories.append(current_elf_calories)
    else:
        current_elf_inventory.append(float(line))

calories = np.array(calories)
calories.sort()

print(calories[-3] + calories[-2] + calories[-1])
