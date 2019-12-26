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

def get_location(unique, maze):
    for k,v in maze.items():
        if v == unique:
            return k
    return None

initial_position = get_location('@',maze)

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
robot_journeys = {}
key_locations = []

print("Getting distances from start")
queue = []
visited = []
time = 0
queue = get_options(initial_position, [],[],maze,visited,time)
while len(queue) > 0:
    time,position,doors_passed,keys_passed = heapq.heappop(queue)
    location_content = maze[position]
    if location_content != '.':
        if location_content in keys:
            key_count += 1
            robot_journeys[("@",location_content)] = (time, doors_passed, keys_passed)
            key_locations.append(location_content)
    visited.append(position)
    options = get_options(position, doors_passed, keys_passed, maze, visited, time)
    for o in options:
        heapq.heappush(queue, o)

working_on = ''
for combo in itertools.combinations(keys,2):
    if combo[0] != working_on:
        working_on = combo[0]
        print("Getting distances from", working_on)
    start = get_location(combo[0], maze)
    visited = []
    time = 0
    queue = get_options(start, [], [], maze, visited, time)
    while len(queue) > 0 and combo not in robot_journeys:
        time, position, doors_passed, keys_passed = heapq.heappop(queue)
        location_content = maze[position]
        if location_content == combo[1]:
            robot_journeys[combo] = (time, doors_passed, keys_passed)
            keys_passed.append(combo[0])
            robot_journeys[(combo[1],combo[0])] = (time, doors_passed, keys_passed)
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

def get_robot_moves(location, keys_collected, robot_journeys, visited, time):
    options = []
    for key in keys:
        if key not in keys_collected:
            new_keys_collected = copy.deepcopy(keys_collected)
            distance, doors, key_list = robot_journeys[(location,key)]
            key_list_copy = copy.deepcopy(key_list)
            key_list_copy.remove(key)
            if can_get_through_doors(doors,keys_collected) and no_keys_in_way(key_list_copy, keys_collected):
                new_keys_collected.append(key)
                new_keys_collected.sort()
                new_location=key
                if (new_location, new_keys_collected) not in visited:
                    robstr = ''.join(new_location)
                    keystr = ''.join(new_keys_collected)
                    if (robstr,keystr) in added_to_queue:
                        if added_to_queue[(robstr,keystr)] > time+distance:
                            queue.remove((added_to_queue[(robstr,keystr)], new_location, new_keys_collected))
                            added_to_queue[(robstr,keystr)] = time+distance
                            options.append((time+distance,new_location,new_keys_collected))
                    else:
                        added_to_queue[(robstr,keystr)] = time+distance
                        options.append((time+distance,new_location,new_keys_collected))
    return options

location = '@'
queue = []
visited = []
time = 0
max_keys = 0
keys_collected = []
opts = get_robot_moves(location,keys_collected,robot_journeys,visited,time)
for o in opts:
    heapq.heappush(queue,o)
while len(queue) > 0:
    time,location,keys_collected = heapq.heappop(queue)
    if len(keys_collected) > max_keys:
        max_keys = len(keys_collected)
        print("Time:",time,"Location:",location,"Most keys collected:",max_keys,"/",len(keys),"Queue length:",len(queue))        
    visited.append((location,keys_collected))
    if len(keys_collected) == len(keys):
        print("Answer for part one:", time)
        exit()
    opts = get_robot_moves(location,keys_collected,robot_journeys,visited,time)
    for o in opts:
        heapq.heappush(queue,o)
    
        