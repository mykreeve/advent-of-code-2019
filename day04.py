lower = 254032
upper = 789860

def contains_double(a):
    tests = ['11','22','33','44','55','66','77','88','99']
    for t in tests:
        if t in str(a):
            return True
    return False

def contains_2_in_a_row(a):
    sa = str(a)
    nums = []
    curr = ''
    count = 0
    for p in range(len(sa)):
        if sa[p] == curr:
            count += 1
        else:
            if curr:
                nums.append(count)
            curr = sa[p]
            count = 1
    nums.append(count)
    if 2 in nums:
        return True
    else:
        return False

def not_descending(a):
    sa = str(a)
    for p in range(len(sa)-1):
        if (int(sa[p+1]) < int(sa[p])):
            return False
    return True

count = 0

for a in range(lower, upper+1):
    if (contains_double(a) and not_descending(a)):
        # print(a)
        count += 1

print ("Answer for part one:", count)

count = 0

for a in range(lower, upper+1):
    if (contains_2_in_a_row(a) and not_descending(a)):
        # print(a)
        count += 1

print ("Answer for part two:", count)