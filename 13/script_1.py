#!/usr/bin/python3

import numpy as np

KEEP_GOING, RIGHT_ORDER, WRONG_ORDER, ERROR = range(4)

f = open("data.dat", "r")

lines = [line.strip() for line in f.readlines()]

lefts = []
rights = []

i = 0
while i < len(lines):
    lefts.append(eval(lines[i]))
    i += 1
    rights.append(eval(lines[i]))
    i += 2

num_pairs = len(lefts)

print(lefts)
print(rights)

def compare_ints(left, right):
    if left < right:
        return RIGHT_ORDER
    elif left == right:
        return KEEP_GOING
    else:
        return WRONG_ORDER

def compare_lists(left, right, level=1):

    print(" " + "-"*level + " comparing lists ", left, right)

    size = max(len(left), len(right))

    for i in range(size):
        if i == len(left):
            print(" " + "-"*level + " left ran out, right order")
            return RIGHT_ORDER
        if i == len(right):
            print(" " + "-"*level + " right ran out, wrong order")
            return WRONG_ORDER
        left_item = left[i]
        right_item = right[i]
        print(" " + "-"*level + " comparing items ", left_item, right_item)
        result = compare_items(left_item, right_item, level)
        if result == RIGHT_ORDER:
            print(" " + "-"*level + " comparing items, right order recieved")
            return RIGHT_ORDER
        elif result == WRONG_ORDER:
            print(" " + "-"*level + " comparing items, wrong order recieved")
            return WRONG_ORDER
        elif result == KEEP_GOING:
            print(" " + "-"*level + " comparing items, keep going recieved")
            continue
        elif result == ERROR:
            print("!!! oh fuck error !!!")
            continue

    return KEEP_GOING

def compare_items(left_item, right_item, level):

        if type(left_item) is int and type(right_item) is int:
            return compare_ints(left_item, right_item)
        elif type(left_item) is list and type(right_item) is list:
            return compare_lists(left_item, right_item, level+1)
        elif type(left_item) is int and type(right_item) is list:
            return compare_lists([left_item], right_item, level+1)
        elif type(left_item) is list and type(right_item) is int:
            return compare_lists(left_item, [right_item], level+1)

        return ERROR

score = 0
for i in range(num_pairs):
    print("top level compare ", lefts[i], rights[i])
    if compare_lists(lefts[i], rights[i], level=1) == RIGHT_ORDER:
        score += i + 1
        print(i + 1)

print(score)


