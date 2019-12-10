import math

filename="input/day10input.txt"
file=open(filename,"r")
file=file.readlines()

world = {}
y = 0
best = 0

for line in file:
    line = list(line.replace("\n",""))
    x = 0
    for char in line:
        world[(x,y)] = char
        x += 1
    y += 1

asteroids = []
for k,v in world.items():
    if v == '#':
        asteroids.append(k)

for a in asteroids:
    trajectories = []
    field = {}
    for b in asteroids:
        if a == b:
            pass
        else:
            xdist = b[0]-a[0]
            ydist = b[1]-a[1]
            if xdist == 0 and ydist < 0:
                direction = 0
            elif xdist == 0 and ydist > 0:
                direction = 180
            elif ydist == 0 and xdist > 0:
                direction = 90
            elif ydist == 0 and xdist < 0:
                direction = 270
            else:
                if xdist > 0 and ydist > 0:
                    direction = 90 + abs(math.degrees(math.atan(ydist/xdist)))
                elif xdist > 0 and ydist < 0:
                    direction = 90 + (math.degrees(math.atan(ydist/xdist)))
                elif xdist < 0 and ydist < 0:
                    direction = 270 + math.degrees(math.atan(ydist/xdist))
                elif xdist < 0 and ydist > 0:
                    direction = 270 - abs(math.degrees(math.atan(ydist/xdist)))
            distance = math.sqrt(xdist**2 + ydist**2)
            # print (a,b, xdist, ydist, direction, distance)
            trajectories.append((direction, distance, b))
            if str(direction) not in field:
                field[str(direction)] = [(distance, b)]
            else:
                field[str(direction)].append((distance, b))
    angles = []
    for t in trajectories:
        if t[0] not in angles:
            angles.append(t[0])
    if len(angles) > best:
        best = len(angles)
        angles.sort()
        best_angles = angles
        best_field = field

print("Answer for part one:", best)

removed = 0
while removed < 200:
    for a in best_angles:
        k = best_field[str(a)]
        k.sort()
        b = best_field[str(a)].pop(0)
        removed += 1
        if removed == 200:
            print("Answer to part two:", ((b[1][0] * 100) + b[1][1]))
        if len(best_field[str(a)]) == 0:
            del best_field[str(a)]