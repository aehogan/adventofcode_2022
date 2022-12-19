#!/usr/bin/python3

import numpy as np

f = open("data.dat", "r")

lines = [line.strip() for line in f.readlines()]

class Sensor():
    def __init__(self, x1, y1, x2, y2):
        self.x = np.array([x1, y1], dtype=int)
        self.beacon_x = np.array([x2, y2], dtype=int)
        self.dist = self.manhattan_dist(self.x, self.beacon_x)
        #print("sensor init", self.x, self.beacon_x, self.dist)

    def manhattan_dist(self, x1, x2):
        return np.sum(np.abs(x1 - x2))

    def get_range_at_y(self, y):
        y_dist = np.abs(self.x[1] - y)
        if y_dist > self.dist:
            return None
        remaining = self.dist - y_dist
        return np.array([self.x[0] - remaining, self.x[0] + remaining])

    def get_range_at_y_clamp_x(self, y, x_min, x_max):
        y_dist = np.abs(self.x[1] - y)
        if y_dist > self.dist:
            return None
        remaining = self.dist - y_dist
        left_edge = self.x[0] - remaining
        right_edge = self.x[0] + remaining
        if right_edge < x_min:
            return None
        if left_edge > x_max:
            return None
        if left_edge < x_min:
            left_edge = x_min
        if right_edge > x_max:
            right_edge = x_max
        return np.array([left_edge, right_edge])
        
sensors = []

for line in lines:
    split = line.split()
    x1 = int("".join([char for char in split[2] if char.isnumeric() or char == "-"]))
    y1 = int("".join([char for char in split[3] if char.isnumeric() or char == "-"]))
    x2 = int("".join([char for char in split[8] if char.isnumeric() or char == "-"]))
    y2 = int("".join([char for char in split[9] if char.isnumeric() or char == "-"]))
    sensor = Sensor(x1, y1, x2, y2)
    sensors.append(sensor)

max_search_dimension = 4000000
#max_search_dimension = 20
search_size = max_search_dimension + 1

for search_y in range(0, search_size):
    ranges = []

    for sensor in sensors:
        _range = sensor.get_range_at_y_clamp_x(search_y, 0, max_search_dimension)
        #print("sensor at", sensor.x, "max dist", sensor.dist)
        #print("sensor range at search_y", _range)
        if _range is not None:
            ranges.append(_range)

    ranges = np.array(ranges, dtype=int)

    tmp_ranges = np.copy(ranges)
    iters = 0
    while True:
        found_something = False

        #print(len(tmp_ranges))
        for i, range1 in enumerate(tmp_ranges):
            for j, range2 in enumerate(tmp_ranges):
                if i == j:
                    continue
                #print(i, j, range1, range2, np.min(range1), np.max(range2), np.min(range2), np.max(range1))
                #print(np.min(range1) - 1 > np.max(range2), np.min(range2) - 1 > np.max(range1))
                if np.min(range1) - 1 > np.max(range2) or np.min(range2) - 1 > np.max(range1):
                    continue
                #print("--- confirmed overlap ---")
                #print(i, j)
                #print("before", tmp_ranges[i])
                tmp_ranges[i][0] = np.min([np.min(range1), np.min(range2)])
                tmp_ranges[i][1] = np.max([np.max(range1), np.max(range2)])
                #print("after", tmp_ranges[i])
                #print("before delete", tmp_ranges)
                tmp_ranges = np.delete(tmp_ranges, j, 0)
                #print("after delete", tmp_ranges)
                found_something = True
                break
            if found_something:
                break

        if len(tmp_ranges) == 1:
            #print(len(tmp_ranges))
            found_something = False
            break

        iters += 1
        if iters > len(sensors):
            found_something = True
            break

    if search_y % 1000 == 0:
        print(search_y)

    if found_something:
        print("dbl checking", search_y)
        Map = np.zeros(search_size, dtype=int)

        for _range in ranges:
            Map[_range[0]:_range[1]+1] = 1

        unique, counts = np.unique(Map, return_counts=True)

        if len(unique) == 2:
            for i, val in enumerate(Map):
                if val == 0:
                    print("!!! found freq:", i*4000000 + search_y, "!!!")






