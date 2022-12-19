#!/usr/bin/python3

import numpy as np

cycle = 0
instruction = 0
register = 1

f = open("data.dat", "r")

commands = f.readlines()

image = []
current_line = []

def check_signal():
    global current_line
    cursor = cycle % 40 - 1
    if np.abs(cursor - register) < 2:
        current_line.append("#")
    else:
        current_line.append(".")
    if len(current_line) == 40:
        image.append(current_line)
        current_line = []

while instruction < len(commands):
    line = commands[instruction].split()
    command = line[0]
    
    print(command, cycle, instruction, register)
    if command == "noop":
        cycle += 1
        instruction += 1
        check_signal()
    elif command == "addx":
        cycle += 1
        check_signal()
        cycle += 1
        check_signal()
        instruction += 1
        register += int(line[1])
        
        
while cycle < 6*40:
    cycle += 1
    check_signal()

for line in image:
    for char in line:
        print(char, end="")
    print("")
        

