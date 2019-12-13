import copy

filename="input/day13input.txt"
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

layout = {}

input_value = 0
outputs = []
position = 0
relative_base = 0
input_position = 0
program = copy.deepcopy(original_program)

def do_action(o):
    layout[(o[0],o[1])] = o[2]

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
        if len(outputs) == 3:
            do_action(outputs)
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

minx = 0
maxx = 0
miny = 0
maxy = 0
for l in layout:
    if l[0] > maxx:
        maxx = l[0]
    if l[0] < minx:
        minx = l[0]
    if l[1] > maxy:
        maxy = l[0]
    if l[1] < miny:
        miny = l[0]

count = 0

for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
        ch = {0:' ', 1:'#', 2:'*', 3:'_', 4:'.'}
        # print(ch[layout[(x,y)]], end="")
        if layout[(x,y)] == 2:
            count += 1
    # print("")

print ("Answer for part one:", count)



layout = {}

inputs = []
outputs = []
position = 0
score = 0
relative_base = 0
input_position = 0
ball_position = None
bat_position = None
program = copy.deepcopy(original_program)
program[0] = 2

def do_action_pt2(o):
    global ball_position
    global bat_position
    global score
    if o[0] == -1:
        score = o[2]
    else:
        layout[(o[0],o[1])] = o[2]
        if o[2] == 4:
            ball_position = (o[0],o[1])
        if o[2] == 3:
            bat_position = (o[0],o[1])

def get_direction():
    global ball_position
    global bat_position
    if len(inputs) < 2:
        inputs.append(0)
    else:
        if (ball_position[0] < bat_position[0]):
            inputs.append(-1)
        elif (ball_position[0] > bat_position[0]):
            inputs.append(1)
        else:
            inputs.append(0)

def print_screen():
    pass
    # === If you want to see the gameplay, restore these lines ===
    # print("Score:", score)
    # for y in range(miny, maxy+1):
    #     for x in range(minx, maxx+1):
    #         ch = {0:' ', 1:'#', 2:'*', 3:'_', 4:'.'}
    #         print(ch[layout[(x,y)]], end="")
    #     print("")

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
        get_direction()
        if parameters[0] == '0':
            program[program[position+1]] = inputs[input_position]
            # print("3) Setting position", program[position+1], "to", x)
        elif parameters[0] == '1':
            program[position+1] = inputs[input_position]
            # print("3) Setting position", (position+1), "to", x)
        elif parameters[0] == '2':
            program[relative_base+program[position+1]] = inputs[input_position]
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
        if len(outputs) == 3:
            do_action_pt2(outputs)
            outputs = []
            if len(layout) == 735:
                print_screen()
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

print ("Answer for part two:", score)