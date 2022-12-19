#!/usr/bin/python3

import numpy as np

class Monkey:
    def __init__(self, starting_items, operation, test, if_true, if_false):

        self.items = starting_items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.counter = 0

    def update(self, monkeys):

        true_list = []
        false_list = []

        for old_worry in self.items:
            self.counter += 1
            if self.operation[0] == "old":
                new_worry = old_worry
            else:
                new_worry = int(self.operation[0])

            if self.operation[2] == "old":
                operand = old_worry
            else:
                operand = int(self.operation[2])

            if self.operation[1] == "+":
                new_worry = new_worry + operand
            elif self.operation[1] == "*":
                new_worry = new_worry * operand

            new_worry = int(new_worry / 3)

            test = new_worry % self.test == 0

            if test == True:
                true_list.append(new_worry)
            else:
                false_list.append(new_worry)

        self.items = []

        for item in true_list:
            monkeys[self.if_true].items.append(item)

        for item in false_list:
            monkeys[self.if_false].items.append(item)

f = open("data.dat", "r")

lines = [line.strip() for line in f.readlines()]

monkeys = []

starting_items = None
operation = None
test = None
if_true = None
if_false = None

for line in lines:

    split = line.split()

    if line == "":
        if starting_items is None:
            continue
        print("make da monkey")
        monkey = Monkey(starting_items, operation, test, if_true, if_false)
        monkeys.append(monkey)
        starting_items = None
        operation = None
        test = None
        if_true = None
        if_false = None

    elif split[0] == "Monkey":
        pass

    elif split[0] == "Starting":
        starting_items = []
        for i in range(2, len(split)):
            starting_items.append(int(split[i].split(",")[0]))
        print("starting", starting_items)

    elif split[0] == "Operation:":
        operation = split[-3:]
        print("operation", operation)

    elif split[0] == "Test:":
        test = int(split[3])
        print("test", test)

    elif split[0] == "If" and split[1] == "true:":
        if_true = int(split[5])
        print("if true", if_true)

    elif split[0] == "If" and split[1] == "false:":
        if_false = int(split[5])
        print("if false", if_false)

for round in range(20):
    for monkey in monkeys:
        monkey.update(monkeys)

counter = []

for monkey in monkeys:
    print(monkey.items)
    print(monkey.counter)
    counter.append(monkey.counter)

counter = np.array(counter)
counter.sort()
print(counter[-1] * counter[-2])



