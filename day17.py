import copy

filename="input/day17input.txt"
file=open(filename,"r")
file=file.readlines()

program = {}
position = 0

for line in file:
    line = line.replace("\n","").split(",")
    for n in line:
        program[position] = int(n)
        position += 1

for n in range(3000):
    program[position] = 0
    position += 1

original_program = copy.deepcopy(program)

input_value = 0
xpos = -1
ypos = 0
grid = {}
position = 0
relative_base = 0
input_position = 0
program = copy.deepcopy(original_program)


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
            x = (program[program[position+1]])
        elif parameters[0] == '1':
            # print("4) Setting output to", program[position+1])
            x = (program[position+1])
        elif parameters[0] == '2':
            # print("4) Setting output to", program[relative_base+program[position+1]])
            x = (program[relative_base+program[position+1]])
        xpos += 1
        if x == 10:
            xpos = -1
            ypos += 1
        else:
            grid[(xpos, ypos)] = chr(x)
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

maxx = 0
maxy = 0
for g,val in grid.items():
    if g[0] > maxx:
        maxx = g[0]
    if g[1] > maxy:
        maxy = g[1]

# for y in range(maxy+1):
#     for x in range(maxx+1):
#         print (grid[(x,y)],end="")
#     print("")

tots = 0

for y in range(1,maxy):
    for x in range(1,maxx):
        adj = [(-1,0),(1,0),(0,-1),(0,1)]
        surrounds = 0
        for a in adj:
            if grid[(x+a[0],y+a[1])] == '#':
                surrounds += 1
        if surrounds == 4 and grid[(x,y)] == '#':
            tots += (x*y)

print ("Answer for part one:", tots)


#grid route

def get_position(symbol,grid):
    for k,v in grid.items():
        if v == symbol:
            return k
    return None

route = []
position = get_position('^', grid)
#find initial turn
facing = 'u'
if grid[(position[0]-1,position[1])] == '#':
    route.append('L')
    facing = 'l'
elif grid[(position[0]+1),position[1]] == '#':
    route.append('R')
    facing = 'r'

def spaces_around(position, grid):
    spaces = 0
    adj = [(-1,0),(1,0),(0,-1),(0,1)]
    for a in adj:
        if (position[0]+a[0], position[1]+a[1]) in grid and grid[(position[0]+a[0], position[1]+a[1])] == '.':
            spaces += 1
    return spaces

def step_forward(position, grid):
    if facing == 'u':
        diff = (0,-1)
    elif facing == 'd':
        diff = (0,1)
    elif facing == 'l':
        diff = (-1,0)
    elif facing == 'r':
        diff = (1,0)
    count = 0
    while position in grid and grid[position] != '.':
        count += 1
        position = (position[0]+diff[0],position[1]+diff[1])
    position = (position[0]-diff[0],position[1]-diff[1])
    return position,count-1

def which_way_to_turn(facing,position,grid):
    order = ['u','r','d','l']
    turn = ""
    order_pos = order.index(facing)
    if facing == 'u':
        compares = [(-1,0),(1,0)]
    elif facing == 'd':
        compares = [(1,0),(-1,0)]
    elif facing == 'l':
        compares = [(0,1),(0,-1)]
    elif facing == 'r':
        compares = [(0,-1),(0,1)]
    for c,a in enumerate(compares):
        if (position[0]+a[0], position[1]+a[1]) in grid and grid[(position[0]+a[0], position[1]+a[1])] == '#':
            if c == 0:
                turn = 'L'
                order_pos = order_pos - 1
            elif c == 1:
                turn = 'R'
                order_pos = order_pos + 1
    if order_pos < 0:
        order_pos = 3
    elif order_pos > 3:
        order_pos = 0
    return turn, order[order_pos]

while spaces_around(position, grid) < 3:
    position,steps_forward = step_forward(position,grid)
    route.append(str(steps_forward))
    turn, facing = which_way_to_turn(facing,position,grid)
    route.append(turn)
route.pop()

print("Route through scaffolding:",','.join(route))

# Examined by using eyeballs to generate these inputs:
# A,B,B,C,C,A,B,B,C,A
# R,4,R,12,R,10,L,12 = A
# L,12,R,4,R,12 = B
# L,12,L,8,R,10 = C

strings = ["A,B,B,C,C,A,B,B,C,A","R,4,R,12,R,10,L,12","L,12,R,4,R,12","L,12,L,8,R,10","n"]

string_being_entered = 0
string_chr_position = -1

def get_input_value():
    global string_chr_position
    global string_being_entered
    string_chr_position += 1
    if string_chr_position == len(strings[string_being_entered]):
        print("Finishing sending string:",strings[string_being_entered])
        string_being_entered += 1
        string_chr_position = -1
        return ord("\n")
    return ord(strings[string_being_entered][string_chr_position])

message = []
input_value = 0
position = 0
relative_base = 0
input_position = 0
program = copy.deepcopy(original_program)
program[0] = 2

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
        input_value = get_input_value()
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
            x = (program[program[position+1]])
        elif parameters[0] == '1':
            # print("4) Setting output to", program[position+1])
            x = (program[position+1])
        elif parameters[0] == '2':
            # print("4) Setting output to", program[relative_base+program[position+1]])
            x = (program[relative_base+program[position+1]])
        if x > 255:
            print("Answer to part two:", x)
        elif x == 10:
            print(''.join(message))
            message = []
        else:
            message.append(chr(x))
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
