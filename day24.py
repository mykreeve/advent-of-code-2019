filename="input/day24input.txt"
file=open(filename,"r")
file=file.readlines()

field = {}
recursive_field = {}

y = 0
for line in file:
    x = 0
    line = line.replace("\n","")
    for char in list(line):
        field[(x,y)] = char
        recursive_field[(0,x,y)] = char
        x += 1
    y += 1
recursive_field[(0,2,2)] = "?"

maxx = x
maxy = y
visited = []
generation = 0

def print_field(field):
    for y in range(maxy):
        for x in range(maxx):
            print(field[(x,y)], end="")
        print("")

def print_field_layer(field,layer):
    for y in range(maxy):
        for x in range(maxx):
            print(field[(layer,x,y)], end="")
        print("")

def biodiversity_calc(field):
    bio = 0
    val = 1
    for y in range(maxy):
        for x in range(maxx):
            if field[(x,y)] == '#':
                bio += val
            val = val * 2
    return bio

def advance_generation(field):
    new_field = {}
    adj = [(-1,0),(1,0),(0,-1),(0,1)]
    for y in range(maxy):
        for x in range(maxx):
            neighbours = 0
            for a in adj:
                if (x+a[0],y+a[1]) in field and field[(x+a[0],y+a[1])] == '#':
                    neighbours += 1
            if neighbours != 1 and field[(x,y)] == '#':
                new_field[(x,y)] = '.'
            elif (neighbours == 1 or neighbours == 2) and field[(x,y)] == '.':
                new_field[(x,y)] = '#'
            else:
                new_field[(x,y)] = field[(x,y)]
    return new_field

def advance_recursive_generation(field):
    new_field = {}
    lowest_field = 0
    highest_field = 0
    adj = [(-1,0),(1,0),(0,-1),(0,1)]
    for key,val in field.items():
        if key[0] < lowest_field:
            lowest_field = key[0]
        if key[0] > highest_field:
            highest_field = key[0]
    for layer in range(lowest_field-1,highest_field+2):
        # print("Layer:", layer)
        for y in range(maxy):
            for x in range(maxx):
                neighbours = 0
                for a in adj:
                    if (layer,x+a[0],y+a[1]) in field and field[(layer,x+a[0],y+a[1])] == '#':
                        neighbours += 1
                if x == 0:
                    if (layer-1,1,2) in field and field[(layer-1,1,2)] == '#':
                        neighbours += 1
                if y == 0:
                    if (layer-1,2,1) in field and field[(layer-1,2,1)] == '#':
                        neighbours += 1
                if x == maxx-1:
                    if (layer-1,3,2) in field and field[(layer-1,3,2)] == '#':
                        neighbours += 1
                if y == maxy-1:
                    if (layer-1,2,3) in field and field[(layer-1,2,3)] == '#':
                        neighbours += 1
                if x == 2 and y == 1:
                    for a in range(maxx):
                        if (layer+1,a,0) in field and field[(layer+1,a,0)] == '#':
                            neighbours += 1
                if x == 2 and y == 3:
                    for a in range(maxx):
                        if (layer+1,a,maxy-1) in field and field[(layer+1,a,maxy-1)] == '#':
                            neighbours += 1
                if x == 1 and y == 2:
                    for a in range(maxy):
                        if (layer+1,0,a) in field and field[(layer+1,0,a)] == '#':
                            neighbours += 1
                if x == 3 and y == 2:
                    for a in range(maxy):
                        if (layer+1,maxx-1,a) in field and field[(layer+1,maxx-1,a)] == '#':
                            neighbours += 1
                if (layer,x,y) not in field:
                    field[(layer,x,y)] = '.'
                if neighbours != 1 and field[(layer,x,y)] == '#':
                    new_field[(layer,x,y)] = '.'
                elif (neighbours == 1 or neighbours == 2) and field[(layer,x,y)] == '.':
                    new_field[(layer,x,y)] = '#'
                else:
                    new_field[(layer,x,y)] = field[(layer,x,y)]
        #         print(neighbours,end="")
        #     print("")
        # print("")
        new_field[(layer,2,2)] = "?"
    return new_field

dont_stop = True
while dont_stop:
    bio = biodiversity_calc(field)
    if bio in visited:
        dont_stop = False
    visited.append(bio)
    field = advance_generation(field)
    generation += 1
print("Answer for part one:",bio)

generation = 0
while generation < 200:
    # lowest_field = 0
    # highest_field = 0
    # for key,val in recursive_field.items():
    #     if key[0] < lowest_field:
    #         lowest_field = key[0]
    #     if key[0] > highest_field:
    #         highest_field = key[0]
    # print("Generation:",generation)
    # for layer in range(lowest_field,highest_field+1):
    #     print("Layer:", layer)
    #     print_field_layer(recursive_field,layer)
    recursive_field = advance_recursive_generation(recursive_field)
    generation += 1

count = 0
for k,v in recursive_field.items():
    if v == '#':
        count += 1

print("Answer for part two:",count)