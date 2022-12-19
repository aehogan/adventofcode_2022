#!/usr/bin/python3

import numpy as np

KEEP_GOING, RIGHT_ORDER, WRONG_ORDER, ERROR = range(4)

f = open("data.dat", "r")

lines = [line.strip() for line in f.readlines()]

all_lists = []

i = 0
while i < len(lines):
    all_lists.append(eval(lines[i]))
    i += 1
    all_lists.append(eval(lines[i]))
    i += 2

all_lists.append([[2]])
all_lists.append([[6]])

#print(all_lists)

def compare_ints(left, right):
    if left < right:
        return RIGHT_ORDER
    elif left == right:
        return KEEP_GOING
    else:
        return WRONG_ORDER

def compare_lists(left, right, level=1):

    #print(" " + "-"*level + " comparing lists ", left, right)

    size = max(len(left), len(right))

    for i in range(size):
        if i == len(left):
            #print(" " + "-"*level + " left ran out, right order")
            return RIGHT_ORDER
        if i == len(right):
            #print(" " + "-"*level + " right ran out, wrong order")
            return WRONG_ORDER
        left_item = left[i]
        right_item = right[i]
        #print(" " + "-"*level + " comparing items ", left_item, right_item)
        result = compare_items(left_item, right_item, level)
        if result == RIGHT_ORDER:
            #print(" " + "-"*level + " comparing items, right order recieved")
            return RIGHT_ORDER
        elif result == WRONG_ORDER:
            #print(" " + "-"*level + " comparing items, wrong order recieved")
            return WRONG_ORDER
        elif result == KEEP_GOING:
            #print(" " + "-"*level + " comparing items, keep going recieved")
            continue
        elif result == ERROR:
            #print("!!! oh fuck error !!!")
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

def swap_positions(pos1, pos2):
    all_lists[pos1], all_lists[pos2] = all_lists[pos2], all_lists[pos1]

all_ordered = False
while all_ordered == False:
    all_ordered = True
    for i in range(len(all_lists)-1):
        #print("top level compare ", all_lists[i], all_lists[i+1])
        if compare_lists(all_lists[i], all_lists[i+1], level=1) == WRONG_ORDER:
            all_ordered = False
            swap_positions(i, i+1)

print(all_lists)

decoder_key = 1

for i, item in enumerate(all_lists):
    if item == [[2]]:
        decoder_key *= (i+1)
    if item == [[6]]:
        decoder_key *= (i+1)

print(decoder_key)

