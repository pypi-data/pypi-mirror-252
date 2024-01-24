import matplotlib.pyplot as plt
from sedenion import *

def random_unit_octonion():
    x = Sedenion(array=np.random.normal(size=16))
    return x/x.norm()

N = 1000000
s = 0
h = np.zeros(N)
for n in range(N):
    x = random_unit_octonion()
    y = random_unit_octonion()
    z = random_unit_octonion()    
    t = moufang1(x, y, z).norm()
    s += t
    h[n] = t

print('Moufang1:',s/N)
plt.hist(h, bins=200)
plt.show()

