import copy

filename="input/day21input.txt"
file=open(filename,"r")
file=file.readlines()

program = {}
position = 0

for line in file:
    line = line.replace("\n","").split(",")
    for n in line:
        program[position] = int(n)
        position += 1

for n in range(25000):
    program[position] = 0
    position += 1

original_program = copy.deepcopy(program)

input_value = 0
position = 0
relative_base = 0
input_position = 0
program = copy.deepcopy(original_program)

strings = ["OR A T","OR B J","NOT C J","AND C T","NOT T J","AND D J","WALK"]

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
            print("Answer to part one:", x)
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




strings = ["NOT F J","OR E J","OR H J","AND D J","NOT C T","AND T J","NOT D T","OR B T","OR E T","NOT T T","OR T J","NOT A T","OR T J","RUN"]

string_being_entered = 0
string_chr_position = -1

def get_input_value_pt2():
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
        input_value = get_input_value_pt2()
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
