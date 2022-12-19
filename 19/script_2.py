#!/usr/bin/python3

import numpy as np

def have_materials(inventory, costs):
    have_question_mark = True
    for key, val in costs.items():
        if inventory[key] < val:
            have_question_mark = False
    return have_question_mark

def simulation(weights, blueprint):

    robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
    inventory = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
    
    build_prio = {}
    build_prio["ore"]      = weights[0]
    build_prio["clay"]     = weights[1]
    build_prio["obsidian"] = weights[2]
    build_prio["geode"]    = weights[3]
    
    build_options = ["ore", "clay"]
    
    max_ore = np.max([blueprint["clay"]["ore"], blueprint["obsidian"]["ore"], blueprint["geode"]["ore"]])
    #max_ore = blueprint["geode"]["ore"]
    max_clay = blueprint["obsidian"]["clay"]
    max_obsidian = blueprint["geode"]["obsidian"]

    minute = 1
    while minute <= 32:
    
        highest_prio = -1000
        rando_build_prio = build_prio.copy()
        for key, val in rando_build_prio.items():
            if key in build_options:
                rando_build_prio[key] += np.random.randint(weights[4])
                if key == "ore" and robots["ore"] > max_ore:
                    rando_build_prio[key] -= 100000
                elif key == "clay" and robots["clay"] > max_clay:
                    rando_build_prio[key] -= 100000
                elif key == "obsidian" and robots["obsidian"] > max_obsidian:
                    rando_build_prio[key] -= 100000
                if have_materials(inventory, blueprint[key]):
                    rando_build_prio[key] += weights[5]
                    if key == "obsidian":
                        rando_build_prio[key] += 100
                    elif key == "geode":
                        rando_build_prio[key] += 100000
                highest_prio = np.max((highest_prio, rando_build_prio[key]))
        for key, val in rando_build_prio.items():
            if val == highest_prio and key in build_options:
                chosen_option = key
                break
    
        build_robots = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        if have_materials(inventory, blueprint[chosen_option]):
            build_robots[chosen_option] += 1
            if chosen_option == "clay" and "obsidian" not in build_options:
                build_options.append("obsidian")
            if chosen_option == "obsidian" and "geode" not in build_options:
                build_options.append("geode")
            for key, val in blueprint[chosen_option].items():
                inventory[key] -= val

        for key, val in robots.items():
            inventory[key] += val
        
        for key, val in build_robots.items():
            robots[key] += val
        
        #print("minute", minute)
        #print("robots", robots)
        #print("inventory", inventory)
        
        minute += 1
    
    return inventory["geode"]

f = open("data.dat", "r")

lines = [line.strip() for line in f.readlines()]

blueprints = []

for line in lines:
    split_line = line.split()
    blueprint = {}
    blueprint["ore"] = {"ore": int(split_line[6])}
    blueprint["clay"] = {"ore": int(split_line[12])}
    blueprint["obsidian"] = {"ore": int(split_line[18]), "clay": int(split_line[21])}
    blueprint["geode"] = {"ore": int(split_line[27]), "obsidian": int(split_line[30])}
    blueprints.append(blueprint)

weights = np.array([0.5, 10, 20, 30, 20, 100])

def get_score(weights, averaging, blueprint):
    #sum = 0
    #for blueprint in blueprints:
    #    for i in range(averaging):
    #        sum += simulation(weights, blueprints[0])
    #sum /= len(blueprints) * averaging
    #return sum
    #return np.max([simulation(weights, blueprint) for i in range(averaging) for blueprint in blueprints])
    return np.max([simulation(weights, blueprint) for i in range(averaging)])

def genetic_opt(initial_weights, blueprint):

    initial_num = 10000
    
    weight_matrix = np.random.normal(0.0, 100.0, size=(initial_num, len(initial_weights)))
    
    for weight in weight_matrix:
        if weight[4] < 1.0:
            weight[4] = 1.0

    scores = np.zeros(initial_num, dtype=float)
    
    for i, weight in enumerate(weight_matrix):
        scores[i] = get_score(weight, 1, blueprint)
        
    sort = np.argsort(scores)
        
    weight_matrix = weight_matrix[sort]
    scores = scores[sort]
    
    initial_num = 1000
    
    weight_matrix = weight_matrix[-initial_num:]

    scores = np.zeros(initial_num, dtype=float)
    
    for i, weight in enumerate(weight_matrix):
        scores[i] = get_score(weight, 10, blueprint)
        
    sort = np.argsort(scores)
        
    weight_matrix = weight_matrix[sort]
    scores = scores[sort]
    
    #print("initial scores", scores)

    num = 100
    
    weight_matrix = weight_matrix[-num:]
    
    steps = 100
    
    for step in range(steps):
    
        lr = 2 - 2 * (step/steps)
    
        scores = np.zeros(num, dtype=float)
        
        weight_matrix += np.random.normal(scale=lr, size=(num, len(initial_weights)))
        
        for weight in weight_matrix:
            if weight[4] < 1.0:
                weight[4] = 1.0
        
        for i, weight in enumerate(weight_matrix):
            scores[i] = get_score(weight, 500, blueprint)
        
        sort = np.argsort(scores)
        
        weight_matrix = weight_matrix[sort]
        scores = scores[sort]
        
        for i in range(len(weight_matrix)//2):
            j = len(weight_matrix)//2 + i
            weight_matrix[i] = weight_matrix[j]

        print("step", step, "lr", lr, "scores", scores)
    
    #print(weight_matrix[-1])
    
    return weight_matrix

sum = 1

for i, blueprint in enumerate(blueprints[:3]):
    if i <= 1:
        continue
    print("blueprint", i+1)
    weight_matrix = genetic_opt(weights, blueprint)

    geodes = np.max([simulation(weights, blueprint) for i in range(1000) for weights in weight_matrix])
    print("max geode", i+1, geodes)
    sum *= geodes
    
#print(max_geodes)
print("quality levels", sum)

# 57, 28, 10
# 51, 28, 9





