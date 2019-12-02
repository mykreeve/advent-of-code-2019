import copy

filename="input/day2input.txt"
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

program[1] = 12
program[2] = 2

# print (program)
position = 0
while program[position] != 99:
    # print ("Executing:", program[position], ",", program[position+1], ",", program[position+2], ",", program[position+3], ",")
    # print ("Executing:", program[position], ",", program[program[position+1]], ",", program[program[position+2]], ",", program[program[position+3]], ",")
    if program[position] == 1:
        # print ("Storing:", (program[program[position+1]] + program[program[position+2]] ), "in", program[program[position+3]])
        program[program[position+3]] = program[program[position+1]] + program[program[position+2]] 
        position += 4
    elif program[position] == 2:
        # print ("Storing:", (program[program[position+1]] * program[program[position+2]] ), "in", program[program[position+3]])
        program[program[position+3]] = program[program[position+1]] * program[program[position+2]] 
        position += 4
    else:
        print ("Problem with execution:", program[position])
    # print(program)
print("Answer for part one:", program[0])


for a in range(100):
    for b in range(100):
        program = copy.deepcopy(original_program)
        program[1] = a
        program[2] = b
        position = 0
        while program[position] != 99:
            # print ("Executing:", program[position], ",", program[position+1], ",", program[position+2], ",", program[position+3], ",")
            # print ("Executing:", program[position], ",", program[program[position+1]], ",", program[program[position+2]], ",", program[program[position+3]], ",")
            if program[position] == 1:
                # print ("Storing:", (program[program[position+1]] + program[program[position+2]] ), "in", program[program[position+3]])
                program[program[position+3]] = program[program[position+1]] + program[program[position+2]] 
                position += 4
            elif program[position] == 2:
                # print ("Storing:", (program[program[position+1]] * program[program[position+2]] ), "in", program[program[position+3]])
                program[program[position+3]] = program[program[position+1]] * program[program[position+2]] 
                position += 4
            else:
                print ("Problem with execution:", program[position])
            # print(program)
        # print (a,b, program[0])
        if program[0] == 19690720:
            print ("Answer to part two:", (a*100)+b)
            break