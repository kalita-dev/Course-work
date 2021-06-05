import numpy as np

n =  int(input('Enter n: '))
ndots = 2**n
cols = [-1 for i in range(ndots)]

for g in range(ndots):
  #print(g, bin(g ^ (g >> 1)))

  g = g ^ (g >> 1)
  #for s in range(n):
    #print(bin(g & ~(1 << s)), cols[g ^ (1 << s)])
  near = set(cols[g & ~(1 << s)] for s in range(n))

  #print('will use:', max(near) + 1)
  cols[g] = max(near) + 1

  #print(cols)

print('Minimum number of colors:', np.max(cols) + 1)
