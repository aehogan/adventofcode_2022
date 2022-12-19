#!/usr/bin/python3

rucksacks = []

f = open("data.dat", "r")

def Priority(letter):
    prio = ord(letter) - 96
    if prio < 0:
        prio += 58
    return prio

total_prio = 0

group_members = 0

for line in f.readlines():
    line = line[:-1]
    inv_size = len(line)
    half = int(inv_size/2)
    rucksack = line
    rucksacks.append(rucksack)
    group_members += 1
    if group_members == 3:
        print(rucksacks)
        for letter in rucksacks[0]:
            if letter in rucksacks[1] and letter in rucksacks[2]:
                total_prio += Priority(letter)
                break
        rucksacks = []
        group_members = 0

print(total_prio)
