#!/usr/bin/python3

import numpy as np
import sympy

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
                elif self.operation == "=":
                    self.number = 1 if num1 == num2 else 0
                self.set = True
        return self.set


monkeys = []

for line in lines:
    name = line[0].split(":")[0]
    try:
        num = int(line[1])
        monkey = Monkey(name, num=num)
        monkeys.append(monkey)
    except:
        other_name1 = line[1]
        other_name2 = line[3]
        operation = line[2]
        monkey = Monkey(name, other_name1=other_name1, other_name2=other_name2, operation=operation)
        monkeys.append(monkey)

for monkey in monkeys:
    if monkey.name == "root":
        monkey.operation = "="
    elif monkey.name == "humn":
        monkey.set = False
        monkey.name1 = "humn"
        monkey.name2 = "humn"
        monkey.operation = "="

true_monkeys = np.sum([monkey.update(monkeys) for monkey in monkeys])
old_true_monkeys = -1

while true_monkeys != old_true_monkeys:
    old_true_monkeys = true_monkeys
    true_monkeys = np.sum([monkey.update(monkeys) for monkey in monkeys])

monkey_dict = {}

for monkey in monkeys:
    monkey_dict[monkey.name] = monkey

if monkey_dict[monkey_dict["root"].name1].set:
    eval_monkey = monkey_dict["root"].name2
    equals = monkey_dict[monkey_dict["root"].name1].number
else:
    eval_monkey = monkey_dict["root"].name1
    equals = monkey_dict[monkey_dict["root"].name2].number

def generate_eval(monkey_dict, eval_monkey):
    monkey = monkey_dict[eval_monkey]
    if monkey.name == "humn":
        return "x"
    else:
        if monkey.set:
            return str(monkey.number)
        else:
            return "( |" + monkey.name1 + "| " + monkey.operation + " |" + \
                   monkey.name2 + "| )"

eval_string = generate_eval(monkey_dict, eval_monkey)
for _ in range(1000):
    split_string = eval_string.split('|')
    for j, string in enumerate(split_string):
        if len(string) == 4:
            if not string.__contains__(" "):
                split_string[j] = generate_eval(monkey_dict, string)
    eval_string = "".join(split_string)

print(eval_string)
print(equals)

expr = sympy.sympify(eval_string)

print(expr)

print(sympy.solve(sympy.Eq(expr, equals)))


