#!/usr/bin/python3

import numpy as np
from collections import Counter

class Elf:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.directions = [self.consider_north, self.consider_south, self.consider_west, self.consider_east]
        self.proposed_direction = self.x, self.y

    def move_direction(self, elves, counter):
        reference = elves.pop((self.x, self.y))
        if counter[self.proposed_direction] == 1:
            self.x, self.y = self.proposed_direction
        elves[(self.x, self.y)] = reference

    def propose_direction(self, elves):
        #print("x y", self.x, self.y)
        proposed_direction = self.x, self.y
        if self.elf_nearby(elves):
            for i, direction in enumerate(self.directions):
                #print(direction.__name__)
                if direction(elves):
                    #print("ok going " + direction.__name__.split('_')[1])
                    proposed_direction = direction
                    break
        x = self.directions.pop(0)
        self.directions.append(x)

        if proposed_direction == self.consider_north:
            self.proposed_direction = self.x, self.y - 1
        elif proposed_direction == self.consider_south:
            self.proposed_direction = self.x, self.y + 1
        elif proposed_direction == self.consider_west:
            self.proposed_direction = self.x - 1, self.y
        elif proposed_direction == self.consider_east:
            self.proposed_direction = self.x + 1, self.y
        return self.proposed_direction

    def elf_nearby(self, elves):
        if (self.x+1, self.y+1) in elves or \
                (self.x+1, self.y) in elves or \
                (self.x+1, self.y-1) in elves or \
                (self.x, self.y+1) in elves or \
                (self.x, self.y-1) in elves or \
                (self.x-1, self.y+1) in elves or \
                (self.x-1, self.y) in elves or \
                (self.x-1, self.y-1) in elves:
            return True
        return False

    def consider_north(self, elves):
        if (self.x-1, self.y-1) not in elves and \
                (self.x, self.y-1) not in elves and \
                (self.x+1, self.y-1) not in elves:
            return True
        return False

    def consider_south(self, elves):
        if (self.x-1, self.y+1) not in elves and \
                (self.x, self.y+1) not in elves and \
                (self.x+1, self.y+1) not in elves:
            return True
        return False

    def consider_west(self, elves):
        if (self.x-1, self.y+1) not in elves and \
                (self.x-1, self.y) not in elves and \
                (self.x-1, self.y-1) not in elves:
            return True
        return False

    def consider_east(self, elves):
        if (self.x+1, self.y+1) not in elves and \
                (self.x+1, self.y) not in elves and \
                (self.x+1, self.y-1) not in elves:
            return True
        return False

def print_map():
    coords = np.array([coord for coord in elves], dtype=int)
    x_lo = np.min(coords[:, 0])
    x_hi = np.max(coords[:, 0])
    y_lo = np.min(coords[:, 1])
    y_hi = np.max(coords[:, 1])
    counter = Counter([(coord[0], coord[1]) for coord in coords])
    sum = 0
    for y in np.arange(y_lo, y_hi+1, 1):
        for x in np.arange(x_lo, x_hi+1, 1):
            if counter[(x, y)] == 1:
                print("#", end='')
            else:
                sum += 1
                print(".", end='')
        print()
    return x_lo, x_hi, y_lo, y_hi, sum


lines = [line.strip() for line in open("data.dat", "r").readlines()]
elves = {}

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "#":
            elf = Elf(x, y)
            elves[(x, y)] = elf

print(print_map())
for _ in range(10):
    proposed_directions = [elf.propose_direction(elves) for coords, elf in elves.items()]
    counter = Counter(proposed_directions)
    elves_list = [elf for elf in elves.values()]
    [elf.move_direction(elves, counter) for elf in elves_list]
    print(print_map())

# 6006, 6084 too high
# 3798, 5928 not right
# 3641 too low

