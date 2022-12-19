#!/usr/bin/python3

import numpy as np

class File:
    def __init__(self, size, name):
        self.size = int(size)
        self.name = name

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.files = []
        self.child_directories = []
        self.parent_directory = parent

    def get_size(self):
        size = 0

        for file in self.files:
            size += file.size

        for directory in self.child_directories:
            size += directory.get_size()

        return size

    def file_exists(self, name):
        file_names = [file.name for file in self.files]
        dir_names = [directory.name for directory in self.child_directories]
        if name in file_names or name in dir_names:
            return True
        else:
            return False

    def tree(self, level=1):
        print("-"*level+" dir "+self.name)
        for file in self.files:
            print("-"*(level+1)+" file "+file.name+" "+str(file.size))
        for directory in self.child_directories:
            directory.tree(level+1)

    def crawl_tree_and_return_sizes(self):
        tree = [[self.name, self.get_size()]]
        for directory in self.child_directories:
            child_tree = directory.crawl_tree_and_return_sizes()
            for item in child_tree:
                tree.append(item)
        return tree
        

root = Directory("/", None)

cwd = root

f = open("data.dat", "r")

lines = [line.split() for line in f.readlines()]

i = 0
while i < len(lines):
    line = lines[i]
    if line[0] == "$":
        if line[1] == "ls":
            while i + 1 < len(lines):
                i += 1
                line = lines[i]
                if line[0] == "dir":
                    if not cwd.file_exists(line[1]):
                        new_dir = Directory(line[1], cwd)
                        cwd.child_directories.append(new_dir)
                elif line[0] == "$":
                    i -= 1
                    break
                else:
                    if not cwd.file_exists(line[1]):
                        new_file = File(line[0], line[1])
                        cwd.files.append(new_file)
        elif line[1] == "cd":
            if line[2] == "..":
                cwd = cwd.parent_directory
            else:
                for directory in cwd.child_directories:
                    if directory.name == line[2]:
                        cwd = directory
                        break
    i += 1

root.tree()

total_disk_space = 70000000
free_space = total_disk_space - root.get_size()
needed_space = 30000000
free_this_much = needed_space - free_space

print(total_disk_space, free_space, needed_space, free_this_much)

dirs_that_meet_criteria = []

for item in root.crawl_tree_and_return_sizes():
    if item[1] >= free_this_much:
        dirs_that_meet_criteria.append(item[1])

dirs_that_meet_criteria.sort()
print(dirs_that_meet_criteria)
















