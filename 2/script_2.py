#!/usr/bin/python3

import numpy as np

# 1 = rock = A, X
# 2 = paper = B, Y
# 3 = scissors = C, Z

def Winner(choice_a, choice_b):
    if choice_a == choice_b:
        return 0 # draw
    elif choice_a == 1 and choice_b == 2:
        return 2
    elif choice_a == 1 and choice_b == 3:
        return 1
    elif choice_a == 2 and choice_b == 1:
        return 1
    elif choice_a == 2 and choice_b == 3:
        return 2
    elif choice_a == 3 and choice_b == 1:
        return 2
    elif choice_a == 3 and choice_b == 2:
        return 1
    return -1

def score(both_choices):
    choice_a = both_choices[0]
    choice_b = both_choices[1]
    winner = Winner(choice_a, choice_b)
    score = choice_b
    if winner == 0:
        score += 3
    elif winner == 2:
        score += 6
    return score

choices = []

f = open("data.dat", "r")

for line in f.readlines():
    split_line = line.split()
    split_line[0] = split_line[0].replace("A", "1")
    split_line[0] = split_line[0].replace("B", "2")
    split_line[0] = split_line[0].replace("C", "3")
    split_line[1] = split_line[1].replace("X", "1")
    split_line[1] = split_line[1].replace("Y", "2")
    split_line[1] = split_line[1].replace("Z", "3")
    split_line[0] = int(split_line[0])
    split_line[1] = int(split_line[1])
    if split_line[1] == 2: # draw
        split_line[1] = split_line[0]
    elif split_line[1] == 1: # lose
        if split_line[0] == 1:
            split_line[1] = 3
        elif split_line[0] == 2:
            split_line[1] = 1
        elif split_line[0] == 3:
            split_line[1] = 2
    elif split_line[1] == 3: # win
        if split_line[0] == 1:
            split_line[1] = 2
        elif split_line[0] == 2:
            split_line[1] = 3
        elif split_line[0] == 3:
            split_line[1] = 1
    choices.append(split_line)

choices = np.array(choices)

total_score = 0
for choice in choices:
    total_score += score(choice)

print(total_score)

