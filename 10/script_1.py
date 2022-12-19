#!/usr/bin/python3

import numpy as np

cycle = 0
instruction = 0
register = 1

f = open("data.dat", "r")

commands = f.readlines()

save_signal_strength = []

times = np.array([20, 60, 100, 140, 180, 220])

def check_signal():
    if np.any(cycle == times):
        save_signal_strength.append(register * cycle) 

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
        
        
while cycle < np.max(times):
    cycle += 1
    check_signal()

print(np.sum(save_signal_strength))
