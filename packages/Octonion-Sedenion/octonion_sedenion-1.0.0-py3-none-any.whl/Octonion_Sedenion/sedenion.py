# -*- coding: utf8 -*-

# Title : Algorithms for Sedenions

################################################################################
## Created by Dieter Kadelka
## Date : 22 January 2024
## Email: dieterkadelka@aol.com
################################################################################

import numpy as np
from quaternion import quaternion as Quaternion
from octonion import Octonion
import math, cmath
import copy
import numbers
import numpy.linalg as nla
import sys

class Sedenion(Octonion):
  # General Problem: views are faster than copies.

  RIGHT_POWER = True
  # a**b = exp(log(a)*b) if True, a**b = exp(b*log(a)) if False
  PRECISION = 5

  def __init__(self,*v,array=None,q1=None,q2=None):
    # internally Sedenions are pairs of Octonions
    if q1 is not None or q2 is not None:
      if q1 is None:
        self.z1 = Octonion(0)
        self.z2 = q2
      else:
        self.z1 = q1
        if q2 is not None:
          self.z2 = q2
        else:
          self.z2 = Octonion(0)
    else:
      if array is not None:
        if v != ():
          raise ValueError
        else:
          v = array

      laenge = len(v)
      self.z1 = Octonion(0)
      self.z2 = Octonion(0)

      if laenge == 1:
        u = v[0] # v contains just one value, can be arbitrary
        if isinstance(u,(int,float)):
          self.z1.e0 = u
        elif isinstance(u,numbers.Complex):
          self.z1.e0 = u.real
          self.z1.e1 = u.imag # There may be more cases
        elif isinstance(u,Quaternion):
          self.z1 = Octonion(u)
        elif isinstance(u,Octonion) and not isinstance(u,Sedenion):
          # u is Octonion, but no Sedenion
          # Sedenions are Octonions, but Octonions are not Sedenions
          self.z1 = u
        elif isinstance(u,Sedenion):
          self.z1 = u.z1
          self.z2 = u.z2
        else:
          raise ValueError
      elif 1 < len(v) < 9:
        self.z1 = Octonion(array=v)
      elif 8 < len(v) < 17:
        self.z1 = Octonion(array=v[0:8])
        self.z2 = Octonion(array=v[8:])
      else:
        raise ValueError

# get or change individual components
  @property
  def e0(self):
    return self.z1.e0
  @e0.setter
  def e0(self,value):
    self.z1.e0 = value

  @property
  def e1(self):
    return self.z1.e1
  @e1.setter
  def e1(self,value):
    self.z1.e1 = value

  @property
  def e2(self):
    return self.z1.e2
  @e2.setter
  def e2(self,value):
    self.z1.e2 = value

  @property
  def e3(self):
    return self.z1.e3
  @e3.setter
  def e3(self,value):
    self.z1.e3 = value

  @property
  def e4(self):
    return self.z1.e4
  @e4.setter
  def e4(self,value):
    self.z1.e4 = value

  @property
  def e5(self):
    return self.z1.e5
  @e5.setter
  def e5(self,value):
    self.z1.e5 = value

  @property
  def e6(self):
    return self.z1.e6
  @e6.setter
  def e6(self,value):
    self.z1.e6 = value

  @property
  def e7(self):
    return self.z1.e7
  @e7.setter
  def e7(self,value):
    self.z1.e7 = value

  @property
  def e8(self):
    return self.z2.e0
  @e0.setter
  def e8(self,value):
    self.z2.e0 = value

  @property
  def e9(self):
    return self.z2.e1
  @e1.setter
  def e9(self,value):
    self.z2.e1 = value

  @property
  def e10(self):
    return self.z2.e2
  @e2.setter
  def e10(self,value):
    self.z2.e2 = value

  @property
  def e11(self):
    return self.z2.e3
  @e3.setter
  def e11(self,value):
    self.z2.e3 = value

  @property
  def e12(self):
    return self.z2.e4
  @e4.setter
  def e12(self,value):
    self.z2.e4 = value

  @property
  def e13(self):
    return self.z2.e5
  @e5.setter
  def e13(self,value):
    self.z2.e5 = value

  @property
  def e14(self):
    return self.z2.e6
  @e6.setter
  def e14(self,value):
    self.z2.e6 = value

  @property
  def e15(self):
    return self.z2.e7
  @e7.setter
  def e15(self,value):
    self.z2.e7 = value

  @property
  def components(self):
    return np.append(self.z1.components,self.z2.components)

  def __repr__(self):
    # Bad formatting!
    return 'sedenion' + str(tuple(self.components))
    # as in Quaternion

  def __str__(self):
    suffix = ('','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w')
    u = self.components
    if u[0] != 0:
      s = np.format_float_positional(u[0],precision=Sedenion.PRECISION) + ' '
    else:
      s = ''
    for i in range(1,16):
      if u[i] != 0.0:
        s += np.format_float_positional(u[i],precision=Sedenion.PRECISION,sign=True) + suffix[i] + ' '
    if s == '': s = '0'
    return s
    # There must be a better format

  def __getitem__(self,i): # Octonions subscriptable
    return self.components[i]

  def __mul__(self,v):
    # Sedenions are pairs of octonions (fast multiplication)
    a, b = self.z1, self.z2
    if isinstance(v,Sedenion):
      c,d = v.z1, v.z2
      return Sedenion(q1 = a*c-d.conj*b, q2 = d*a + b*c.conj)
    else:
      if isinstance(v,numbers.Real):
        u = Sedenion(q1 = a*v, q2 = b*v)
        try:
          u.sold_e0 = self.sold_e0*v
        except AttributeError:
          pass
        try:
          u.cold_e0 = self.cold_e0*v
        except AttributeError:
          pass
        try:
          u.told_e0 = self.told_e0*v
        except AttributeError:
          pass
        try:
          u.x = self.x*v
          u.y = self.y*v
        except AttributeError:
          pass
        try:
          u.r = self.r*v
          u.phi = self.phi
          u.I = self.I
        except AttributeError:
          pass
        return u
      elif isinstance(v,(numbers.Complex,Quaternion)):
        if isinstance(v,numbers.Complex):
          v = Octonion(v.real,v.imag,0,0)
        return Sedenion(q1 = a*v, q2 = b*v.conj)
      else:
        x = Sedenion(v)
        c, d = x.z1, x.z2
        return Sedenion(q1 = a*c-d.conj*b, q2 = d*a + b*c.conj)

  def __rmul__(self,v):
    # if v in v*self is no sedenion, otherwise we use __mul__
    if isinstance(v,numbers.Real):
      u = Sedenion(q1 = v*self.z1, q2 = v*self.z2)
      try:
        u.sold_e0 = self.sold_e0*v
      except AttributeError:
        pass
      try:
        u.cold_e0 = self.cold_e0*v
      except AttributeError:
        pass
      try:
        u.told_e0 = self.sold_e0*v
      except AttributeError:
        pass
      try:
        u.x = self.x*v
        u.y = self.y*v
      except AttributeError:
        pass
      try:
        u.r = self.r*v
        u.phi = self.phi
        u.I = self.I
      except AttributeError:
        pass
      return u
    else:
      if isinstance(v,numbers.Complex):
        v = Octonion(v.real,v.imag)
      elif isinstance(v,Quaternion):
        v = Octonion(v)
      return Sedenion(q1 = v*self.z1, q2 = self.z2*v)

  def __add__(self,v):
    x = Sedenion(v) # else complications with Octonions, Quaternions
    return Sedenion(q1 = self.z1 + x.z1, q2 = self.z2 + x.z2)

  def __radd__(self,v):
    x = Sedenion(v)
    return Sedenion(q1 = self.z1 + x.z1, q2 = self.z2 + x.z2)

  def __neg__(self):
    return Sedenion(q1=-self.z1,q2=-self.z2)

  def __sub__(self,v):
    x = Sedenion(v)
    return Sedenion(q1=self.z1-x.z1,q2=self.z2-x.z2)

  def __rsub__(self,v):
    x = Sedenion(v)
    return Sedenion(q1=x.z1-self.z1,q2=x.z2-self.z2)

  @property
  def conj(self):
    x = -self
    x.e0 *= -1
    return x

  def conjugate(self):
    return self.conj

  def imunit(self):
    # self = self.e0 + w.norm()*imunit
    w = self-self.conj
    wn = w.norm()
    if wn > 0:
      return w/wn
    else:
      return Sedenion(0,1)
      # If wn == 0 then I is undefined. Is 'raise ZeroDivisionError' better or is the solution with Sedenion(nan,...) better?

  def decomp(self):
    if not hasattr(self,'I'):
      w = 0.5*(self-self.conj)
      y = w.norm()
      if y > 0: # self non real
        self.x, self.y, self.I = self.e0, y, w/y
        return (self.e0, y, w/y)
      else: # self real with similar problem as in imunit
        self.x, self.y, self.I = self.e0, 0, Sedenion(0,1)
        return (self.x, self.y, self.I)
    else:
      return (self.x, self.y, self.I)
    # self -> decomp(self) is bijektion between octonion and {(e0,y,I)}

  def __invert__(self):
    return 1/(self.z1.norm()**2+self.z2.norm()**2)*self.conj
    # Raises ZeroDivisionError if self == 0. Seems to be the best solution here.

  def __truediv__(self,v):
  # returns self/v
    if isinstance(v,numbers.Real):
      if v == 0:
        raise ZeroDivisionError
      u = Sedenion(q1=self.z1/v,q2=self.z2/v)
      try:
        u.sold_e0 = self.sold_e0/v
        return u
      except AttributeError:
        return u
      try:
        u.cold_e0 = self.cold_e0/v
        return u
      except AttributeError:
        return u
      try:
        u.told_e0 = self.told_e0/v
        return u
      except AttributeError:
        return u
    else:
      if not isinstance(v,Sedenion):
        v = Sedenion(v)
      norm = v.norm()**2
      if norm > 0:
        return self*v.conj/norm
      else:
        raise ZeroDivisionError
    # Problem: without ZeroDivisionError we get Sedenion(nan/inf,...) if v == 0
    # Is there a better solution?

  def __rtruediv__(self,v):
  # returns v/self
    v = Sedenion(v)
    norm = self.norm()**2
    if norm > 0:
      return v*self.conj/norm
    else:
      raise ZeroDivisionError

  def polar(self): # generate polar coordinates
    if not hasattr(self,'phi'):
      w = 0.5*(self-self.conj)
      x = w.components
      normw = nla.norm(x)
      if normw > 0:
        self.x,self.y,self.I = self.e0, normw, w/normw
      else:
        self.x,self.y,self.I = self.e0, 0, Sedenion(0,1)
        # This is needed by log
      self.r,self.phi = cmath.polar(self.x+1j*self.y)
  # not enough information for improving polar

  def norm(self): # fast l2-norm
    return nla.norm(self.components)

  def vnorm(self): # l2-norm of non real components (slow)
    return nla.norm(self.components[1:])

  def exp(self):
    self.polar() # if self has polar coordinates do nothing, otherwise generate them
    r = math.exp(self.r*math.cos(self.phi))
    phi = self.y
    x = r*math.cos(phi)
    y = r*math.sin(phi)
    if y != 0:
      w = x + y*self.I # w is Sedenion
      w.r,w.phi,w.x,w.y,w.I = r,phi,x,y,self.I
      return w
    else: # self is real
      return Sedenion(math.exp(self.e0))

  def sin(self):
    self.decomp()
    u = cmath.sin(self.x+1j*self.y)
    v = u.real+u.imag*self.I
    v.x,v.y,v.I = u.real,u.imag,self.I
    v.r,v.phi = cmath.polar(v.x+1j*v.y)
    v.sold_e0 = self.e0
    return v

  def cos(self):
    self.decomp()
    u = cmath.cos(self.x+1j*self.y)
    v = u.real+u.imag*self.I
    v.x,v.y,v.I = u.real,u.imag,self.I
    v.r,v.phi = cmath.polar(v.x+1j*v.y)
    v.cold_e0 = self.e0
    return v

  def tan(self):
    self.decomp()
    u = cmath.tan(self.x+1j*self.y)
    v = u.real+u.imag*self.I
    v.x,v.y,v.I = u.real,u.imag,self.I
    v.r,v.phi = cmath.polar(v.x+1j*v.y)
    v.told_e0 = self.e0
    return v

  def sinh(self):
    return (self.exp()-(-self).exp())/2

  def cosh(self):
    return (self.exp()+(-self).exp())/2

# sin, cos and tan are multivalued. cmath chooses one inverse
# self cannot contain enough information to resolve this problem
# Is uniformisation a solution to solve this problem as in exp/log?
# arcsin(sin(0.5*a)) correct, but arcsin(sin(0.6*a)) incorrect
# corrected with fake
# We have to copy with branch cuts from 1 to infinity and from -1 to -infinity

  def arcsin(self):
    self.decomp()
    u = cmath.asin(self.x+1j*self.y)
    try:
      korr = 1 - 2*(math.floor(self.sold_e0/math.pi+0.5) & 1)
      u = self.sold_e0 + korr*u.imag*self.I # fake and useless
    except AttributeError:
      u = u.real+u.imag*self.I
    u.polar()
    return u

  def arccos(self):
    self.decomp()
    if self.y == 0:
      u = -cmath.acos(self.x+1j*self.y)
    else:
      u = cmath.acos(self.x+1j*self.y)
    try:
      korr = 1 - 2*(math.floor(self.cold_e0/math.pi) & 1)
      u = self.cold_e0 + korr*u.imag*self.I # fake and useless
    except AttributeError:
      u = u.real+u.imag*self.I
    u.polar()
    return u

  def arctan(self): # great rounding errors
    self.decomp()
    u = cmath.atan(self.x+1j*self.y)
    try:
      u = self.told_e0 + u.imag*self.I # fake and useless
    except AttributeError:
      u = u.real+u.imag*self.I
    u.polar()
    return u

  def sqrt(self): # computation without polar coordinates
    a = self.norm()
    if a+self.e0 > 0:
      c = math.sqrt(0.5/(a+self.e0))
      r = c*self
      r.e0 = (a+self.e0)*c
      return r
    else: # self negativ reell
      return math.sqrt(-self.e0)*e1
      # e1 can be replaced by any unit I

  def log(self):
    self.polar()
    return math.log(self.r)+self.phi*self.I

  def __pow__(self,v):
    if self.norm() == 0:
      return Sedenion(0)
    if Sedenion.RIGHT_POWER:
      return (self.log()*v).exp()
    else:
      return (v*self.log()).exp()
  # identical results if v real
  # What is the interpretation of a**b, if b is not real
  # Even without interpretation we have (a**b)**(1/b) = a

  def __rpow__(self,v):
    if Sedenion(v).norm() == 0:
      return Sedenion(0)
    if self.norm() == 0:
      return Sedenion(1)
    v = Sedenion(v)
    if Sedenion.RIGHT_POWER:
      return (v.log()*self).exp()
    else:
      return (self*v.log()).exp()
    # identical results if v real

sed = np.dtype(Sedenion)

# Definition of functions
# Since Sedenion is a subclass of Octonion, these following functions choose depending on the class the right function

def exp(v):
  if isinstance(v,numbers.Real):
    return math.exp(v)
  elif isinstance(v,numbers.Complex):
    return cmath.exp(v)
  else:
    return v.exp()

def sin(v):
  if isinstance(v,numbers.Real):
    return math.sin(v)
  elif isinstance(v,numbers.Complex):
    return cmath.sin(v)
  else:
    return v.sin()

def cos(v):
  if isinstance(v,numbers.Real):
    return math.cos(v)
  elif isinstance(v,numbers.Complex):
    return cmath.cos(v)
  else:
    return v.cos()

def tan(v):
  if isinstance(v,numbers.Real):
    return math.tan(v)
  elif isinstance(v,numbers.Complex):
    return cmath.tan(v)
  else:
    return v.tan()

def arcsin(v):
  if isinstance(v,numbers.Real):
    return math.asin(v)
  elif isinstance(v,numbers.Complex):
    return cmath.asin(v)
  else:
    return v.arcsin()

def arccos(v):
  if isinstance(v,numbers.Real):
    return math.acos(v)
  elif isinstance(v,numbers.Complex):
    return cmath.acos(v)
  else:
    return v.arccos()

def arctan(v):
  if isinstance(v,numbers.Real):
    return math.atan(v)
  elif isinstance(v,numbers.Complex):
    return cmath.atan(v)
  else:
    return v.arctan()

def sinh(v):
  if isinstance(v,numbers.Real):
    return math.sinh(v)
  elif isinstance(v,numbers.Complex):
    return cmath.sinh(v)
  else:
    return v.sinh()

def cosh(v):
  if isinstance(v,numbers.Real):
    return math.cosh(v)
  elif isinstance(v,numbers.Complex):
    return cmath.cosh(v)
  else:
    return v.cosh()

def tanh(v):
  return sinh(v)/cosh(v)

def sqrt(v):
  if isinstance(v,numbers.Real):
    return math.sqrt(v)
  elif isinstance(v,numbers.Complex):
    return cmath.sqrt(v)
  else:
    return v.sqrt()

def log(v):
  if isinstance(v,numbers.Real):
    return math.log(v)
  elif isinstance(v,numbers.Complex):
    return cmath.log(v)
  else:
    return v.log()

def associator(x,y,z):
  return (x*y)*z-x*(y*z)

def commutator(x,y):
  return x*y-y*x

def moufang1(x,y,z):
  return (x*(y*x))*z - x*(y*(x*z))

def moufang2(x,y,z):
  return (x*y)*(z*x)-x*((y*z)*x)

# moufang1 = 0 and moufang2 = 0 (apart from rounding errors)
# octonions are an alternating field

def uniform(a,b): # Generates random sedenions equidistributed in [a,b]^16
  x = a + np.random.random(16)*(b-a)
  return Sedenion(array=x)

def random_ball(r=1): # Generates random sedenions equidistributed on the ball around 0 with radius r
  x = Sedenion(array=np.random.standard_normal(size=16))
  y = np.random.uniform()**(1/16)*r
  return x*y/x.norm()

def norm(v):
  if isinstance(v,(numbers.Real,numbers.Complex)):
    return abs(v)
  else:
    return v.norm()

# Some test values
a = Sedenion(3,1,4,1,5,9,2,6,-3,0,1,2,3,4,5,6)
a10 = a*a*a*a*a*a*a*a*a*a
an = norm(a)
au = a/an
b = Sedenion(-3.2,5.3,1.2,math.pi)
bn = norm(b)
bu = b/bn
c = Sedenion(q1=Octonion(-3.2,5.3,1.2,math.pi))
e0 = Sedenion(1)
e1 = Sedenion(0,1)
e2 = Sedenion(0,0,1)
e3 = Sedenion(0,0,0,1)
e4 = Sedenion(0,0,0,0,1)
e5 = Sedenion(0,0,0,0,0,1)
e6 = Sedenion(0,0,0,0,0,0,1)
e7 = Sedenion(0,0,0,0,0,0,0,1)
e8 = Sedenion(0,0,0,0,0,0,0,0,1)
e9 = Sedenion(0,0,0,0,0,0,0,0,0,1)
e10 = Sedenion(0,0,0,0,0,0,0,0,0,0,1)
e11 = Sedenion(0,0,0,0,0,0,0,0,0,0,0,1)
e12 = Sedenion(0,0,0,0,0,0,0,0,0,0,0,0,1)
e13 = Sedenion(0,0,0,0,0,0,0,0,0,0,0,0,0,1)
e14 = Sedenion(0,0,0,0,0,0,0,0,0,0,0,0,0,0,1)
e15 = Sedenion(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1)

all_e = {'e0':e0,'e1':e1,'e2':e2,'e3':e3,'e4':e4,'e5':e5,'e6':e6,'e7':e7,'e8':e8,'e9':e9,'e10':e10,'e11':e11,'e12':e12,'e13':e13,'e14':e14,'e15':e15}
e_keys = all_e.keys()
e_values = all_e.values()

# Using routines from numpy
A = np.array([[a,b],[c,e3]])
AtA = A @ A
Ap2 = A**2
Ap3 = A**3
# print('A*A = ',Ata) # matrix multiplication
# print('A^2 = ',Ap2) # not the same result, elementwise
# print('A^3 = ',Ap3) # power function applied elementwise
# Note that A @ (A @ A) != (A @ A) @ A, while (a*a)*a = a*(a*a)

X = np.array([a,b])
X_bar_exp = np.mean(np.exp(X))
# print('mean of exp(a) and exp(b) =',X_bar_exp)

# Unfortunately nla.inv(A) doesn't work. Raises UFuncTypeError. Can this be resolved?
