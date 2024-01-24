from sedenion import *
# determines all pairs ((ei±ej),(ek±el) of zero divisors with (ei±ej)*(ek±el) = 0

single = (e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15)

def zero_divisormm(i,j,k,l):
  return (single[i]-single[j])*(single[k]-single[l])

def zero_divisorpp(i,j,k,l):
  return (single[i]+single[j])*(single[k]+single[l])

def zero_divisorpm(i,j,k,l):
  return (single[i]+single[j])*(single[k]-single[l])

def zero_divisormp(i,j,k,l):
  return (single[i]-single[j])*(single[k]+single[l])

counter = 0
tested = 0

for i in range(15):
  for j in range(i+1,15):
    for k in range(i,15):
      for l in range(k+1,15):
        tested += 1
        pp = True
        mm = True
        pm = True
        mp = True
        if norm(zero_divisorpp(i,j,k,l)) == 0:
          print((i+1,j+1,k+1,l+1),'pp')
          counter += 1
          pp = False 
        if norm(zero_divisorpm(i,j,k,l)) == 0 and pp:
          print((i+1,j+1,k+1,l+1),'pm')
          counter += 1
          pm = False
        if norm(zero_divisormp(i,j,k,l)) == 0 and pp and pm:
          print((i+1,j+1,k+1,l+1),'mp')
          counter += 1
          mp = False
        if norm(zero_divisormm(i,j,k,l)) == 0 and pp and pm and mp:
          print((i+1,j+1,k+1,l+1),'mm')
          counter += 1

print('Total number of pairs = ',counter)          
print('Tested altogether     =',tested)
