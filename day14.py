
import math
import copy

filename="input/day14input.txt"
file=open(filename,"r")
file=file.readlines()

recipes = {}

for line in file:
    line = line.replace("\n","").replace(" => ", ", ")
    line = line.split(", ")
    output = line.pop()
    output = output.split(" ")
    output = (int(output[0]), output[1])
    inputs = []
    for l in line:
        l = l.split(" ")
        inputs.append((int(l[0]), l[1]))
    recipes[output] = inputs

#prioritization
prods_to_prioritize = []
prods = {0:['ORE']}
done = ['ORE']
for rci, rco in recipes.items():
    if rci[1] not in prods_to_prioritize:
        prods_to_prioritize.append(rci[1])
    for r in rco:
        if r[1] not in prods_to_prioritize:
            prods_to_prioritize.append(r[1])
prods_to_prioritize.remove('ORE')
prods_to_prioritize.remove('FUEL')
priority = 1
for rci, rco in recipes.items():
    for item in rco:
        if item[1] == 'ORE':
            if rci[1] not in prods:
                if priority not in prods:
                    prods[priority] = [rci[1]]
                else:
                    prods[priority].append(rci[1])
                done.append(rci[1])
                prods_to_prioritize.remove(rci[1])
while len(prods_to_prioritize) > 0:
    priority += 1
    d = done
    ptp = prods_to_prioritize
    for rci, rco in recipes.items():
        if rci[1] in ptp:
            add = True
            for item in rco:
                if item[1] not in d:
                    add = False
            if add == True:
                if priority not in prods:
                    prods[priority] = [rci[1]]
                else:
                    prods[priority].append(rci[1])
                d.append(rci[1])
                ptp.remove(rci[1])
    done = d
    prods_to_prioritize = ptp

max_prods = 0
for k in prods:
    if k > max_prods:
        max_prods = k

ordering = []
for i in range(max_prods+1):
    for a in prods[i]:
        ordering.append(a)

proc = ordering.pop()
requirements = copy.deepcopy(recipes[(1, 'FUEL')])
next_round = []

def req_rearrange(reqs):
    items = {}
    outp = []
    for r in reqs:
        if r[1] not in items:
            items[r[1]] = r[0]
        else:
            items[r[1]] += r[0]
    for k,v in items.items():
        outp.append((v,k))
    return outp

while (len(requirements) > 1 or len(next_round) > 0) and proc != 'ORE':
    nothing_done = True
    while len(requirements) > 0: 
        r = requirements.pop()
        no_changes = True
        if r[1] == 'ORE':
            next_round.insert(0,r)
        else:
            for rci, rco in recipes.items():
                if rci[1] == r[1] and r[1] == proc:
                    if r[0] > rci[0]:
                        repeats = math.ceil(r[0]/rci[0])
                    else:
                        repeats = 1
                    for item in rco:
                        next_round.append((item[0]*repeats, item[1]))
                    no_changes = False
                    nothing_done = False
            if no_changes:
                next_round.append(r)
    # print (nothing_done)
    if nothing_done:
        proc = ordering.pop()
    #     print("Moving on to:", proc)
    # print (next_round)
    requirements = next_round
    next_round = []
    requirements = req_rearrange(requirements)
    # print(requirements)

print("Answer for part one:", requirements[0][0])

ore_available = 1000000000000


#prioritization
prods_to_prioritize = []
prods = {0:['ORE']}
done = ['ORE']
for rci, rco in recipes.items():
    if rci[1] not in prods_to_prioritize:
        prods_to_prioritize.append(rci[1])
    for r in rco:
        if r[1] not in prods_to_prioritize:
            prods_to_prioritize.append(r[1])
prods_to_prioritize.remove('ORE')
prods_to_prioritize.remove('FUEL')
priority = 1
for rci, rco in recipes.items():
    for item in rco:
        if item[1] == 'ORE':
            if rci[1] not in prods:
                if priority not in prods:
                    prods[priority] = [rci[1]]
                else:
                    prods[priority].append(rci[1])
                done.append(rci[1])
                prods_to_prioritize.remove(rci[1])
while len(prods_to_prioritize) > 0:
    priority += 1
    d = done
    ptp = prods_to_prioritize
    for rci, rco in recipes.items():
        if rci[1] in ptp:
            add = True
            for item in rco:
                if item[1] not in d:
                    add = False
            if add == True:
                if priority not in prods:
                    prods[priority] = [rci[1]]
                else:
                    prods[priority].append(rci[1])
                d.append(rci[1])
                ptp.remove(rci[1])
    done = d
    prods_to_prioritize = ptp

max_prods = 0
for k in prods:
    if k > max_prods:
        max_prods = k

ordering = []
for i in range(max_prods+1):
    for a in prods[i]:
        ordering.append(a)

proc = ordering.pop()
requirements = copy.deepcopy(recipes[(1, 'FUEL')])
next_round = []

while (len(requirements) > 1 or len(next_round) > 0) and proc != 'ORE':
    nothing_done = True
    while len(requirements) > 0: 
        r = requirements.pop()
        no_changes = True
        if r[1] == 'ORE':
            next_round.insert(0,r)
        else:
            for rci, rco in recipes.items():
                if rci[1] == r[1] and r[1] == proc:
                    repeats = (r[0]/rci[0])
                    for item in rco:
                        next_round.append((item[0]*repeats, item[1]))
                    no_changes = False
                    nothing_done = False
            if no_changes:
                next_round.append(r)
    # print (nothing_done)
    if nothing_done:
        proc = ordering.pop()
    #     print("Moving on to:", proc)
    # print (next_round)
    requirements = next_round
    next_round = []
    requirements = req_rearrange(requirements)

s = requirements[0][0]
print("Answer for part two:", math.floor(ore_available/s))
if math.modf(ore_available/s)[0] < 0.05:
    print("Answer for part two might be", math.floor(ore_available/s)-1, "due to rounding.")