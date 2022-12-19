#!/usr/bin/python3

import numpy as np

f = open("data.dat", "r")

lines = [line.strip() for line in f.readlines()]

class Sensor():
    def __init__(self, x1, y1, x2, y2):
        self.x = np.array([x1, y1], dtype=int)
        self.beacon_x = np.array([x2, y2], dtype=int)
        self.dist = self.manhattan_dist(self.x, self.beacon_x)

    def manhattan_dist(self, x1, x2):
        return np.sum(np.abs(x1 - x2))

    def get_range_at_y(self, y):
        y_dist = np.abs(self.x[1] - y)
        if y_dist > self.dist:
            return None
        remaining = self.dist - y_dist
        return np.array([self.x[0] - remaining, self.x[0] + remaining])
        
search_y = 10

sensors = []

for line in lines:
    split = line.split()
    x1 = int("".join([char for char in split[2] if char.isnumeric()]))
    y1 = int("".join([char for char in split[3] if char.isnumeric()]))
    x2 = int("".join([char for char in split[8] if char.isnumeric()]))
    y2 = int("".join([char for char in split[9] if char.isnumeric()]))
    sensor = Sensor(x1, y1, x2, y2)
    sensors.append(sensor)

ranges = []

for sensor in sensors:
    _range = sensor.get_range_at_y(search_y)
    if _range is not None:
        ranges.append(_range)

ranges = np.array(ranges, dtype=int)
left_edge = np.min(ranges[:,0])
right_edge = np.max(ranges[:,1])

print(ranges)
print(left_edge)
print(right_edge)
print()

total_size = right_edge - left_edge + 1

ranges[:,0] -= left_edge
ranges[:,1] -= left_edge

print(ranges)
print(total_size)
print()

Map = np.zeros(total_size, dtype=int)

for _range in ranges:
    print(_range)
    Map[_range[0]:_range[1]+1] = 1

for sensor in sensors:
    if sensor.beacon_x[1] == search_y:
        Map[sensor.beacon_x[0] - left_edge] = 0

print()
print(Map)

unique, counts = np.unique(Map, return_counts=True)
print(unique, counts)

total_spaces = np.max(counts)

print(total_spaces)





