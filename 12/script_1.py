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
step_map = np.zeros_like(height_map) - 1
step_map[start_loc[0], start_loc[1]] = 0

print_chars = ["□", "▤", "▥", "▧", "▨", "▦", "▩", "■"]
colors = ["white", "cyan", "magenta", "blue", "yellow", "green", "red"]

steps = 400
for i in range(steps):
    if step_map[end_loc[0], end_loc[1]] != -1:
        #break
        pass
    new_step_map = np.copy(step_map)
    for y, line in enumerate(height_map):
        for x, height in enumerate(line):
            if x == 46 and y == 20:
                #debug = True
                debug = False
            else:
                debug = False
            if debug:
                print("x ", x, "y ", y, "h ", height_map[y][x], "s ", step_map[y][x])
            if step_map[y][x] != -1:
                continue
            possible_steps = []
            if y - 1 >= 0:
                step = step_map[y - 1][x]
                if step != -1:
                    if np.abs(height - height_map[y - 1][x]) <= 1 or height_map[y][x] < height_map[y - 1][x]:
                        if debug:
                            print("a ", height, height_map[y - 1][x])
                        possible_steps.append(step)
            if y + 1 < height_map.shape[0]:
                step = step_map[y + 1][x]
                if step != -1:
                    if np.abs(height - height_map[y + 1][x]) <= 1 or height_map[y][x] < height_map[y + 1][x]:
                        if debug:
                            print("b ", height, height_map[y - 1][x])
                        possible_steps.append(step)
            if x - 1 >= 0:
                step = step_map[y][x - 1]
                if step != -1:
                    if np.abs(height - height_map[y][x - 1]) <= 1 or height_map[y][x] < height_map[y][x - 1]:
                        if debug:
                            print("c ", height, height_map[y - 1][x])
                        possible_steps.append(step)
            if x + 1 < height_map.shape[1]:
                step = step_map[y][x + 1]
                if step != -1:
                    if np.abs(height - height_map[y][x + 1]) <= 1 or height_map[y][x] < height_map[y][x + 1]:
                        if debug:
                            print("d ", height, height_map[y - 1][x])
                        possible_steps.append(step)
            if len(possible_steps) == 0:
                continue
            smallest_step = np.min(np.array(possible_steps))
            new_step_map[y][x] = smallest_step + 1
            if debug:
                print("x ", x, "y ", y, "h ", height_map[y][x], "s ", new_step_map[y][x])
                print("steps ", possible_steps)
                print("step + 1 ", smallest_step + 1)
    step_map = new_step_map
    print("step: {0}".format(i))
    for y, line in enumerate(step_map):
        for x, step in enumerate(line):
            if x == start_loc[1] and y == start_loc[0]:
                termcolor.cprint("S", "green", end="")
            elif x == end_loc[1] and y == end_loc[0]:
                color = colors[ int( height_map[y][x] % len(colors) ) ]
                termcolor.cprint("E", color, end="")
            elif step == -1:
                color = colors[ int( height_map[y][x] % len(colors) ) ]
                termcolor.cprint(".", color, end="")
            else:
                char = print_chars[step % len(print_chars)]
                #color = colors[int( (step / len(print_chars)) % len(colors) )]
                color = colors[ int( height_map[y][x] % len(colors) ) ]
                termcolor.cprint(char, color, end="")
                #print(char, end="")
        print("")
    os.system('sleep 0.1')
    if i != steps - 1:
        print("\033c", end="")


print(height_map.shape)

#print(height_map)
#print(step_map)
#print("start", start_loc)
#print("end", end_loc)
print(step_map[end_loc[0], end_loc[1]])
