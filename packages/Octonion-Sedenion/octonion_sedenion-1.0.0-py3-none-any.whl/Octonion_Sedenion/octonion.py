# -*- coding: utf8 -*-

# Title : Algorithms for Octonions

################################################################################
## Created by Dieter Kadelka
## Date : 22 January 2024
## Email: dieterkadelka@aol.com
################################################################################

import numpy as np
import quaternion as qu
from quaternion import quaternion as Quaternion
import math, cmath
import copy
import numbers
import numpy.linalg as nla
import sys

class Octonion(object):
  # General Problem: views are faster than copies.

  RIGHT_POWER = True
  # a**b = exp(log(a)*b) if True, a**b = exp(b*log(a)) if False
  PRECISION = 5

  def __init__(self,*v,array=None,q1=None,q2=None):
    if q1 is not None:
      # internally Octonion are pairs of Quaternions (numpy-quaternion is fast)
      self.z1 = q1
      if q2 is not None:
        self.z2 = q2
      else:
        self.z2 = qu.zero.copy()
    else:
      if array is not None:
        if v != ():
          raise ValueError
        else:  
          v = array

      laenge = len(v)
      if laenge > 3:
        self.z1 = qu.as_quat_array(v[0:4])
      else:
        self.z1 = qu.zero.copy() # without copy zero will be modified
      self.z2 = qu.zero.copy() # must not be a view

      if laenge == 0:
        pass # zero
      elif laenge == 1: # real or complex number or quaternion
        u = v[0]
        if isinstance(u,(int,float)):
          self.z1.w = u
        elif isinstance(u,numbers.Complex):
          self.z1.w = u.real
          self.z1.x = u.imag # There may be more cases
        elif isinstance(u,Quaternion):
          self.z1 = u
        elif isinstance(u,Octonion):
          self.z1 = u.z1
          self.z2 = u.z2
        else:
          raise ValueError
          # if v is a string, f.i., then we get zero
      elif laenge == 2: # complex number represented as pair of reals
        self.z1.w = v[0]
        self.z1.x = v[1]
      elif laenge == 3:
        self.z1.w = v[0]
        self.z1.x = v[1]
        self.z1.y = v[2]
      elif laenge == 4: pass
      elif laenge == 5:
        self.z2.w = v[4]
      elif laenge == 6:
        self.z2.w = v[4]
        self.z2.x = v[5]
      elif laenge == 7:
        self.z2.w = v[4]
        self.z2.x = v[5]
        self.z2.y = v[6]
      elif laenge == 8:
        self.z2 = qu.as_quat_array(v[4:8])
      else: # some inputs cannot be interpreted
        raise ValueError

  # get or change individual components
  @property
  def e0(self):
    return self.z1.w
  @e0.setter
  def e0(self,value):
    self.z1.w = value

  @property
  def e1(self):
    return self.z1.x
  @e1.setter
  def e1(self,value):
    self.z1.x = value

  @property
  def e2(self):
    return self.z1.y
  @e2.setter
  def e2(self,value):
    self.z1.y = value

  @property
  def e3(self):
    return self.z1.z
  @e3.setter
  def e3(self,value):
    self.z1.z = value

  @property
  def e4(self):
    return self.z2.w
  @e4.setter
  def e4(self,value):
    self.z2.w = value

  @property
  def e5(self):
    return self.z2.x
  @e5.setter
  def e5(self,value):
    self.z2.x = value

  @property
  def e6(self):
    return self.z2.y
  @e6.setter
  def e6(self,value):
    self.z2.y = value

  @property
  def e7(self):
    return self.z2.z
  @e7.setter
  def e7(self,value):
    self.z2.z = value

  @property
  def components(self):
    return np.append(self.z1.components,self.z2.components)

  def __repr__(self):
    # Bad formatting!
    return 'octonion' + str(tuple(self.components))
    # as in quaternion

  def __str__(self):
    suffix = ('','i','j','k','l','m','n','o')
    u = self.components
    if u[0] != 0:
      s = np.format_float_positional(u[0],precision=Octonion.PRECISION) + ' '
    else:
      s = ''
    for i in range(1,8):
      if u[i] != 0.0:
        s += np.format_float_positional(u[i],precision=Octonion.PRECISION,sign=True) + suffix[i] + ' '
    if s == '': s = '0'
    return s
    # There must be a better format

  def __getitem__(self,i): # Octonions subscriptable
    return self.components[i]

  def __mul__(self,v):
    # Octonions are pairs of quaternions (fast multiplication)
    a, b = self.z1, self.z2
    try:
      c, d = v.z1, v.z2
      return Octonion(q1 = a*c-d.conj()*b, q2 = d*a + b*c.conj())
    except AttributeError:
      if isinstance(v,numbers.Real):
        u = Octonion(q1 = a*v, q2 = b*v)
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
          v = Quaternion(v.real,v.imag,0,0)
        return Octonion(q1 = a*v, q2 = b*v.conj())
      else:
        x = Octonion(v)
        c, d = x.z1, x.z2
        return Octonion(q1 = a*c-d.conj()*b, q2 = d*a + b*c.conj())

  def __rmul__(self,v):
    # is no octonion, otherwise we use __mul__
    if isinstance(v,numbers.Real):
      u = Octonion(q1 = self.z1*v, q2 = self.z2*v)
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
    else:
      if isinstance(v,numbers.Complex):
        v = Quaternion(v.real,v.imag,0,0)
      return Octonion(q1 = v*self.z1, q2 = self.z2*v)

  def __add__(self,v):
    try:
      return Octonion(q1=self.z1+v.z1,q2=self.z2+v.z2)
    except AttributeError:
      x = Octonion(v)
      return Octonion(q1 = self.z1 + x.z1, q2 = self.z2 + x.z2)

  def __radd__(self,v):
    y = Octonion(v) # otherwise we use __add__
    return self+y

  def __neg__(self):
    return Octonion(q1=-self.z1,q2=-self.z2)

  def __sub__(self,v):
    try:
      return Octonion(q1=self.z1-v.z1,q2=self.z2-v.z2)
    except AttributeError:
      x = Octonion(v)
      return Octonion(q1=self.z1-x.z1,q2=self.z2-x.z2)

  def __rsub__(self,v):
    y = Octonion(v) # otherwise we use __sub__
    return y-self

  @property
  def conj(self):
    x = -self
    x.z1.w *= -1
    return x

  def conjugate(self): # for applications with numpy this is needed  
    return self.conj

  def imunit(self):
    # self = self.e0 + w.norm()*imunit
    w = copy.deepcopy(self)
    w.e0 = 0
    return w/w.norm()

  def decomp(self):
    if not hasattr(self,'I'):
      w = copy.deepcopy(self)
      w.e0 = 0
      y = w.norm()
      if y > 0: # self non real
        self.x, self.y, self.I = self.e0, y, w/y
        return (self.e0, y, w/y)
      else: # self real
        self.x, self.y, self.I = self.e0, 0, Octonion(0,1)
        return (self.x, self.y, self.I)
    else:
      return (self.x, self.y, self.I)
    # self -> decomp(self) is bijektion between octonion and {(e0,y,I)}

  def __invert__(self):
    return 1/(self.z1.norm()+self.z2.norm())*self.conj

  def __truediv__(self,v):
  # returns self/v
    if isinstance(v,numbers.Real):
      if v == 0:
        raise ZeroDivisionError
      u = Octonion(q1=self.z1/v,q2=self.z2/v)
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
      if not isinstance(v,Octonion):
        v = Octonion(v)
      norm = v.z1.norm()+v.z2.norm()
      # norm in octonion and quaternion are implemented differently!
      if norm > 0:
        return self*v.conj/norm
      else:
        raise ZeroDivisionError

  def __rtruediv__(self,v):
  # returns v/self
    v = Octonion(v)
    norm = self.z1.norm()+self.z2.norm()
    if norm > 0:
      return v*self.conj/norm
    else:
      raise ZeroDivisionError

  def polar(self): # generate polar coordinates
    if not hasattr(self,'phi'):
      w = copy.deepcopy(self)
      w.z1.w = 0
      normw = math.sqrt(w.z1.norm()+w.z2.norm())
      if normw > 0:
        self.x,self.y,self.I = self.z1.w, normw, w/normw
      else:
        self.x,self.y,self.I = self.z1.w, 0, Octonion(0,1)
        # This is needed by log
      self.r,self.phi = cmath.polar(self.x+1j*self.y)
  # not enough information for improving polar

  def norm(self): # fast l2-norm
    n1 = self.z1.norm()
    n2 = self.z2.norm()
    return math.sqrt(n1+n2) # quaternion.norm is square of l2-norm

  def vnorm(self): # l2-norm of non real components (slow)
    x = self.components
    return nla.norm(x[1:])

  def exp(self):
    self.polar() # if self has polar coordinates do nothing, otherwise generate them
    r = math.exp(self.r*math.cos(self.phi))
    phi = self.y
    x = r*math.cos(phi)
    y = r*math.sin(phi)
    if y != 0:
      w = x + y*self.I # w is Octonion
      w.r,w.phi,w.x,w.y,w.I = r,phi,x,y,self.I
      return w
    else: # self is real
      return Octonion(math.exp(self.e0))

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

  def arcsin(self):
    self.decomp()
    u = cmath.asin(self.x+1j*self.y)
    try:
      korr = 1 - 2*(math.floor(self.sold_e0/math.pi+0.5) & 1)
      u = self.sold_e0 + korr*u.imag*self.I # fake
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
      u = self.cold_e0 + korr*u.imag*self.I # fake
    except AttributeError:
      u = u.real+u.imag*self.I
    u.polar()
    return u

  def arctan(self): # great rounding errors
    self.decomp()
    u = cmath.atan(self.x+1j*self.y)
    try:
      u = self.told_e0 + u.imag*self.I # fake
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
      return Octonion(1)
    if Octonion.RIGHT_POWER:
      return (self.log()*v).exp()
    else:
      return (v*self.log()).exp()
  # identical results if v real
  # What is the interpretation of a**b, if b is not real
  # Even without interpretation we have (a**b)**(1/b) = a

  def __rpow__(self,v):
    if Octonion(v).norm() == 0:
      return Octonion(0)
    if self.norm() == 0:
      return Octonion(1)
    v = Octonion(v)
    if Octonion.RIGHT_POWER:
      return (v.log()*self).exp()
    else:
      return (self*v.log()).exp()
    # identical results if v real

oct = np.dtype(Octonion)

# Definition of functions
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

def uniform(a,b): # Generates random octions equidistributed in [a,b]^8
  x = a + np.random.random(8)*(b-a)
  return Octonion(array=x)

def random_ball(r=1): # Generates random sedenions equidistributed on the ball around 0 with radius r
  x = Octonion(array=np.random.standard_normal(size=8))
  y = np.random.uniform()**(1/8)*r
  return x*y/x.norm()

def norm(v):
  if isinstance(v,(numbers.Real,numbers.Complex)):
    return abs(v)
  else:
    return v.norm()

def left_matrix(v):
  if isinstance(v,(numbers.Real,numbers.Complex)):
    v = Octonion(v)
  elif isinstance(v,Quaternion):
    v = Octonion(q1=v)
  a0,a1,a2,a3,a4,a5,a6,a7 = v.components
  return np.array([[a0,-a1,-a2,-a3,-a4,-a5,-a6,-a7],
                   [a1,a0,-a3,a2,-a5,a4,a7,-a6],
                   [a2,a3,a0,-a1,-a6,-a7,a4,a5],
                   [a3,-a2,a1,a0,-a7,a6,-a5,a4],
                   [a4,a5,a6,a7,a0,-a1,-a2,-a3],
                   [a5,-a4,a7,-a6,a1,a0,a3,-a2],
                   [a6,-a7,-a4,a5,a2,-a3,a0,a1],
                   [a7,a6,-a5,-a4,a3,a2,-a1,a0]])

def right_matrix(v):
  if isinstance(v,(numbers.Real,numbers.Complex)):
    v = Octonion(v)
  elif isinstance(v,Quaternion):
    v = Octonion(q1=v)
  a0,a1,a2,a3,a4,a5,a6,a7 = v.components
  return np.array([[a0,-a1,-a2,-a3,-a4,-a5,-a6,-a7],
                   [a1,a0,a3,-a2,a5,-a4,-a7,a6],
                   [a2,-a3,a0,a1,a6,a7,-a4,-a5],
                   [a3,a2,-a1,a0,a7,-a6,a5,-a4],
                   [a4,-a5,-a6,-a7,a0,a1,a2,a3],
                   [a5,a4,-a7,a6,-a1,a0,-a3,a2],
                   [a6,a7,a4,-a5,-a2,a3,a0,-a1],
                   [a7,-a6,a5,a4,-a3,-a2,a1,a0]])

# Some test values
a = Octonion(3,1,4,1,5,9,2,6)
a10 = a*a*a*a*a*a*a*a*a*a
an = norm(a)
au = a/an
b = Octonion(-3.2,5.3,1.2,math.pi)
bn = norm(b)
bu = b/bn
c = Octonion(q1=Quaternion(-3.2,5.3,1.2,math.pi))
x = np.array([a,b],dtype=oct)
e0 = Octonion(1)
e1 = Octonion(0,1)
e2 = Octonion(0,0,1)
e3 = Octonion(0,0,0,1)
e4 = Octonion(0,0,0,0,1)
e5 = Octonion(0,0,0,0,0,1)
e6 = Octonion(0,0,0,0,0,0,1)
e7 = Octonion(0,0,0,0,0,0,0,1)

# Integration to numpy
A = np.array([[a,b],[c,e3]])
# print('A*A = ',A @ A) # matrix multiplication
# print('A^2 = ',A**2) # not the same result, elementwise
# print('A^3 = ',A**3) # power function applied elementwise
# Note that A @ (A @ A) != (A @ A) @ A even for octonions, while (a*a)*a = a*(a*a)

