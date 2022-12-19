#!/usr/bin/python3

import numpy as np
import termcolor
from termcolor import cprint
import time

#AIR, FALLING_ROCK, SIDE_WALL, CORNER_WALL, BOTTOM_WALL, SOLID_ROCK = range(6)

AIR = 0b0
FALLING_ROCK = 0b1
SIDE_WALL = 0b11
CORNER_WALL = 0b101
BOTTOM_WALL = 0b111
SOLID_ROCK = 0b1001
MASK = 0b1111110

def print_map(x_lo, x_hi, y_lo, y_hi):
    #print("\033c", end="")
    print("--------------------------------")
    for y in range(y_lo, y_hi + 1):
        for x in range(x_lo, x_hi + 1):
            char = Map[y][x]
            if char == AIR:
                cprint(".", "blue", end="")
            elif char == SIDE_WALL:
                cprint("|", "white", end="")
            elif char == BOTTOM_WALL:
                cprint("-", "white", end="")
            elif char == CORNER_WALL:
                cprint("+", "white", end="")
            elif char == SOLID_ROCK:
                cprint("#", "cyan", end="")
            elif char == FALLING_ROCK:
                cprint("@", "yellow", end="")
        print("")
    #time.sleep(0.1)
        
map_depth = 2000
draw_depth = 75
width = 9

Map = np.zeros((map_depth + 1, width), dtype=int)

Map[:, :] = AIR
Map[-1, :] = BOTTOM_WALL
Map[:, 0] = SIDE_WALL
Map[:, 8] = SIDE_WALL
Map[-1, -1] = CORNER_WALL
Map[-1, 0] = CORNER_WALL

f = open("data.dat", "r")

line = f.readlines()[0].strip()
wind = np.zeros(len(line), dtype=int)
for idx, char in enumerate(line):
    if char == "<":
        wind[idx] = -1
    elif char == ">":
        wind[idx] = 1

horizontal_shape = np.ones((1, 4), dtype=int) * FALLING_ROCK

cross_shape = np.ones((3, 3), dtype=int) * FALLING_ROCK
cross_shape[0, 0] = AIR
cross_shape[-1, 0] = AIR
cross_shape[0, -1] = AIR
cross_shape[-1, -1] = AIR

l_shape = np.ones((3, 3), dtype=int) * FALLING_ROCK
l_shape[0:2, 0:2] = AIR

vertical_shape = np.ones((4, 1), dtype=int) * FALLING_ROCK

block_shape = np.ones((2, 2), dtype=int) * FALLING_ROCK

shapes = [horizontal_shape, cross_shape, l_shape, vertical_shape, block_shape]

last_y_start = map_depth

def spawn_rock(Map, rock_counter, shape):
    global last_y_start
    break_me = False
    for y in np.arange(last_y_start, 0, -1):
        if np.max(Map[y, 1:8]) == AIR:
            y_start = y
            break_me = True
            break
        if break_me:
            break
    last_y_start = y_start
    rock_pos = np.array([y_start - 2 - shape.shape[0], 3])
    
    for y in range(shape.shape[0]):
        for x in range(shape.shape[1]):
            Map[rock_pos[0] + y, rock_pos[1] + x] = shape[y, x]
    
    return rock_pos
    
def test_rock_movement(Map, rock_pos, shape):
    can_move = True
    #can_move = np.all( ( ( shape * MASK ) & Map[rock_pos[0]:rock_pos[0] + shape.shape[0], rock_pos[1]:rock_pos[1] + shape.shape[1]] ) <= FALLING_ROCK )
    for y in range(shape.shape[0]):
        for x in range(shape.shape[1]):
            if shape[y, x] != AIR:
                if Map[rock_pos[0] + y, rock_pos[1] + x] > FALLING_ROCK:
                    can_move = False
    return can_move

def move_rock(Map, rock_pos, new_rock_pos, shape):
    for y in range(shape.shape[0]):
        for x in range(shape.shape[1]):
            if shape[y, x] != AIR:
                 Map[rock_pos[0] + y, rock_pos[1] + x] = AIR
                 
    for y in range(shape.shape[0]):
        for x in range(shape.shape[1]):
            if shape[y, x] != AIR:
                 Map[new_rock_pos[0] + y, new_rock_pos[1] + x] = FALLING_ROCK
                 
def convert_to_solid_rock(Map, rock_pos, shape):
    for y in range(shape.shape[0]):
        for x in range(shape.shape[1]):
            if shape[y, x] != AIR:
                 Map[rock_pos[0] + y, rock_pos[1] + x] = SOLID_ROCK
    
def rock_clock(Map, rock_pos, shape, wind):
    test_wind_pos = np.copy(rock_pos)
    test_wind_pos[1] += wind
    
    if test_rock_movement(Map, test_wind_pos, shape) == True:
        move_rock(Map, rock_pos, test_wind_pos, shape)
        rock_pos = test_wind_pos
    
    test_falling = np.copy(rock_pos)
    test_falling[0] += 1
    
    if test_rock_movement(Map, test_falling, shape) == True:
        move_rock(Map, rock_pos, test_falling, shape)
        rock_pos = test_falling
        return False, rock_pos
    else:
        return True, rock_pos

total_chopped = 0

def chop_length_off_map():
    global last_y_start, Map, total_chopped
    length = 100
    total_chopped += length
    last_y_start += length
    Map = np.roll(Map, length, axis=0)
    Map[0:length, 1:8] = AIR
    
def get_total_rock_depth():
    tmp = -1
    for y in range(map_depth + 1):
        for x in range(1, width-1):
            ele = Map[y, x]
            if ele == BOTTOM_WALL or ele == SOLID_ROCK:
                tmp = y
                break
        if tmp != -1:
            break
    return map_depth - tmp + total_chopped

#print(shapes)
#print(wind)
#print_map(0, 8, map_depth - 10, map_depth)

print_freq = len(wind)

wind_counter = 0
for rock_counter in range(20182 + 295893):
    shape = shapes[rock_counter % len(shapes)]
    rock_pos = spawn_rock(Map, rock_counter, shape)
    #print_map(0, 8, map_depth - draw_depth, map_depth)
    rock_settled = False
    while rock_settled == False:
        rock_settled, rock_pos = rock_clock(Map, rock_pos, shape, wind[wind_counter])
        wind_counter = ( wind_counter + 1 ) % len(wind)
        #print_map(0, 8, map_depth - draw_depth, map_depth)
    convert_to_solid_rock(Map, rock_pos, shape)
    if last_y_start < map_depth - 1700:
        chop_length_off_map()
    #print_map(0, 8, map_depth - draw_depth, map_depth)
    if rock_counter % print_freq == 0:
        print(rock_counter, get_total_rock_depth(), flush=True)

print(rock_counter, get_total_rock_depth())
#print_map(0, 8, map_depth - draw_depth, map_depth)






