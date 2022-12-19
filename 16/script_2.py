#!/usr/bin/python3

import numpy as np

class Valve():
    def __init__(self, name, flow_rate, connections):
        self.name = name
        self.flow_rate = flow_rate
        self.simple_connections = connections
        self.state = 1

    def update_with_id_dict_and_valves(self, id_dict, valves):
        self.valves = valves
        self.id_dict = id_dict
        self.name_dict = {v: k for k, v in self.id_dict.items()}
        self.id_num = name_to_id[self.name]
        self.simple_numeric_connections = [name_to_id[name] for name in self.simple_connections]
        self.connections = np.copy(np.array(self.simple_numeric_connections, dtype=int))
        self.costs = np.ones_like(self.connections, dtype=int)

    def print_connections(self):
        print(" " + self.name + " flow_rate: " + str(self.flow_rate))
        for i, connection in enumerate(self.connections):
            print("  → " + self.name_dict[connection] + " cost: " + str(self.costs[i]) + " flow_rate: " + str(self.valves[connection].flow_rate))

    def collapse_simple_connections(self):

        for i, connection in enumerate(self.connections):
            if self.valves[connection].flow_rate == 0:
                cost = self.costs[i]
                self.costs = np.delete(self.costs, i)
                self.connections = np.delete(self.connections, i)
                for j, connection_j in enumerate(valves[connection].connections):
                    self.costs = np.append(self.costs, cost + valves[connection].costs[j])
                self.connections = np.append(self.connections, valves[connection].connections)
                break

        self.remove_dupes()

    def extend_farther_connections(self):

        for i, connection in enumerate(self.connections):
            cost = self.costs[i]
            for j, connection_j in enumerate(valves[connection].connections):
                self.costs = np.append(self.costs, cost + valves[connection].costs[j])
            self.connections = np.append(self.connections, valves[connection].connections)

        self.remove_dupes()


    def remove_dupes(self):
        to_delete = []
        for i, connection in enumerate(self.connections):
            if connection == self.id_num:
                to_delete.append(i)

        self.costs = np.delete(self.costs, to_delete)
        self.connections = np.delete(self.connections, to_delete)

        uniques, counts = np.unique(self.connections, return_counts=True)

        dupes = []

        for index, count in enumerate(counts):
            if count > 1:
                dupes.append(uniques[index])

        for dupe in dupes:
            dupe_indices = []
            for idx, connection in enumerate(self.connections):
                if connection == dupe:
                    dupe_indices.append(idx)
            lowest_cost = np.min(self.costs[dupe_indices])

            got_one = False
            to_delete = []
            for i in dupe_indices:
                if self.costs[i] > lowest_cost or got_one == True:
                    to_delete.append(i)
                if self.costs[i] == lowest_cost and got_one == False:
                    got_one = True
            self.costs = np.delete(self.costs, to_delete)
            self.connections = np.delete(self.connections, to_delete)

def get_pressure_for_path(path_me, path_elephant):

    minute = 1
    max_minutes = 26
    pressure = 0
    pressure_per_minute = 0

    current_path_me = 0
    current_path_elephant = 0
    steps_me = 0
    steps_elephant = 0

    #print(path_me, path_elephant)

    while minute <= max_minutes:

        pressure += pressure_per_minute

        if current_path_me < len(path_me):
            steps_me += 1
            if steps_me > path_me[current_path_me][1]:
                steps_me = 0
                pressure_per_minute += path_me[current_path_me][2]
                current_path_me += 1

        if current_path_elephant < len(path_elephant):
            steps_elephant += 1
            if steps_elephant > path_elephant[current_path_elephant][1]:
                steps_elephant = 0
                pressure_per_minute += path_elephant[current_path_elephant][2]
                current_path_elephant += 1
                

        minute += 1


    '''
    for connection, cost, flow_rate in path_me:
        for time_counter in range(cost):
            if minute > max_minutes:
                break

            minute += 1
            pressure += pressure_per_minute

        if minute > max_minutes:
            break
        
        minute += 1
        pressure += pressure_per_minute
        pressure_per_minute += flow_rate
    '''

    return pressure

f = open("data.dat", "r")

lines = [line.split() for line in f.readlines()]

valves = []

for line in lines:
    name = line[1]
    rate = int("".join([char for char in line[4] if char.isnumeric()]))
    connections = [connection.replace(",", "") for connection in line[9:]]
    valve = Valve(name, rate, connections)
    valves.append(valve)

name_to_id = {}

for i, valve in enumerate(valves):
    name_to_id[valve.name] = i

for valve in valves:
    valve.update_with_id_dict_and_valves(name_to_id, valves)
'''
for valve in valves:
    valve.print_connections()
'''
for i in range(10):
    for valve in valves:
        valve.collapse_simple_connections()

for i in range(10):
    for valve in valves:
        valve.extend_farther_connections()

nonzero_valves = []

for valve in valves:
    '''
    if valve.name == "AA" or valve.flow_rate > 0:
        valve.print_connections()
    '''
    if valve.flow_rate > 0:
        nonzero_valves.append(valve)

highest_pressure = -1
best_path = []

for rando_guesses in range(0, 100000):
    cost_modifier = np.random.randint(0,5)
    current_valve_me = valves[name_to_id["AA"]]
    current_valve_elephant = valves[name_to_id["AA"]]
    path_me = []
    path_elephant = []
    for counter in range(len(nonzero_valves)//2):

        scores = [ [( valves[connection].flow_rate + np.random.randint(1, 20 + 1) - cost_modifier * current_valve_me.costs[idx] + 100 ) * valves[connection].state, connection, current_valve_me.costs[idx]] for idx, connection in enumerate(current_valve_me.connections) ]
        scores = np.array(scores)
        highest_score = np.max(scores[:,0])
        for score, connection, cost in scores:
            if score == highest_score:
                path_me.append([connection, cost, valves[connection].flow_rate])
                current_valve_me = valves[connection]
                current_valve_me.state = 0
                break

        scores = [ [( valves[connection].flow_rate + np.random.randint(1, 20 + 1) - cost_modifier * current_valve_elephant.costs[idx] + 100 ) * valves[connection].state, connection, current_valve_elephant.costs[idx]] for idx, connection in enumerate(current_valve_elephant.connections) ]
        scores = np.array(scores)
        highest_score = np.max(scores[:,0])
        for score, connection, cost in scores:
            if score == highest_score:
                path_elephant.append([connection, cost, valves[connection].flow_rate])
                current_valve_elephant = valves[connection]
                current_valve_elephant.state = 0
                break

    #print(path_me)
    #print(path_elephant)

    current_pressure = get_pressure_for_path(path_me, path_elephant)
    #print(current_pressure, " me: ", end="")
    #for connection, cost, flow_rate in path_me:
        #print(valves[connection].name, "", end="")
    #print(" elephant: ", end="")
    #for connection, cost, flow_rate in path_elephant:
        #print(valves[connection].name, "", end="")
    #print()

    if current_pressure > highest_pressure:
        highest_pressure = current_pressure
        best_path = [path_me, path_elephant]

    for valve in valves:
        valve.state = 1

print(highest_pressure)
print(best_path)



