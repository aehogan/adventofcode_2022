#!/usr/bin/python3

import numpy as np

f = open("data.dat", "r")

most_calories = -1.0

current_elf_inventory = []

for line in f.readlines():
    #print(line)
    if line == "\n":
        current_elf_calories = np.sum(np.array(current_elf_inventory))
        current_elf_inventory = []
        if current_elf_calories > most_calories:
            most_calories = current_elf_calories
    else:
        current_elf_inventory.append(float(line))

print(most_calories)
