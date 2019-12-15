import copy
import random
import heapq

filename="input/day15input.txt"
file=open(filename,"r")
file=file.readlines()

program = {}
position = 0

for line in file:
    line = line.replace("\n","").split(",")
    for n in line:
        program[position] = int(n)
        position += 1

for n in range(1000):
    program[position] = 0
    position += 1

original_program = copy.deepcopy(program)

surface = {}
surface_position = (0,0)
surface[surface_position] = 's'
start = (0,0)
destination = ()

output = ""
input_value = 0
outputs = []
position = 0
relative_base = 0
input_position = 0
program = copy.deepcopy(original_program)

def draw_map(surface):
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    for k in surface:
        if k[0] < minx:
            minx = k[0]
        if k[0] > maxx:
            maxx = k[0]
        if k[1] < miny:
            miny = k[1]
        if k[1] > maxy:
            maxy = k[1]
    # print(minx, maxx, miny, maxy)
    print("")
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x,y) in surface:
                print(surface[(x,y)], end="")
            else:
                print(" ", end="")
        print("")
    print("")

def update_map(output):
    global surface
    global surface_position
    global destination
    if output == 0:
        if input_value == 1:
            surface[(surface_position[0], surface_position[1]-1)] = '#'
        elif input_value == 2:
            surface[(surface_position[0], surface_position[1]+1)] = '#'
        elif input_value == 3:
            surface[(surface_position[0]-1, surface_position[1])] = '#'
        elif input_value == 4:
            surface[(surface_position[0]+1, surface_position[1])] = '#'
    elif output == 1 or output == 2:
        if input_value == 1:
            surface_position = (surface_position[0], surface_position[1]-1)
        elif input_value == 2:
            surface_position = (surface_position[0], surface_position[1]+1)
        elif input_value == 3:
            surface_position = (surface_position[0]-1, surface_position[1])
        elif input_value == 4:
            surface_position = (surface_position[0]+1, surface_position[1])
        if output == 1:
            if surface_position == (0,0):
                surface[surface_position] = 's'
            else:
                surface[surface_position] = '.'
        elif output == 2:
            surface[surface_position] = '*'
            destination = surface_position
            # print(surface, surface_position)
            # draw_map()
            # exit()

def get_options(loc, surface, visited, t):
    opts = []
    if (surface[(loc[0], loc[1]-1)] == '_' or surface[(loc[0], loc[1]-1)] == '.')and (loc[0], loc[1]-1) not in visited:
        opts.append((t+1, loc[0], loc[1]-1))
    if (surface[(loc[0], loc[1]+1)] == '_' or surface[(loc[0], loc[1]+1)] == '.') and (loc[0], loc[1]+1) not in visited:
        opts.append((t+1, loc[0], loc[1]+1))
    if (surface[(loc[0]-1, loc[1])] == '_' or surface[(loc[0]-1, loc[1])] == '.') and (loc[0]-1, loc[1]) not in visited:
        opts.append((t+1, loc[0]-1, loc[1]))
    if (surface[(loc[0]+1, loc[1])] == '_' or surface[(loc[0]+1, loc[1])] == '.') and (loc[0]+1, loc[1]) not in visited:
        opts.append((t+1, loc[0]+1, loc[1]))
    return opts

def find_path(surface):
    # draw_map(surface)
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    for k in surface:
        if k[0] < minx:
            minx = k[0]
        if k[0] > maxx:
            maxx = k[0]
        if k[1] < miny:
            miny = k[1]
        if k[1] > maxy:
            maxy = k[1]
    places = 0
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x,y) in surface:
                if surface[(x,y)] == '_' or surface[(x,y)] == '.':
                    places += 1
    location = start
    time = 0
    curr = time
    visited = []
    queue = []
    for n in get_options(location, surface, visited, time):
        heapq.heappush(queue, n)
    while location != destination:
        v = heapq.heappop(queue)
        time = v[0]
        location = (v[1],v[2])
        if time != curr:
            curr = time
            # print(time)
            # draw_map()
            # mm = input('.')
        visited.append(location)
        if location == destination:
            print("Answer for part one:", time)
        for n in get_options(location, surface, visited, time):
            heapq.heappush(queue, n)
        # print(len(visited))


def find_fill(surface):
    # draw_map(surface)
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    for k in surface:
        if k[0] < minx:
            minx = k[0]
        if k[0] > maxx:
            maxx = k[0]
        if k[1] < miny:
            miny = k[1]
        if k[1] > maxy:
            maxy = k[1]
    places = 0
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x,y) in surface:
                if surface[(x,y)] == '_' or surface[(x,y)] == '.':
                    places += 1
    location = destination
    time = 0
    curr = time
    visited = []
    queue = []
    for n in get_options(location, surface, visited, time):
        heapq.heappush(queue, n)
    while len(queue) > 0:
        v = heapq.heappop(queue)
        time = v[0]
        location = (v[1],v[2])
        if time != curr:
            curr = time
        surface[location] = 'O'
        visited.append(location)
        for n in get_options(location, surface, visited, time):
            heapq.heappush(queue, n)
    print("Answer to part two:",time)


def get_input(output):
    global surface
    # draw_map()
    options = [1,2,3,4]
    surrounds = []
    if (surface_position[0], surface_position[1]-1) in surface:
        surrounds.append(surface[(surface_position[0], surface_position[1]-1)])
    else:
        surrounds.append(" ")
    if (surface_position[0], surface_position[1]+1) in surface:
        surrounds.append(surface[(surface_position[0], surface_position[1]+1)])
    else:
        surrounds.append(" ")
    if (surface_position[0]-1, surface_position[1]) in surface:
        surrounds.append(surface[(surface_position[0]-1, surface_position[1])])
    else:
        surrounds.append(" ")
    if (surface_position[0]+1, surface_position[1]) in surface:
        surrounds.append(surface[(surface_position[0]+1, surface_position[1])])
    else:
        surrounds.append(" ")
    count_surrounds = 0
    pos = 0
    for s in surrounds:
        if s == '#' or s == '_' or s == 's' or s == '*':
            count_surrounds += 1
            options.remove(pos+1)
        pos += 1
    if count_surrounds == 3:
        surface[surface_position] = '_'
    if len(options) == 0:
        find_path(surface)
        find_fill(surface)
        exit()
    return random.choice(options)

while program[position] != 99:
    opcode = int(str(program[position])[-2:])
    parameters = list(str(program[position])[:-2])

    while len(parameters)<3:
        parameters.insert(0,'0')
    parameters.reverse()

    if opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8 or opcode == 9:
        if parameters[0] == '0':
            a = program[program[position+1]]
        elif parameters[0] == '1':
            a = program[position+1]
        elif parameters[0] == '2':
            a = program[relative_base+program[position+1]]
    if opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8:
        if parameters[1] == '0':
            b = program[program[position+2]]
        elif parameters[1] == '1':
            b = program[position+2]
        elif parameters[1] == '2':
            b = program[relative_base+program[position+2]]
    if opcode == 7 or opcode == 8:
        if parameters[2] == '0':
            c = program[position+3]
        elif parameters[2] == '1':
            c = position+3
        elif parameters[2] == '2':
            c = relative_base+program[position+3]

    if opcode == 1:
        if parameters[2] == '0':
            program[program[position+3]] = (a + b)
            # print("1) Setting position", program[position+3], "to", (a+b))
        elif parameters[2] == '1':
            program[position+3] = (a + b)
            # print("1) Setting position", (position+3), "to", (a+b))
        elif parameters[2] == '2':
            program[relative_base+program[position+3]] = (a + b)
            # print("1) Setting position", (relative_base+program[position+3]), "to", (a+b))
        position += 4
    elif opcode == 2:
        if parameters[2] == '0':
            program[program[position+3]] = (a * b)
            # print("2) Setting position", program[position+3], "to", (a*b))
        elif parameters[2] == '1':
            program[position+3] = (a * b)
            # print("2) Setting position", (position+3), "to", (a*b))
        elif parameters[2] == '2':
            program[relative_base+program[position+3]] = (a * b)
            # print("2) Setting position", (relative_base+program[position+3]), "to", (a*b))
        position += 4
    elif opcode == 3:
        update_map(output)
        input_value = get_input(output)
        if parameters[0] == '0':
            program[program[position+1]] = input_value
            # print("3) Setting position", program[position+1], "to", x)
        elif parameters[0] == '1':
            program[position+1] = input_value
            # print("3) Setting position", (position+1), "to", x)
        elif parameters[0] == '2':
            program[relative_base+program[position+1]] = input_value
            # print("3) Setting position", (relative_base+program[position+1]), "to", x)
        position += 2
        input_position += 1
    elif opcode == 4:
        if parameters[0] == '0':
            # print("4) Setting output to", program[program[position+1]])
            output = (program[program[position+1]])
        elif parameters[0] == '1':
            # print("4) Setting output to", program[position+1])
            output = (program[position+1])
        elif parameters[0] == '2':
            # print("4) Setting output to", program[relative_base+program[position+1]])
            output = (program[relative_base+program[position+1]])
        position += 2
    elif opcode == 5:
        if a != 0:
            position = b
            # print("5) Moving pointer to", b)
        else:
            position += 3
    elif opcode == 6:
        if a == 0:
            position = b
            # print("6) Moving pointer to", b)
        else:
            position += 3
    elif opcode == 7:
        if a < b:
            # print("7) Setting position", c, "to", '1')
            program[c] = 1
        else:
            # print("7) Setting position", c, "to", '0')
            program[c] = 0
        position += 4
    elif opcode == 8:
        if a == b:
            # print("8) Setting position", c, "to", '1')
            program[c] = 1
        else:
            # print("8) Setting position", c, "to", '0')
            program[c] = 0
        position += 4
    elif opcode == 9:
        # print("9) Changing relative base from", relative_base, "to", (relative_base+a))
        relative_base += a
        position += 2
    else:
        print ("Problem with execution:", program[position])

count = 0
for a in surface.items():
    count += 1
print("Answer for part one:", count)
