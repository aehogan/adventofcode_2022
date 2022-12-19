#!/usr/bin/python3

rucksacks = []

f = open("data.dat", "r")

def Priority(letter):
    prio = ord(letter) - 96
    if prio < 0:
        prio += 58
    return prio

total_prio = 0

for line in f.readlines():
    line = line[:-1]
    inv_size = len(line)
    half = int(inv_size/2)
    rucksack = line
    side_a = line[:half]
    side_b = line[half:]
    in_common = []
    for letter in side_a:
        if letter in side_b:
            in_common.append(letter)
            total_prio += Priority(letter)
            break
    print(inv_size, half, side_a, side_b, in_common, rucksack)

print(total_prio)
