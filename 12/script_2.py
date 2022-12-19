#!/usr/bin/python3

import os
import numpy as np
import termcolor

f = open("data.dat", "r")
lines = [line.strip() for line in f.readlines()]

height_map = []
start_loc = None
end_loc = None

for y, line in enumerate(lines):
    height_line = []
    for x, char in enumerate(line):
        height = ord(char) - 97
        if height == -14:
            start_loc = np.array([y, x])
            height = 0
        elif height == -28:
            end_loc = np.array([y, x])
            height = 25
        height_line.append(height)
    height_map.append(height_line)

height_map = np.array(height_map, dtype=int)


print_chars = ["□", "▤", "▥", "▧", "▨", "▦", "▩", "■"]
colors = ["white", "cyan", "magenta", "blue", "yellow", "green", "red"]

def get_steps_for_loc(x, y):
    step_map = np.zeros_like(height_map) - 1
    step_map[y, x] = 0
    for i in range(400):
        if step_map[end_loc[0], end_loc[1]] != -1:
            break
        moving = False
        new_step_map = np.copy(step_map)
        for y, line in enumerate(height_map):
            for x, height in enumerate(line):
                if step_map[y][x] != -1:
                    continue
                possible_steps = []
                if y - 1 >= 0:
                    step = step_map[y - 1][x]
                    if step != -1:
                        if np.abs(height - height_map[y - 1][x]) <= 1 or height_map[y][x] < height_map[y - 1][x]:
                            possible_steps.append(step)
                if y + 1 < height_map.shape[0]:
                    step = step_map[y + 1][x]
                    if step != -1:
                        if np.abs(height - height_map[y + 1][x]) <= 1 or height_map[y][x] < height_map[y + 1][x]:
                            possible_steps.append(step)
                if x - 1 >= 0:
                    step = step_map[y][x - 1]
                    if step != -1:
                        if np.abs(height - height_map[y][x - 1]) <= 1 or height_map[y][x] < height_map[y][x - 1]:
                            possible_steps.append(step)
                if x + 1 < height_map.shape[1]:
                    step = step_map[y][x + 1]
                    if step != -1:
                        if np.abs(height - height_map[y][x + 1]) <= 1 or height_map[y][x] < height_map[y][x + 1]:
                            possible_steps.append(step)
                if len(possible_steps) == 0:
                    continue
                smallest_step = np.min(np.array(possible_steps))
                new_step_map[y][x] = smallest_step + 1
                moving = True
        step_map = new_step_map
        if moving == False:
            return 1000

    if step_map[end_loc[0], end_loc[1]] == -1:
        return 1000
    else:
        return step_map[end_loc[0], end_loc[1]] 

total_steps = []

for y, line in enumerate(height_map):
    for x, height in enumerate(line):
        if height == 0:
            steps = get_steps_for_loc(x, y)
            print(steps)
            total_steps.append(steps)

print(np.min(total_steps))

