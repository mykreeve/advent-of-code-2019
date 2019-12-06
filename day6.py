filename="input/day6input.txt"
file=open(filename,"r")
file=file.readlines()

objects = {}
for line in file:
    line = line.replace("\n","").split(")")
    objects[line[1]] =  line[0] 


tot_steps = 0
loc = ''
for k,v in objects.items():
    loc = v
    steps = 1
    while loc != 'COM':
        loc = objects[loc]
        steps += 1
    tot_steps += steps
print('Answer to part one:', tot_steps)

start = objects['YOU']
end = objects['SAN']

route_from_start = []
loc = start
while loc != 'COM':
    loc = objects[loc]
    route_from_start.append(loc)


route_from_end = []
loc = end
while loc != 'COM':
    loc = objects[loc]
    route_from_end.append(loc)

for a in route_from_start:
    if a in route_from_end:
        steps = route_from_start.index(a) + 1 + route_from_end.index(a) + 1
        print("Answer for part two:", steps)
        break