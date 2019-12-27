import copy
import re
import heapq

filename="input/day20input.txt"
file=open(filename,"r")
file=file.readlines()

grid = {}
portals = {}
portal_layer = {}
portal_locations = []
portal_lookup = {}
visited = []

maxx = 0
y = 0
for line in file:
    line = line.replace("\n","")
    values = list(line)
    x = 0
    for v in values:
        grid[(x,y)] = v
        x += 1
    maxx = x
    y += 1
maxy = y

def add_to_portals(label,location,layer):
    if label not in portals:
        portals[label] = [location]
    else:
        portals[label].append(location)
    portal_locations.append(location)
    portal_lookup[location] = label
    portal_layer[location] = layer

for k,v in grid.items():
    re_find = re.findall("([A-Z])", v)
    if re_find:
        #test horizontal
        if (k[0]+1,k[1]) in grid:
            h = grid[(k[0]+1,k[1])] 
            re_find2 = re.findall("([A-Z])", h)
            if re_find2:
                if (k[0]-1,k[1]) in grid:
                    if grid[(k[0]-1,k[1])] == '.':
                        if k[0]-1 == maxx-3:
                            add_to_portals(v+h, (k[0]-1,k[1]), "Outer")
                        else:
                            add_to_portals(v+h, (k[0]-1,k[1]), "Inner")
                if (k[0]+2,k[1]) in grid:
                    if grid[(k[0]+2,k[1])] == '.':
                        if k[0]+2 == 2:
                            add_to_portals(v+h, (k[0]+2,k[1]), "Outer")
                        else:
                            add_to_portals(v+h, (k[0]+2,k[1]), "Inner")
        #test vertical
        if (k[0],k[1]+1) in grid:
            h = grid[(k[0],k[1]+1)] 
            re_find2 = re.findall("([A-Z])", h)
            if re_find2:
                if (k[0],k[1]-1) in grid:
                    if grid[(k[0],k[1]-1)] == '.':
                        if k[1]-1 == maxy-3:
                            add_to_portals(v+h, (k[0],k[1]-1),"Outer")
                        else:
                            add_to_portals(v+h, (k[0],k[1]-1),"Inner")
                if (k[0],k[1]+2) in grid:
                    if grid[(k[0],k[1]+2)] == '.':
                        if k[1]+2 == 2:
                            add_to_portals(v+h, (k[0],k[1]+2),"Outer")
                        else:
                            add_to_portals(v+h, (k[0],k[1]+2),"Inner")


def find_options(time,position):
    opts = []
    alt_loc = None
    adj = [(-1,0),(1,0),(0,-1),(0,1)]
    for a in adj:
        if grid[(position[0]+a[0],position[1]+a[1])] == '.' and (position[0]+a[0],position[1]+a[1]) not in visited:
            opts.append((time+1,(position[0]+a[0],position[1]+a[1])))
    if position in portal_locations:
        portal = portal_lookup[position]
        ends = portals[portal]
        for e in ends:
            if e != position:
                alt_loc = e
        if alt_loc and alt_loc not in visited:
            opts.append((time+1,alt_loc))
    return opts

added_to_queue = {}

def find_options_layer(time,position,layer):
    opts = []
    alt_loc = None
    adj = [(-1,0),(1,0),(0,-1),(0,1)]
    for a in adj:
        if grid[(position[0]+a[0],position[1]+a[1])] == '.':
            if ((position[0]+a[0],position[1]+a[1]), layer) in added_to_queue:
                if added_to_queue[((position[0]+a[0],position[1]+a[1]), layer)] > time+1:
                    queue.remove((layer, added_to_queue[((position[0]+a[0],position[1]+a[1]), layer)], position[1]+a[1]))
                    added_to_queue[((position[0]+a[0],position[1]+a[1]), layer)] = time+1
                    opts.append((layer, time+1,(position[0]+a[0],position[1]+a[1])))
            else:
                added_to_queue[((position[0]+a[0],position[1]+a[1]), layer)] = time+1
                opts.append((layer, time+1,(position[0]+a[0],position[1]+a[1])))
    if position in portal_locations:
        portal = portal_lookup[position]
        layer_situation = portal_layer[position]
        ends = portals[portal]
        for e in ends:
            if e != position:
                alt_loc = e
        if alt_loc:
            if layer_situation == "Outer" and layer-1 >= 0:
                if (alt_loc,layer-1) not in visited:
                    opts.append((layer-1,time+1,alt_loc))
            if layer_situation == "Inner":
                if (alt_loc,layer+1) not in visited:
                    opts.append((layer+1,time+1,alt_loc))
    return opts

time = 0
layer = 0
position = portals['AA'][0]
queue = find_options(time,position)

while len(queue) > 0:
    time, position = heapq.heappop(queue)
    visited.append(position)
    if position == portals['ZZ'][0]:
        print("Answer to part one:",time)
    opts = find_options(time,position)
    for o in opts:
        heapq.heappush(queue, o)

time = 0
layer = 0
visited = []
position = portals['AA'][0]
queue = find_options_layer(time,position,layer)

while len(queue) > 0:
    layer, time, position = heapq.heappop(queue)
    visited.append((position,layer))
    if position == portals['ZZ'][0] and layer == 0:
        print("Answer to part two:",time)
        exit()
    opts = find_options_layer(time,position,layer)
    for o in opts:
        heapq.heappush(queue, o)