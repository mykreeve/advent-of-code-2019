import copy

filename="input/day23input.txt"
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
program = copy.deepcopy(original_program)

nics = {}

for a in range(50):
    p = copy.deepcopy(original_program)
    nics[a] = {'program':p, 'position': 0, 'relative_base': 0}

def run_nic(input_value, program,position,relative_base):
    outputs = []
    val_applied = False
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
            if val_applied:
                return (program, position,relative_base,outputs)
            val_applied = True
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
            outputs.append(x)
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

def check_queue_status(queue):
    for nic,q in queue.items():
        if len(q) != 0:
            return False
    return True


# initiate each nic
for a in range(50):
    program = nics[a]['program']
    position = nics[a]['position']
    relative_base = nics[a]['relative_base']
    program, position,relative_base,outputs = run_nic(a, program,position, relative_base)
    nics[a]['program'] = program
    nics[a]['position'] = position
    nics[a]['relative_base'] = relative_base

queue = {}
natx = 0
naty = 0
lastnaty = 0
display_part_one = True

# passing -1 to every nic
for a in range(50):
    program = nics[a]['program']
    position = nics[a]['position']
    relative_base = nics[a]['relative_base']
    program, position,relative_base,outputs = run_nic(-1,program,position, relative_base)
    nics[a]['program'] = program
    nics[a]['position'] = position
    nics[a]['relative_base'] = relative_base
    if outputs:
        while len(outputs) >= 3:
            proc_output = []
            proc_output.append(outputs.pop(0))
            proc_output.append(outputs.pop(0))
            proc_output.append(outputs.pop(0))
            if proc_output[0] == 255:
                if display_part_one:
                    print ("Answer to part one:", proc_output[2])
                    display_part_one = False
                natx = proc_output[1]
                naty = proc_output[2]
            else:
                if proc_output[0] not in queue:
                    queue[proc_output[0]] = [[proc_output[1],proc_output[2]]]
                else:
                    queue[proc_output[0]].append([proc_output[1],proc_output[2]])

item_to_process = []

while True:
    idle = 0
    for a in range(50):
        if a in queue and len(queue[a]) > 0:
            item_to_process = queue[a].pop(0)
            program = nics[a]['program']
            position = nics[a]['position']
            relative_base = nics[a]['relative_base']
            program, position,relative_base,outputs = run_nic(item_to_process[0],program,position, relative_base)
            program, position,relative_base,outputs = run_nic(item_to_process[1],program,position, relative_base)
            nics[a]['program'] = program
            nics[a]['position'] = position
            nics[a]['relative_base'] = relative_base
            if outputs:
                while len(outputs) >= 3:
                    proc_output = []
                    proc_output.append(outputs.pop(0))
                    proc_output.append(outputs.pop(0))
                    proc_output.append(outputs.pop(0))
                    if proc_output[0] == 255:
                        if display_part_one:
                            print ("Answer to part one:", proc_output[2])
                            display_part_one = False
                        natx = proc_output[1]
                        naty = proc_output[2]
                    else:
                        if proc_output[0] not in queue:
                            queue[proc_output[0]] = [[proc_output[1],proc_output[2]]]
                        else:
                            queue[proc_output[0]].append([proc_output[1],proc_output[2]])
        else:
            program = nics[a]['program']
            position = nics[a]['position']
            relative_base = nics[a]['relative_base']
            program, position,relative_base,outputs = run_nic(-1,program,position, relative_base)
            nics[a]['program'] = program
            nics[a]['position'] = position
            nics[a]['relative_base'] = relative_base
            if outputs:
                while len(outputs) >= 3:
                    proc_output = []
                    proc_output.append(outputs.pop(0))
                    proc_output.append(outputs.pop(0))
                    proc_output.append(outputs.pop(0))
                    if proc_output[0] == 255:
                        if display_part_one:
                            print ("Answer to part one:", proc_output[2])
                            display_part_one = False
                        natx = proc_output[1]
                        naty = proc_output[2]
                    else:
                        if proc_output[0] not in queue:
                            queue[proc_output[0]] = [[proc_output[1],proc_output[2]]]
                        else:
                            queue[proc_output[0]].append([proc_output[1],proc_output[2]])
            else:
                idle += 1
    if idle == 50:
        if naty == lastnaty:
            print("Answer to part two:", naty)
            exit()
        lastnaty = naty
        if 0 in queue:
            queue[0].append([natx,naty])
        else:
            queue[0] = [[natx,naty]]