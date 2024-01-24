import matplotlib.pyplot as plt
from sedenion import *

def associator(x, y, z):
    return ((x*y)*z - x*(y*z)).norm()

def random_unit_octonion():
    x = Sedenion(array=np.random.normal(size=16))
    return x/x.norm()

N = 1000000
s = 0
maximum = 0
minimum = 100
h = np.zeros(N)
for n in range(N):
    x = random_unit_octonion()
    y = random_unit_octonion()
    z = random_unit_octonion()    
    t = associator(x, y, z)
    maximum = max(maximum,t)
    minimum = min(minimum,t)
    s += t
    h[n] = t

print('Mean    =',s/N)
print('Maximum =',maximum)
print('Minimum =',minimum)
plt.hist(h, bins=200)
plt.show()

