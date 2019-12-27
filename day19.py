import copy

filename="input/day19input.txt"
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
grid = {}
position = 0
relative_base = 0
input_position = 0
program = copy.deepcopy(original_program)

for y in range(50):
    for x in range(50):
        xused = False
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
                if xused:
                    input_value = y
                else:
                    input_value = x
                    xused = True
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
                grid[(x,y)] = output
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

count = 0
for y in range(maxy+1):
    for x in range(maxx+1):
        print (grid[(x,y)],end="")
        if grid[(x,y)] == 1:
            count += 1
    print("")


print ("Answer for part one:", count)

# This value was arrived at by testing higher values, and working back.
test_value = 975

def do_test(test_value):
    global grid
    grid = {}
    for y in range(test_value,test_value+100, 99):
        # print("Analysing y:", y)
        xstart = True
        xend = True
        for x in range(int(y/2),y):
            if (xstart or xend):
                xused = False
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
                        if xused:
                            input_value = y
                        else:
                            input_value = x
                            xused = True
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
                        if output == 1:
                            grid[(x,y)] = output
                            if xstart:
                                # print(str(x) + " ", end="")
                                xstartval = x
                                xstart = False
                        if output == 0:
                            if xend and not xstart:
                                xendval = x
                                # print("to",x, " - width:", xendval-xstartval)
                                xend = False
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

while True:
    print("Trying value:", test_value)
    do_test(test_value)
    lowstartyval = 0
    y = test_value+99
    xstart = True
    for x in range(int(y/2),y):
        if xstart:
            if (x,y) in grid:
                if grid[(x,y)] == 1:
                    xstart = False
                    if lowstartyval == 0:
                        lowstartyval = x

    if (lowstartyval,test_value) in grid and grid[(lowstartyval,test_value)] == 1:
        if (lowstartyval+99,test_value) in grid and grid[(lowstartyval+99,test_value)] == 1:
            print("Success with test value:", test_value)
            print("Answer to part two:", lowstartyval*10000 + test_value)
            exit()
    test_value += 1
