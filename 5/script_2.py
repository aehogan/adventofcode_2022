#!/usr/bin/python3

import numpy as np

#[V]         [T]         [J]        
#[Q]         [M] [P]     [Q]     [J]
#[W] [B]     [N] [Q]     [C]     [T]
#[M] [C]     [F] [N]     [G] [W] [G]
#[B] [W] [J] [H] [L]     [R] [B] [C]
#[N] [R] [R] [W] [W] [W] [D] [N] [F]
#[Z] [Z] [Q] [S] [F] [P] [B] [Q] [L]
#[C] [H] [F] [Z] [G] [L] [V] [Z] [H]
# 1   2   3   4   5   6   7   8   9 

stacks = []
stack = ['C', 'Z', 'N', 'B', 'M', 'W', 'Q', 'V']
stacks.append(stack)
stack = ['H', 'Z', 'R', 'W', 'C', 'B']
stacks.append(stack)
stack = ['F', 'Q', 'R', 'J']
stacks.append(stack)
stack = ['Z', 'S', 'W', 'H', 'F', 'N', 'M', 'T']
stacks.append(stack)
stack = ['G', 'F', 'W', 'L', 'N', 'Q', 'P']
stacks.append(stack)
stack = ['L', 'P', 'W']
stacks.append(stack)
stack = ['V', 'B', 'D', 'R', 'G', 'C', 'Q', 'J']
stacks.append(stack)
stack = ['Z', 'Q', 'N', 'B', 'W']
stacks.append(stack)
stack = ['H', 'L', 'F', 'C', 'G', 'T', 'J']
stacks.append(stack)

print(stacks)

f = open("data.dat", "r")

for line in f.readlines():
    split_line = line.split()
    number = int(split_line[1])
    stack_a = int(split_line[3]) - 1
    stack_b = int(split_line[5]) - 1
    boxes = []
    for i in range(number):
        boxes.append(stacks[stack_a].pop())
    for i in range(number):
        stacks[stack_b].append(boxes[len(boxes)-i-1])
    print(number, stack_a, stack_b)
    print(stacks)

for stack in stacks:
    print(stack[-1])
