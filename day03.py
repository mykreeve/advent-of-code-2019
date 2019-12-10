import math

filename="input/day3input.txt"
file=open(filename,"r")
file=file.readlines()

lines = [[],[]]
order = 0

for line in file:
    line = line.replace("\n","").split(",")
    for n in line:
        lines[order].append(n)
    order += 1

grid = {}
steps_grid = {}
line_number = 0

for l in lines:
    positionx = 0
    positiony = 0
    steps = 0
    for i in l:
        if i[:1] == 'L':
            for a in range(int(i[1:])):
                steps += 1
                positionx = positionx - 1
                if (positionx, positiony) in grid:
                    grid[(positionx, positiony)] += str(line_number)
                else:
                    grid[(positionx, positiony)] = str(line_number)
                if (positionx, positiony) in steps_grid:
                    steps_grid[(positionx, positiony)] += steps
                else:
                    steps_grid[(positionx, positiony)] = steps
        elif i[:1] == 'R':
            for a in range(int(i[1:])):
                steps += 1
                positionx = positionx + 1
                if (positionx, positiony) in grid:
                    grid[(positionx, positiony)] += str(line_number)
                else:
                    grid[(positionx, positiony)] = str(line_number)
                if (positionx, positiony) in steps_grid:
                    steps_grid[(positionx, positiony)] += steps
                else:
                    steps_grid[(positionx, positiony)] = steps
        elif i[:1] == 'U':
            for a in range(int(i[1:])):
                steps += 1
                positiony = positiony - 1
                if (positionx, positiony) in grid:
                    grid[(positionx, positiony)] += str(line_number)
                else:
                    grid[(positionx, positiony)] = str(line_number)
                if (positionx, positiony) in steps_grid:
                    steps_grid[(positionx, positiony)] += steps
                else:
                    steps_grid[(positionx, positiony)] = steps
        elif i[:1] == 'D':
            for a in range(int(i[1:])):
                steps += 1
                positiony = positiony + 1
                if (positionx, positiony) in grid:
                    grid[(positionx, positiony)] += str(line_number)
                else:
                    grid[(positionx, positiony)] = str(line_number)
                if (positionx, positiony) in steps_grid:
                    steps_grid[(positionx, positiony)] += steps
                else:
                    steps_grid[(positionx, positiony)] = steps
    line_number += 1

crosses = []

for k,v in grid.items():
    if '0' in v and '1' in v:
        crosses.append(k)

min_dist = 99999
min_steps = 99999

for c in crosses:
    dist = abs(c[0])+abs(c[1])
    if dist < min_dist:
        best_cross = c
        min_dist = dist
    if steps_grid[c] < min_steps:
        best_steps = c
        min_steps = steps_grid[c]

print ("Answer for part one:", min_dist)
print ("Answer for part two:", min_steps)