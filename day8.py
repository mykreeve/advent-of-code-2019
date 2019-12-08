filename="input/day8input.txt"
file=open(filename,"r")
file=file.readlines()

picture = {}
proc_picture = {}

file = list(file[0].replace("\n",""))

columns = 25
rows = 6

layer = 0
row = 0
column = 0

for c in file:
    picture[(layer, row, column)] = c
    if c != '2' and (row,column) not in proc_picture:
        proc_picture[(row,column)] = c

    column += 1
    if column == columns:
        column = 0
        row += 1
    if row == rows:
        row = 0
        layer += 1

least_count = 9999999
least_layer = 0

for m in range(layer):
    count = 0
    for k,v in picture.items():
        if k[0] == m:
            if v == '0':
                count += 1
    if count < least_count:
        least_count = count
        least_layer = m

count_1s = 0
count_2s = 0

for k,v in picture.items():
    if k[0] == least_layer:
        if v == '1':
            count_1s += 1
        elif v == '2':
            count_2s += 1

print ("Answer for part one:", (count_1s * count_2s))

print ("\nAnswer for part two:")
for y in range(rows):
    for x in range(columns):
        if (proc_picture[(y,x)] == '1'):
            print(u"\u2588", end="")
        else:
            print(" ", end="")
    print("")