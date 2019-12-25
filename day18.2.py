import re
import heapq
import copy
import itertools

queue = []
maze = {}
required_key = {}
keys = []
doors = []
collected_keys = []
visited = []
time = 0

fileContents = open('input/day18input.txt', 'r')
f = fileContents.readlines()
y = 0
for line in f:
    line = line.replace('\n','')
    line = list(line)
    x = 0
    for char in line:
        maze[(x,y)] = char
        x += 1
    y += 1

position = (0,0)
for pos,val in maze.items():
    if val == '@':
        position = pos
    k = re.findall("([A-Z])", val)
    if k:
        doors.append(k[0])
    k = re.findall("([a-z])", val)
    if k:
        keys.append(k[0])

maze[(position[0]-1,position[1]-1)] = '@'
maze[(position[0],position[1]-1)] = '#'
maze[(position[0]+1,position[1]-1)] = '@'
maze[(position[0]-1,position[1])] = '#'
maze[(position[0],position[1])] = '#'
maze[(position[0]+1,position[1])] = '#'
maze[(position[0]-1,position[1]+1)] = '@'
maze[(position[0],position[1]+1)] = '#'
maze[(position[0]+1,position[1]+1)] = '@'

robots = {}
robot_number = 0

for k,v in maze.items():
    if v == '@':
        robots[robot_number] = k
        robot_number += 1

def get_location(unique, maze):
    for k,v in maze.items():
        if v == unique:
            return k
    return None

def get_options(position, doors_passed, keys_passed, maze, visited, time):
    options = []
    possible_spaces = [(position[0], position[1]-1), (position[0], position[1]+1), (position[0]-1, position[1]), (position[0]+1, position[1])]
    for p in possible_spaces:
        if maze[p] != '#':
            new_keys_passed = copy.deepcopy(keys_passed)
            new_doors_passed = copy.deepcopy(doors_passed)
            k = re.findall("([A-Z])", maze[p])
            if k:
                new_doors_passed.append(k[0])
            k = re.findall("([a-z])", maze[p])
            if k:
                new_keys_passed.append(k[0])
            if p not in visited and [time+1,p,new_doors_passed,new_keys_passed] not in queue:
                    options.append([time+1,p,new_doors_passed,new_keys_passed])
    return options

key_count = 0
door_count = 0
robot_journeys = {}
key_locations = {}

for robot_number,robot_start in robots.items():
    print("Getting distances from start for robot",str(robot_number))
    robot_journeys[robot_number] = {}
    key_locations[robot_number] = []
    queue = []
    visited = []
    time = 0
    queue = get_options(robot_start, [], [], maze, visited, time)
    while len(queue) > 0:
        time,position,doors_passed,keys_passed = heapq.heappop(queue)
        location_content = maze[position]
        if location_content != '.':
            if location_content in keys:
                key_count += 1
                robot_journeys[robot_number][("@",location_content)] = (time, doors_passed, keys_passed)
                key_locations[robot_number].append(location_content)
                # print('Distance for robot', robot_number, 'to key', location_content, 'is', time, " - Keys found:", key_count, ' - Doors passed:', doors_passed)
            if location_content in doors:
                door_count += 1
                # print('Distance for robot', robot_number, 'to door', location_content, 'is', time, " - Doors found:", door_count, ' - Doors passed:', doors_passed)
        visited.append(position)
        options = get_options(position, doors_passed, keys_passed, maze, visited, time)
        for o in options:
            heapq.heappush(queue, o)

# print (key_locations)
for robot_number,keys_in_loc in key_locations.items():
    print("Getting distances between keys for robot", str(robot_number))
    for combo in itertools.combinations(keys_in_loc,2):
        start = get_location(combo[0], maze)
        visited = []
        time = 0
        queue = get_options(start, [], [], maze, visited, time)
        while len(queue) > 0 and combo not in robot_journeys[robot_number]:
            time, position, doors_passed, keys_passed = heapq.heappop(queue)
            location_content = maze[position]
            if location_content == combo[1]:
                robot_journeys[robot_number][combo] = (time, doors_passed, keys_passed)
                keys_passed.append(combo[0])
                robot_journeys[robot_number][(combo[1],combo[0])] = (time, doors_passed, keys_passed)
            visited.append(position)
            options = get_options(position, doors_passed, keys_passed, maze, visited, time)
            for o in options:
                heapq.heappush(queue,o)
        # print("Journey from", combo[0], "to", combo[1], "takes", time, "steps, and you pass these doors:", doors_passed)

def can_get_through_doors(doors,keys_collected):
    for door in doors:
        if door.lower() not in keys_collected:
            return False
    return True

def no_keys_in_way(key_list, keys_collected):
    for k in key_list:
        if k not in keys_collected:
            return False
    return True

def queue_rationalisation(t,loc,keys):
    for a in queue:
        if a[0] <= t and a[1] == loc and a[2] == keys:
            return False
    return True

added_to_queue = {}

def get_robot_moves(robot_locations, keys_collected, robot_journeys, visited, time):
    options = []
    for robot_number in range(len(robot_locations)):
        robot_loc = robot_locations[robot_number]
        for key in key_locations[robot_number]:
            if key not in keys_collected:
                new_keys_collected = copy.deepcopy(keys_collected)
                new_robot_locations = copy.deepcopy(robot_locations)
                distance, doors, key_list = robot_journeys[robot_number][(robot_loc,key)]
                key_list_copy = copy.deepcopy(key_list)
                key_list_copy.remove(key)
                if can_get_through_doors(doors,keys_collected) and no_keys_in_way(key_list_copy, keys_collected):
                    new_keys_collected.append(key)
                    new_keys_collected.sort()
                    new_robot_locations[robot_number]=key
                    if (new_robot_locations, new_keys_collected) not in visited:
                        robstr = ''.join(new_robot_locations)
                        keystr = ''.join(new_keys_collected)
                        if (robstr,keystr) in added_to_queue:
                            if added_to_queue[(robstr,keystr)] > time+distance:
                                queue.remove((added_to_queue[(robstr,keystr)], new_robot_locations, new_keys_collected))
                                added_to_queue[(robstr,keystr)] = time+distance
                                options.append((time+distance,new_robot_locations,new_keys_collected))
                        else:
                            added_to_queue[(robstr,keystr)] = time+distance
                            options.append((time+distance,new_robot_locations,new_keys_collected))
    return options

robot_locations = ['@','@','@','@']
queue = []
visited = []
time = 0
max_keys = 0
keys_collected = []
opts = get_robot_moves(robot_locations,keys_collected,robot_journeys,visited,time)
for o in opts:
    heapq.heappush(queue,o)
while len(queue) > 0:
    time,robot_locations,keys_collected = heapq.heappop(queue)
    if len(keys_collected) > max_keys:
        max_keys = len(keys_collected)
        print("Time:",time,"Robots:",robot_locations,"Most keys collected:",max_keys,"/",len(keys),"Queue length:",len(queue))        
    visited.append((robot_locations,keys_collected))
    if len(keys_collected) == len(keys):
        print("Answer for part two:", time)
        exit()
    opts = get_robot_moves(robot_locations,keys_collected,robot_journeys,visited,time)
    for o in opts:
        heapq.heappush(queue,o)
    
        