#!/usr/bin/python3

import numpy as np

f = open("data.dat", "r")

lines = [line.strip().split() for line in f.readlines()]

class Monkey():
    def __init__(self, name, num=None, other_name1=None, other_name2=None, operation=None):
        self.name = name
        if num is not None:
            self.number = num
            self.set = True
        else:
            self.set = False
            self.name1 = other_name1
            self.name2 = other_name2
            self.operation = operation

    def update(self, monkeys):
        if self.set == False:
            num1 = None
            num2 = None
            for monkey in monkeys:
                if monkey.set:
                    if monkey.name == self.name1:
                        num1 = monkey.number
                    elif monkey.name == self.name2:
                        num2 = monkey.number
            if num1 is not None and num2 is not None:
                if self.operation == "+":
                    self.number = num1 + num2
                elif self.operation == "-":
                    self.number = num1 - num2
                elif self.operation == "*":
                    self.number = num1 * num2
                elif self.operation == "/":
                    self.number = num1 / num2
                self.set = True
        return self.set

monkeys = []

for line in lines:
    name = line[0].split(":")[0]
    try:
        num = int(line[1])
        monkey = Monkey(name, num=num)
        monkeys.append(monkey)
        #print(name, num, monkey.set)
    except:
        other_name1 = line[1]
        other_name2 = line[3]
        operation = line[2]
        monkey = Monkey(name, other_name1=other_name1, other_name2=other_name2, operation=operation)
        monkeys.append(monkey)
        #print(name, other_name1, other_name2, operation, monkey.set)


while not np.all([monkey.update(monkeys) for monkey in monkeys]):
    pass

for monkey in monkeys:
    if monkey.name == "root":
        print(monkey.name, monkey.number)

