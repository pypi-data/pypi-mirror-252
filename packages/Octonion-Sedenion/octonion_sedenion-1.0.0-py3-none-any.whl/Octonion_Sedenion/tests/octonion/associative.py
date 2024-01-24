#!/usr/bin/env python

import matplotlib.pyplot as plt
from octonion import *

def associator(x, y, z):
    return ((x*y)*z - x*(y*z)).norm()

def random_unit_octonion():
    x = Octonion(array=np.random.normal(size=8))
    return x/x.norm()

N = 1000000
s = 0
h = np.zeros(N)
for n in range(N):
    x = random_unit_octonion()
    y = random_unit_octonion()
    z = random_unit_octonion()    
    t = associator(x, y, z)
    s += t
    h[n] = t

print(s/N)
plt.hist(h, bins=200)
plt.show()

