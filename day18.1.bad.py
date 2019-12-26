import re
import heapq
import copy

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

maze[position] = '.'

for door in doors:
    required_key[door] = door.lower()

def get_options(position, collected_keys, maze, visited, time):
    options = []
    possible_spaces = [(position[0], position[1]-1), (position[0], position[1]+1), (position[0]-1, position[1]), (position[0]+1, position[1])]
    for p in possible_spaces:
        new_collected_keys = copy.deepcopy(collected_keys)
        new_collected_keys.sort()
        if maze[p] != '#':
            if maze[p] == '.':
                if [p, new_collected_keys] not in visited and [time+1,p,new_collected_keys] not in queue:
                    options.append([time+1,p,new_collected_keys])
            if maze[p] in keys:
                if maze[p] not in collected_keys:
                    new_collected_keys.append(maze[p])
                    new_collected_keys.sort()
                    if [p,new_collected_keys] not in visited and [time+1,p,new_collected_keys] not in queue:
                        options.append([time+1,p,new_collected_keys])
                else:
                    if [p,new_collected_keys] not in visited and [time+1,p,new_collected_keys] not in queue:
                        options.append([time+1,p,new_collected_keys])
            if maze[p] in doors:
                if required_key[maze[p]] in new_collected_keys:
                    if [p,new_collected_keys] not in visited and [time+1,p,new_collected_keys] not in queue:
                        options.append([time+1,p,new_collected_keys])
    return options

queue = get_options(position, collected_keys, maze, visited, time)
max_time = 0

while len(queue) > 0:
    next_step = heapq.heappop(queue)
    time = next_step[0]
    position = next_step[1]
    collected_keys = next_step[2]
    visited.append([next_step[1], next_step[2]])
    if time > max_time:
        max_time = time
        print("Reached time:", str(time), " - There are", len(queue), "options left in the queue")
    options = get_options(position,collected_keys,maze,visited,time)
    if len(collected_keys) == len(keys):
        print("Answer for part one:", str(time))
        exit()
    for o in options:
        heapq.heappush(queue, o)