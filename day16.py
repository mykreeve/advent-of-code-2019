import copy

filename="input/day16input.txt"
file=open(filename,"r")
file=file.readlines()

for line in file:
    line = line.replace("\n","")
    value = list(line)

original_value = copy.deepcopy(value)

length = (len(value))

def generate_phase(length, generation):
    phase = []
    phase_position = 0
    generation_position = 0
    phase_values = [0,1,0,-1]
    for i in range(length+1):
        phase.append(phase_values[phase_position])
        generation_position  += 1
        if generation_position == generation:
            phase_position += 1
            if phase_position > len(phase_values)-1:
                phase_position = 0
            generation_position = 0
    del phase[0]
    return phase

count = 0
while count < 100:
    output = []
    for a in range(length):
        output_value = 0
        phase = generate_phase(length,a+1)
        for n in range(length):
            output_value += int(value[n])*phase[n]
        output.append(str(output_value)[-1:])
    value = output
    count += 1
    if count%10 == 0:
        print("Working... " + str(count) + "%")

print("Answer for part one: ", end="")
for a in range(0,8):
    print(value[a],end="")
print("")

value = copy.deepcopy(original_value)

offset = ''
for a in range(0,7):
    offset += value[a]
offset = int(offset)

new_value = []
for a in range(10000):
    new_value.extend(value)

new_value = new_value[offset:]
length = len(new_value)
new = []
for n in new_value:
    new.append(int(n))
new_value = new

count = 0

while count < 100:
    output = []
    output_value = sum(new_value)
    for a in range(0,length):
        output.append(int(str(output_value)[-1:]))
        output_value = output_value - new_value[a]
    new_value = output
    count += 1
    if count%10 == 0:
        print("Working... " + str(count) + "%")

print("Answer for part two: ", end="")
for a in range(0,8):
    print(new_value[a],end="")
print("")