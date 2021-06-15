import os
os.system('pip install tqdm')
import numpy as np
from tqdm import tqdm
import itertools


def check(cols, curr):

  if curr in new:
    for i in new[curr]:
      if cols[i] >= cols[curr]:
        cols[i] = cols[curr] - 1
        cols = check(cols, i)

  if curr in new1:
    for i in new1[curr]:
      if cols[i] <= cols[curr]:
        cols[i] = cols[curr] + 1
        cols = check(cols, i)

  return cols

def get_ans():
  cols = [-1 for i in range(ndots)] 

  for g in range(ndots):
    # print(g)
    # print(cols)

    if g in new:
      to = [cols[_] for _ in new[g]] # to this one
      toi = list(new[g])
    else: 
      to = set()
      toi = set()
    if g in new1:
      fr = [cols[_] for _ in new1[g]]
      fri = list(new1[g])
    else: 
      fr = set()
      fri = set()
    # print('near', toi, fri)

    for i in range(len(fr)):
      if cols[g] == -1:
        cols[g] = ndots
        cols[fri[i]] = ndots + 1
      elif cols[fri[i]] <= cols[g]: 
        cols[fri[i]] = cols[g] + 1
        cols = check(cols, fri[i])

    for i in range(len(to)):
      if cols[g] == -1:
        cols[g] = ndots
        cols[toi[i]] = ndots - 1
      elif cols[toi[i]] >= cols[g]: 
        cols[toi[i]] = cols[g] - 1
        cols = check(cols, toi[i])

    # print(cols)

  return len(np.unique(cols))

def next_check(st, s):
  # print('check', st, s)
  if st not in new: 
    # print('not in')
    return False
  for i in new[st]:
    # print('in nef', i)
    if i in s: 
      # print('i in s')
      return True
    global ss
    ss.add(i)
    if next_check(i, s.union({i})): 
      return True

  return False

def check_cycles():
  global ss
  ss = set()
  for i in new:
    # print('init', i)
    if i in ss: continue
    # {0: {1, 2}, 3: {1}, 5: {1, 4, 7}, 4: {0}, 2: {3, 6}, 7: {3, 6}, 6: {4}}
    if next_check(i, {i}): return True
  return False



n = int(input('Enter n: '))
ndots = 2**n
if n > 4: 
  print('The number is too large, it will be calculating for a lifetime.')
  exit()

edges = []
for g in range(ndots):
  for s in range(n):
    new = g ^ (1 << s)
    # print(bin(g), bin(new))
    if new > g:
      edges.append((g,new))


# print(edges)
# print(len(edges))

numbers = set()
# print(bin(2**(len(edges))-1))
for mask in tqdm(range(2**(len(edges))), position=0, leave=True):
  # print('mask', bin(mask))
  new1 = [ edges[_] if ((1 << _) & mask) else ( (edges[_][1], edges[_][0]) ) for _ in range(len(edges)) ]
  new = {}
  for i in new1:
    if i[0] not in new: new[i[0]] = set()
    new[i[0]].add(i[1])

  new1 = None
  if check_cycles():
    continue
    print('mask', bin(mask))
    print(new)
  # print(new)

  new1 = new
  new = {}
  for i in new1:
    for j in new1[i]:
      if j not in new: new[j] = set()
      new[j].add(i)
  # print(new)
  # print(new1)
  # an = get_ans()

  an = get_ans()
  # if an == 7:
  #   print(f'an{an}', new, new1, check_cycles())

  numbers.add(an)


  # if mask > 2: break
# pmax = max(numbers)
# if pmax != ndots:
#   for mask in range(2**(len(edges))):
#     ins = 0
#     for i in range(pmax+1, ndots+1):
#       if i in numbers: ins += 1
#     if ins == ndots-pmax: 
#       # print('broke')
#       break
#     an = get_ans1(set(range(max(numbers)+1)))
#     numbers = numbers.union(an)

print('\nPossible number of colors:', numbers)
