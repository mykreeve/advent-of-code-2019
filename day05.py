import copy

filename="input/day5input.txt"
file=open(filename,"r")
file=file.readlines()

program = {}
position = 0

for line in file:
    line = line.replace("\n","").split(",")
    for n in line:
        program[position] = int(n)
        position += 1

original_program = copy.deepcopy(program)

x = 1
position = 0
last_output = 0

while program[position] != 99:

    opcode = int(str(program[position])[-2:])
    parameters = list(str(program[position])[:-2])
    while len(parameters)<3:
        parameters.insert(0,'0')
    parameters.reverse()
    if opcode == 1 or opcode == 2:
        if parameters[0] == '0':
            a = program[program[position+1]]
        elif parameters[0] == '1':
            a = program[position+1]
        if parameters[1] == '0':
            b = program[program[position+2]]
        elif parameters[1] == '1':
            b = program[position+2]

    if opcode == 1:
        if parameters[2] == '0':
            program[program[position+3]] = (a + b)
        elif parameters[2] == '1':
            program[position+3] = (a + b)
        position += 4
    elif opcode == 2:
        if parameters[2] == '0':
            program[program[position+3]] = (a * b)
        elif parameters[2] == '1':
            program[position+3] = (a * b)
        position += 4
    elif opcode == 3:
        if parameters[0] == '0':
            program[program[position+1]] = x
        elif parameters[0] == '1':
            program[position+1] = x
        position += 2
    elif opcode == 4:
        if parameters[0] == '0':
            # print(program[program[position+1]])
            last_output = program[program[position+1]]
        elif parameters[0] == '1':
            # print(program[position+1])
            last_output = program[position+1]
        position += 2
    else:
        print ("Problem with execution:", program[position])
print("Answer for part one:", last_output)

x = 5
position = 0
last_output = 0
program = copy.deepcopy(original_program)

while program[position] != 99:

    opcode = int(str(program[position])[-2:])
    parameters = list(str(program[position])[:-2])
    while len(parameters)<3:
        parameters.insert(0,'0')
    parameters.reverse()
    if opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8:
        if parameters[0] == '0':
            a = program[program[position+1]]
        elif parameters[0] == '1':
            a = program[position+1]
        if parameters[1] == '0':
            b = program[program[position+2]]
        elif parameters[1] == '1':
            b = program[position+2]
    if opcode == 7 or opcode == 8:
        if parameters[2] == '0':
            c = program[position+3]
        elif parameters[2] == '1':
            c = position+3

    if opcode == 1:
        if parameters[2] == '0':
            program[program[position+3]] = (a + b)
        elif parameters[2] == '1':
            program[position+3] = (a + b)
        position += 4
    elif opcode == 2:
        if parameters[2] == '0':
            program[program[position+3]] = (a * b)
        elif parameters[2] == '1':
            program[position+3] = (a * b)
        position += 4
    elif opcode == 3:
        if parameters[0] == '0':
            program[program[position+1]] = x
        elif parameters[0] == '1':
            program[position+1] = x
        position += 2
    elif opcode == 4:
        if parameters[0] == '0':
            # print(program[program[position+1]])
            last_output = program[program[position+1]]
        elif parameters[0] == '1':
            # print(program[position+1])
            last_output = program[position+1]
        position += 2
    elif opcode == 5:
        if a != 0:
            position = b
        else:
            position += 3
    elif opcode == 6:
        if a == 0:
            position = b
        else:
            position += 3
    elif opcode == 7:
        if a < b:
            program[c] = 1
        else:
            program[c] = 0
        position += 4
    elif opcode == 8:
        if a == b:
            program[c] = 1
        else:
            program[c] = 0
        position += 4
    else:
        print ("Problem with execution:", program[position])
print("Answer for part two:", last_output)