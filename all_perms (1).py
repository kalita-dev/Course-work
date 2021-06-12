import os
os.system('pip install tqdm')
import numpy as np
from tqdm import tqdm
import itertools

global ss
ss = set()

def get_ans():
  cols = [-1 for i in range(ndots)] 

  for g in range(ndots):


    if g in new:
      to = [cols[_] for _ in new[g]]
      toi = list(new[g])
    else: 
      to = set()
      fri = set()
    if g in new1:
      fr = [cols[_] for _ in new1[g]]
      fri = list(new1[g])
    else: 
      fr = set()
      fri = set()

    for i in range(len(fr)):
      if cols[g] == -1:
        cols[g] = ndots
        cols[fri[i]] = ndots + 1
      else: cols[fri[i]] = cols[g] + 1

    for i in range(len(to)):
      if cols[g] == -1:
        cols[g] = ndots
        cols[toi[i]] = ndots - 1
      else: cols[toi[i]] = cols[g] - 1



  return(np.max(cols) - np.min(cols) + 1)

def next_check(st, s):
  if st not in new: 
    return False
  for i in new[st]:
    if i in s: 
      return True
    global ss
    ss.add(i)
    if next_check(i, s.union({i})): 
      return True

  return False

def check_cycles():
  for i in new:
    if i in ss: continue
    if next_check(i, set()): return True
  return False




def perm(lst, n):  
    buff = set()
    for i in itertools.permutations(lst * max(n - len(lst) + 1, 1), n):
      if i not in buff: 
        yield i
        buff.add(i)


def get_ans1(d):
  poss = set()
  for i in set(range(1,ndots+1)).difference(d):
    for col in perm(list(range(i)), ndots):
      fail = False
      for g in range(ndots):
        if g in new:
          for j in new[g]: 
            if col[j] >= col[g]: 
              fail = True
              break
        if g in new1:
          for j in new1[g]:
            if col[j] <= col[g]: 
              fail = True
              break
      if not fail:
        poss.add(i)
        break
  return poss


n = int(input('Enter n: '))
ndots = 2**n
if n > 4: 
  print('The number is too large, it will be calculating for a lifetime.')
  exit()

edges = []
for g in range(ndots):
  for s in range(n):
    new = g ^ (1 << s)
    if new > g:
      edges.append((g,new))



numbers = set()
for mask in tqdm(range(2**(len(edges))), position=0, leave=True):

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

  new1 = new
  new = {}
  for i in new1:
    for j in new1[i]:
      if j not in new: new[j] = set()
      new[j].add(i)

  an = get_ans()

  numbers.add(an)



pmax = max(numbers)
if pmax != ndots:
  for mask in range(2**(len(edges))):
    ins = 0
    for i in range(pmax+1, ndots+1):
      if i in numbers: ins += 1
    if ins == ndots-pmax: 
      break
    an = get_ans1(set(range(max(numbers)+1)))
    numbers = numbers.union(an)

print('\nPossible number of colors:', numbers)
