#!/usr/local/bin/python
# Title: Calculus in the Riemann plane

################################################################################
## Created by Dieter Kadelka
## Date : 22 January 2024
## Email: dieterkadelka@aol.com
################################################################################

import cmath as cc
import math
import numbers
import copy

class CC:
 
  def __init__(self,v):
    if isinstance(v,(numbers.Real,numbers.Complex)):
      self.value = complex(v)
      self.r,self.phi = cc.polar(self.value)
    else:
      self = v
  
  def __repr__(self):
    w = self.value
    return f"{w.real}{' +' if w.imag >= 0 else ''} {w.imag}j"
#    return self.value.__repr__().strip('()')
# geht sicher noch zu verbessern, z.B. wenn w.real oder w.imag Integer sind

#### Die folgenden @property und @setter sind vermutlich überflüssig
  @property
  def real(self):
    return self.value.real
  @real.setter
  def real(self,value):
    self.value = complex(value+1j*self.value.imag)
    self.r,self.phi = cc.polar(self.value)

  @property
  def imag(self):
    return self.value.imag
  @imag.setter
  def imag(self,value):
    self.value = complex(self.value.real+1j*value)
    self.r,self.phi = cc.polar(self.value)

  @property
  def rho(self):
    return self.r
  @rho.setter
  def rho(self,value):
    self.r = value
    self.value = cc.rect(self.r,self.phi)

  @property
  def angle(self):
    return self.phi
  @angle.setter
  def angle(self,value):
    self.phi = value
    self.value = cc.rect(self.r,self.phi)

#### die nachfolgenden Funktionen sind noch zu verbessern!

  def __add__(self,v):
    if not isinstance(v,CC):
      v = CC(v)
    return CC(self.value+v.value)

  def __radd__(self,v):
    if not isinstance(v,CC):
      v = CC(v)
    return CC(self.value+v.value)
    
  def __neg__(self):
    w = copy.copy(self)
    w.value = -w.value
    w.phi = -w.phi 
    return w

  def __sub__(self,v):
    w = copy.copy(self)
    if not isinstance(v,CC):
      v = CC(v)
    return w+(-v)

  def __rsub__(self,v):
    w = copy.copy(self)
    if not isinstance(v,CC):
      v = CC(v)
    return v+(-w)

  def __mul__(self,v):
    w = copy.copy(self)
    if not isinstance(v,CC):
      v = CC(v)
    w.r *= v.r
    w.phi += v.phi
    w.value = w.r*math.cos(w.phi) + w.r*math.sin(w.phi)*1j
    return w

  def __rmul__(self,v):
    w = copy.copy(self)
    if not isinstance(v,CC):
      v = CC(v)
    w.r *= v.r
    w.phi += v.phi
    w.value = w.r*math.cos(w.phi) + w.r*math.sin(w.phi)*1j
    return w

  def __truediv__(self,v):
    w = copy.copy(self)
    if not isinstance(v,CC):
      v = CC(v)
    w.r /= v.r
    w.phi -= v.phi
    w.value = w.r*math.cos(w.phi) + w.r*math.sin(w.phi)*1j
    return w
   
  def __rtruediv__(self,v):
    w = copy.copy(self)
    if not isinstance(v,CC):
      v = CC(v)
    w.r = v.r/w.r
    w.phi = v.phi-w.phi
    w.value = w.r*math.cos(w.phi) + w.r*math.sin(w.phi)*1j
    return w
   
  def exp(self):
    w = copy.copy(self)
    w.r = math.exp(self.r*math.cos(self.phi))
    w.phi = self.value.imag
    w.value = w.r*math.cos(w.phi) + w.r*math.sin(w.phi)*1j
    return w

  def sin(self):
    u = (1j*self).exp()
    r,phi = u.r,u.phi
##    return 0.5*(r+1/r)*sin(phi) + 0.5j*(1/r-r)*cos(phi)
    return ((1j*self).exp()-(-1j*self).exp())/2j 

  def cos(self):
    return ((1j*self).exp()+(-1j*self).exp())/2
  # Da hier eine Addition vorkommt, ist nicht gesichert dass sin und cos korrekt!
  # Es gibt bessere Formel!

  def asin(self):
    return cc.asin(self.value)

  def acos(self):
    return cc.acos(self.value)

  def log(self):
    w = math.log(self.r)+self.phi*1j
    return CC(w)

  def __pow__(self,v):
    if not isinstance(v,CC):
      v = CC(v)
    return (self.log()*v).exp()

  def sqrt(self):
    return self**0.5
  # geht sicherlich besser!  

  def conj(self):
    w = copy.copy(self)
    w.value = w.value.conjugate()
    w.phi = -w.phi
    return w

def exp(v):
  if isinstance(v,numbers.Real):
    return math.exp(v)
  elif isinstance(v,numbers.Complex):
    return cc.exp(v)
  else:
    return v.exp()

def sin(v):
  if isinstance(v,numbers.Real):
    return math.sin(v)
  elif isinstance(v,numbers.Complex):
    return cc.sin(v)
  else:
    return v.sin()

def cos(v):
  if isinstance(v,numbers.Real):
    return math.cos(v)
  elif isinstance(v,numbers.Complex):
    return cc.cos(v)
  else:
    return v.cos()

def asin(v):
  if isinstance(v,numbers.Real):
    return math.asin(v)
  elif isinstance(v,numbers.Complex):
    return cc.asin(v)
  else:
    return v.asin()

def acos(v):
  if isinstance(v,numbers.Real):
    return math.acos(v)
  elif isinstance(v,numbers.Complex):
    return cc.acos(v)
  else:
    return v.acos()

def log(v):
  if isinstance(v,numbers.Real):
    return math.log(v)
  elif isinstance(v,numbers.Complex):
    return cc.log(v)
  else:
    return v.log()

def sqrt(v):    
  if isinstance(v,numbers.Real):
    return math.sqrt(v)
  elif isinstance(v,numbers.Complex):
    return cc.sqrt(v)
  else:
    return v.sqrt()

a = CC(1+4j)
b = a.log()
b += 3*math.pi*1j # hier ist eine Addition, die alles kaputt macht!
c = (10*b).exp()
print ('Original ',(a**10)**0.1)
print ('Modifiziert ',c**0.1)

a10 = a*a*a*a*a*a*a*a*a*a

print ('Korrektes a^10: ',a10)
print ('Python: ',a**10)


