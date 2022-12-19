#!/usr/bin/python3

import numpy as np
import termcolor
from termcolor import cprint
import time

Map = np.zeros((500, 1000), dtype=int)

AIR, ROCK, SETTLED_SAND, SAND_SOURCE, FALLING_SAND = range(5)

f = open("data.dat", "r")

lines = [line.strip() for line in f.readlines()]

def print_map(x_lo, x_hi, y_lo, y_hi):
    print("\033c", end="")
    #print("--------------------------------")
    for y in range(y_lo, y_hi + 1):
        for x in range(x_lo, x_hi + 1):
            char = Map[y][x]
            if char == AIR:
                cprint(".", "blue", end="")
            elif char == ROCK:
                cprint("#", "white", end="")
            elif char == SETTLED_SAND:
                cprint("o", "yellow", end="")
            elif char == SAND_SOURCE:
                cprint("+", "cyan", end="")
            elif char == FALLING_SAND:
                cprint("~", "yellow", end="")
        print("")

def update_falling_sand():
    global falling_coords
    x = falling_coords[0]
    y = falling_coords[1]
    if Map[y + 1][x] == AIR:
        falling_coords[1] = y + 1
        Map[y][x] = AIR
        Map[y + 1][x] = FALLING_SAND
        return True
    elif Map[y + 1][x - 1] == AIR:
        falling_coords[1] = y + 1
        falling_coords[0] = x - 1
        Map[y][x] = AIR
        Map[y + 1][x - 1] = FALLING_SAND
        return True
    elif Map[y + 1][x + 1] == AIR:
        falling_coords[1] = y + 1
        falling_coords[0] = x + 1
        Map[y][x] = AIR
        Map[y + 1][x + 1] = FALLING_SAND
        return True
    return False

for line in lines:
    split = line.split(" -> ")
    coords = [[int(coord) for coord in pair.split(",")] for pair in split]
    print(coords)
    num_lines_to_draw = len(coords) - 1
    for num_line in range(num_lines_to_draw):
        left = coords[num_line]
        right = coords[num_line + 1]
        print(left, "->", right)
        while left[0] != right[0] or left[1] != right[1]:
            Map[left[1], left[0]] = ROCK
            print(left, right)
            if left[0] < right[0]:
                left[0] += 1
            elif left[0] > right[0]:
                left[0] -= 1
            if left[1] < right[1]:
                left[1] += 1
            elif left[1] > right[1]:
                left[1] -= 1
        Map[right[1], right[0]] = ROCK

Map[0][500] = SAND_SOURCE

draw_map = False

if draw_map:
    print_map(400, 600, 0, 50)
    time.sleep(0.1)

falling_coords = np.zeros(2, dtype=int)

while True:
    if Map[1][500] != AIR:
        break
    Map[1][500] = FALLING_SAND
    falling_coords[0] = 500
    falling_coords[1] = 1
    if draw_map:
        print_map(400, 600, 0, 50)
        time.sleep(0.1)
    while update_falling_sand():
        if draw_map:
            print_map(400, 600, 0, 50)
            time.sleep(0.1)
        if falling_coords[1] >= 300:
            break
    if falling_coords[1] >= 300:
        break
    Map[falling_coords[1]][falling_coords[0]] = SETTLED_SAND

print_map(400, 600, 0, 300)

count = 0
for y in range(len(Map)):
    for x in range(len(Map[0])):
        if Map[y][x] == SETTLED_SAND:
            count += 1
print(count)



