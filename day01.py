import math

filename="input/day1input.txt"
file=open(filename,"r")
file=file.readlines()

inputs = []
for line in file:
    line = line.strip().replace("\n","")
    inputs.append(int(line))

cum_total = 0

def reqd_fuel(num):
    return (math.floor(num/3.0)-2)


cum_total = 0

for i in inputs:
    cum_total += (math.floor(i/3.0)-2)

print ("Answer for part one:", cum_total)

cum_total = 0

for i in inputs:
    this_total = reqd_fuel(i)
    temp_total = reqd_fuel(i)
    while reqd_fuel(temp_total) > 0:
        this_total += reqd_fuel(temp_total)
        temp_total = reqd_fuel(temp_total)
    cum_total += this_total

print ("Answer for part two:", cum_total)