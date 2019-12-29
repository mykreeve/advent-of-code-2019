import collections

commands = []

file = open("input/day22input.txt")
file = file.readlines()
for line in file:
    line = line.replace("\n","")
    line = line.replace("deal with increment ","redeal,")
    line = line.replace("cut ","rotate,")
    line = line.replace("deal into new stack","reverse")
    line = line.split(",")
    commands.append(line)

deck_size = 10007

deck = collections.deque()
for a in range(deck_size):
    deck.append(a)

def deal_with_increment(deck,number):
    new_deck = []
    for i in range(deck_size):
        new_deck.append(0)
    pos = 0
    while len(deck) > 0:
        a = deck.popleft()
        new_deck[pos] = a
        pos = pos + number
        if pos > deck_size:
            pos = pos - deck_size
    return collections.deque(new_deck)

for command in commands:
    if command[0] == 'rotate':
        val = int(command[1])
        if val < 0:
            deck.rotate(abs(val))
        if val > 0:
            deck.rotate(-val)
    if command[0] == 'reverse':
        deck.reverse()
    if command[0] == 'redeal':
        deck = deal_with_increment(deck,int(command[1]))

for n,a in enumerate(deck):
    if a == 2019:
        print("Answer for part one:", n)

## Not my work - this solution came from:
## https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbtugcu/

m = 119315717514047
n = 101741582076661
pos = 2020

shuffles = { 'deal with increment ': lambda x,m,a,b: (a*x %m, b*x %m),
         'deal into new stack': lambda _,m,a,b: (-a %m, (m-1-b)%m),
         'cut ': lambda x,m,a,b: (a, (b-x)%m) }
a,b = 1,0
with open('input/day22input.txt') as f:
  for s in f.read().strip().split('\n'):
    for name,fn in shuffles.items():
      if s.startswith(name):
        arg = int(s[len(name):]) if name[-1] == ' ' else 0
        a,b = fn(arg, m, a, b)
        break
r = (b * pow(1-a, m-2, m)) % m
print(f"Answer to part two: {((pos - r) * pow(a, n*(m-2), m) + r) % m}")