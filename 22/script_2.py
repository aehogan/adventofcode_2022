#!/usr/bin/python3

import numpy as np

WRAP, OPEN, WALL = range(3)
translate = {" ": WRAP, ".": OPEN, "#": WALL}
RIGHT, DOWN, LEFT, UP = range(4)
dir_to_str = {RIGHT: "right", DOWN: "down", LEFT: "left", UP: "up"}

f = open("data.dat", "r")

lines = [line.replace("\n", "") for line in f.readlines()]

read_map = True
game_map = []

for line in lines:
    if read_map:
        game_map.append([translate[char] for char in line])
    else:
        directions = line
    if line == "":
        read_map = False

max_length = np.max([len(line) for line in game_map])

for line in game_map:
    while len(line) < max_length:
        line.append(WRAP)

game_map = np.array(game_map, dtype=int)

temp_directions = []
temp_number = []
for char in directions:
    if char.isnumeric():
        temp_number.append(char)
    else:
        if len(temp_number) != 0:
            temp_directions.append(int("".join(temp_number)))
            temp_number = []
        temp_directions.append(char)

if len(temp_number) != 0:
    temp_directions.append(int("".join(temp_number)))

directions = temp_directions

y = 0
x = np.min([i for i, tile in enumerate(game_map[y]) if tile == OPEN])

current_direction = RIGHT

print(game_map)
print(game_map.shape)
print(directions)
print(x, y)
print(" --- ")

for direction in directions:
    print(direction)
    if direction == "R":
        current_direction = (current_direction + 1) % 4
    elif direction == "L":
        current_direction = (current_direction - 1) % 4
    else:
        for _ in range(direction):
            new_x, new_y = x, y
            if current_direction == RIGHT:
                while True:
                    new_x += 1
                    if new_x >= game_map.shape[1]:
                        new_x = 0
                    if game_map[new_y][new_x] != WRAP:
                        break
            elif current_direction == DOWN:
                while True:
                    new_y += 1
                    if new_y >= game_map.shape[0]:
                        new_y = 0
                    if game_map[new_y][new_x] != WRAP:
                        break
            elif current_direction == LEFT:
                while True:
                    new_x -= 1
                    if new_x < 0:
                        new_x = game_map.shape[1] - 1
                    if game_map[new_y][new_x] != WRAP:
                        break
            elif current_direction == UP:
                while True:
                    new_y -= 1
                    if new_y < 0:
                        new_y = game_map.shape[0] - 1
                    if game_map[new_y][new_x] != WRAP:
                        break
            print("x", x, "y", y, "new_x", new_x, "new_y", new_y, direction, game_map[new_y][new_x] != WALL, dir_to_str[current_direction])
            if game_map[new_y][new_x] != WALL:
                x, y = new_x, new_y

print(1000*(y+1) + 4*(x+1) + current_direction)


