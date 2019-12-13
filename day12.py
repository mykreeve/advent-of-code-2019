from itertools import combinations
import copy
import numpy as np

filename="input/day12input.txt"
file=open(filename,"r")
file=file.readlines()

planet_position = {}
planet_velocity = {}
planet = 0

for line in file:
    line = line.replace("\n","").replace("<","").replace(">","").replace(", ",",")
    line = line.replace("x=","").replace("y=","").replace("z=","").split(",")
    planet_position[planet] = {'x': int(line[0]), 'y': int(line[1]), 'z': int(line[2])}
    planet_velocity[planet] = {'x': 0, 'y': 0, 'z': 0}
    planet += 1

init_position = copy.deepcopy(planet_position)
init_velocity = copy.deepcopy(planet_velocity)

def amend_velocity (pos, vel):
    pairs = combinations([0,1,2,3],2)
    for p in pairs:
        if pos[p[0]]['x'] > pos[p[1]]['x']:
            vel[p[0]]['x'] -= 1
            vel[p[1]]['x'] += 1
        elif pos[p[0]]['x'] < pos[p[1]]['x']:
            vel[p[0]]['x'] += 1
            vel[p[1]]['x'] -= 1
        if pos[p[0]]['y'] > pos[p[1]]['y']:
            vel[p[0]]['y'] -= 1
            vel[p[1]]['y'] += 1
        elif pos[p[0]]['y'] < pos[p[1]]['y']:
            vel[p[0]]['y'] += 1
            vel[p[1]]['y'] -= 1
        if pos[p[0]]['z'] > pos[p[1]]['z']:
            vel[p[0]]['z'] -= 1
            vel[p[1]]['z'] += 1
        elif pos[p[0]]['z'] < pos[p[1]]['z']:
            vel[p[0]]['z'] += 1
            vel[p[1]]['z'] -= 1
    return vel

def amend_position (pos, vel):
    for a in [0,1,2,3]:
        pos[a]['x'] += vel[a]['x']
        pos[a]['y'] += vel[a]['y']
        pos[a]['z'] += vel[a]['z']
    return pos

time = 0
while time < 1000:
    planet_velocity = amend_velocity(planet_position, planet_velocity)
    planet_position = amend_position(planet_position, planet_velocity)
    time += 1
    energy = 0
    for a in [0,1,2,3]:
        pot = (abs(planet_position[a]['x']) + abs(planet_position[a]['y']) + abs(planet_position[a]['z']))
        kin = (abs(planet_velocity[a]['x']) + abs(planet_velocity[a]['y']) + abs(planet_velocity[a]['z']))
        energy += (pot * kin)
print("Answer for part one:", energy)

time = 0
planet_position = copy.deepcopy(init_position)
planet_velocity = copy.deepcopy(init_velocity)
periodicity = {}
last = {}

def calc_lcm(a,b,c):
    print("Answer for part two:", np.lcm.reduce([a,b,c]))
    exit()

def evaluate(pos,vel):
    if pos == init_position and vel == init_velocity and time > 0:
        return False
    for ax in ['x','y','z']:
        plct = 0
        for pl in [0,1,2,3]:
            if pos[pl][ax] == init_position[pl][ax] and vel[pl][ax] == 0:
                plct += 1
        if plct > 3:
            # print(plct, "planets are back at start position on axis", ax, "after", time)
            if ax not in periodicity and ax not in last:
                last[ax] = time
            elif ax not in periodicity:
                periodicity[ax] = last[ax]
                last[ax] = time
            else:
                periodicity[ax] = time - last[ax]
                last[ax] = time
            check = 0
            for a in ['x','y','z']:
                if a in periodicity and periodicity[a] != 0:
                    check += 1
            if check == 3:
                calc_lcm(periodicity['x'], periodicity['y'], periodicity['z'])
    return True

while evaluate(planet_position, planet_velocity):
    planet_velocity = amend_velocity(planet_position, planet_velocity)
    planet_position = amend_position(planet_position, planet_velocity)
    time += 1
