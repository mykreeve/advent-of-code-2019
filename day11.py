import copy

filename="input/day11input.txt"
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
facing = 'U'

input_value = 0
outputs = []
position = 0
relative_base = 0
input_position = 0
program = copy.deepcopy(original_program)

def do_paint(val):
    global surface_position
    global facing
    surface[surface_position] = val[0]
    xpos, ypos = surface_position
    if facing == 'U' and val[1] == 0:
        facing = 'L'
        xpos -= 1
    elif facing == 'U' and val[1] == 1:
        facing = 'R'
        xpos += 1
    elif facing == 'R' and val[1] == 0:
        facing = 'U'
        ypos -= 1
    elif facing == 'R' and val[1] == 1:
        facing = 'D'
        ypos += 1
    elif facing == 'D' and val[1] == 0:
        facing = 'R'
        xpos += 1
    elif facing == 'D' and val[1] == 1:
        facing = 'L'
        xpos -= 1
    elif facing == 'L' and val[1] == 0:
        facing = 'D'
        ypos += 1
    elif facing == 'L' and val[1] == 1:
        facing = 'U'
        ypos -= 1
    # print("Old position:", surface_position, "coloured", val[0])
    surface_position = (xpos, ypos)
    # print("New position:", surface_position, "facing", facing)
    if surface_position not in surface:
        return 0
    else:
        return surface[surface_position]

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
            outputs.append(program[program[position+1]])
        elif parameters[0] == '1':
            # print("4) Setting output to", program[position+1])
            outputs.append(program[position+1])
        elif parameters[0] == '2':
            # print("4) Setting output to", program[relative_base+program[position+1]])
            outputs.append(program[relative_base+program[position+1]])
        if len(outputs) == 2:
            input_value = do_paint(outputs)
            outputs = []
            # Do a thing with outputs
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



surface = {}
surface_position = (0,0)
facing = 'U'

input_value = 1
outputs = []
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
            outputs.append(program[program[position+1]])
        elif parameters[0] == '1':
            # print("4) Setting output to", program[position+1])
            outputs.append(program[position+1])
        elif parameters[0] == '2':
            # print("4) Setting output to", program[relative_base+program[position+1]])
            outputs.append(program[relative_base+program[position+1]])
        if len(outputs) == 2:
            input_value = do_paint(outputs)
            outputs = []
            # Do a thing with outputs
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

miny = 0
maxy = 0
minx = 0
maxx = 0
for k,v in surface.items():
    x,y = k
    if x < minx:
        minx = x
    if x > maxx:
        maxx = x
    if y < miny:
        miny = y
    if y > maxy:
        maxy = y
# print ("Range=(", minx,miny,") to (", maxx,maxy,")")

print ("Answer for part two:")
for b in range(miny,maxy+1):
    for a in range(minx,maxx+1):
        if (a,b) in surface:
            if surface[(a,b)] == 1:
                print (u"\u2588", end='')
            else:
                print(' ', end="")
        else:
            print (' ',end='')
    print('')