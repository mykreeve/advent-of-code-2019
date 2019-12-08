import copy
from itertools import permutations

filename="input/day7input.txt"
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

best_output = 0

phase_permutations = permutations([0,1,2,3,4])
for phase_settings in phase_permutations:
    input_signal = 0

    for p in phase_settings:
        inputs = [p,input_signal]
        position = 0
        input_position = 0
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
                    program[program[position+1]] = inputs[input_position]
                elif parameters[0] == '1':
                    program[position+1] = inputs[input_position]
                position += 2
                input_position += 1
            elif opcode == 4:
                if parameters[0] == '0':
                    input_signal = program[program[position+1]]
                elif parameters[0] == '1':
                    input_signal = program[position+1]
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

    # print("Output for:", phase_settings, '=', input_signal)
    if input_signal > best_output:
        best_output = input_signal
        best_perm = phase_settings

print ("Answer for part one:", best_output, "from", best_perm)


program = copy.deepcopy(original_program)

best_output = 0

phase_permutations = permutations([5,6,7,8,9])
for phase_settings in phase_permutations:
    input_signal = 0
    positions = {0:0, 1:0, 2:0, 3:0, 4:0}
    input_positions = {0:0, 1:0, 2:0, 3:0, 4:0}
    programs = {0: copy.deepcopy(original_program), 1:copy.deepcopy(original_program), 2:copy.deepcopy(original_program), 3:copy.deepcopy(original_program), 4:copy.deepcopy(original_program)}
    amp_running = 0

    inputs = [phase_settings[amp_running],input_signal]
    position = positions[amp_running]

    while programs[amp_running][positions[amp_running]] != 99 and amp_running < 5:
        opcode = int(str(programs[amp_running][positions[amp_running]])[-2:])
        parameters = list(str(programs[amp_running][positions[amp_running]])[:-2])
        while len(parameters)<3:
            parameters.insert(0,'0')
        parameters.reverse()
        if opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8:
            if parameters[0] == '0':
                a = programs[amp_running][programs[amp_running][positions[amp_running]+1]]
            elif parameters[0] == '1':
                a = programs[amp_running][positions[amp_running]+1]
            if parameters[1] == '0':
                b = programs[amp_running][programs[amp_running][positions[amp_running]+2]]
            elif parameters[1] == '1':
                b = programs[amp_running][positions[amp_running]+2]
        if opcode == 7 or opcode == 8:
            if parameters[2] == '0':
                c = programs[amp_running][positions[amp_running]+3]
            elif parameters[2] == '1':
                c = positions[amp_running]+3

        if opcode == 1:
            if parameters[2] == '0':
                programs[amp_running][programs[amp_running][positions[amp_running]+3]] = (a + b)
            elif parameters[2] == '1':
                programs[amp_running][positions[amp_running]+3] = (a + b)
            positions[amp_running] += 4
        elif opcode == 2:
            if parameters[2] == '0':
                programs[amp_running][programs[amp_running][positions[amp_running]+3]] = (a * b)
            elif parameters[2] == '1':
                programs[amp_running][positions[amp_running]+3] = (a * b)
            positions[amp_running] += 4
        elif opcode == 3:
            if parameters[0] == '0':
                programs[amp_running][programs[amp_running][positions[amp_running]+1]] = inputs[input_positions[amp_running]]
            elif parameters[0] == '1':
                programs[amp_running][positions[amp_running]+1] = inputs[input_positions[amp_running]]
            positions[amp_running] += 2
            input_positions[amp_running] += 1
            if input_positions[amp_running] > 1:
                input_positions[amp_running] = 1
        elif opcode == 4:
            if parameters[0] == '0':
                input_signal = programs[amp_running][programs[amp_running][positions[amp_running]+1]] 
            elif parameters[0] == '1':
                input_signal = programs[amp_running][positions[amp_running]+1]
            positions[amp_running] = (positions[amp_running]+2)
            amp_running += 1
            if amp_running == 5:   
                amp_running = 0 
            inputs = [phase_settings[amp_running], input_signal]
        elif opcode == 5:
            if a != 0:
                positions[amp_running] = b
            else:
                positions[amp_running] += 3
        elif opcode == 6:
            if a == 0:
                positions[amp_running] = b
            else:
                positions[amp_running] += 3
        elif opcode == 7:
            if a < b:
                programs[amp_running][c] = 1
            else:
                programs[amp_running][c] = 0
            positions[amp_running] += 4
        elif opcode == 8:
            if a == b:
                programs[amp_running][c] = 1
            else:
                programs[amp_running][c] = 0
            positions[amp_running] += 4
        elif opcode == 99:
            print("Reached the end of amp:", amp_running)
            break
        else:
            print ("Problem with execution:", programs[amp_running][positions[amp_running]])

    # print("Output for:", phase_settings, '=', input_signal)
    if input_signal > best_output:
        best_output = input_signal
        best_perm = phase_settings

print ("Answer for part two:", best_output, "from", best_perm)
