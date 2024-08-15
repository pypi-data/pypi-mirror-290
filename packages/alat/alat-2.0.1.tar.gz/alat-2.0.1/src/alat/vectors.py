# Vectors class for ALAT (Advanced Linear Algebra Toolkit)

import math
import random

from .matrices import Matrices
from .errors import (VectorError, ZeroLenghtVector, DimensionError, 
                    ZeroVectorError)

__all__ = ["Vectors"]

class Vectors:
   """ Vector methods for ALAT (Advanced Linnear Algebra Toolkit) """

   def isvector(self, vector: tuple) -> bool:
      """ Return True, if `vector` is in proper defination, otherwise False. """
      if not isinstance(vector, tuple):
         return False
      for el in vector:
         if not isinstance(el, (int, float)):
            return False
         
      return True
   
   def round(self, vector: tuple, digits: int = 6) -> tuple:
      """ Round the all elements of `vector` with `digits`. """
      return tuple(float(round(el, digits)) for el in vector)
   
   def deg(self, rad: float, digits: int = 6) -> float:
      """ Convert the `rad` raidans to degrees. """
      return round(rad * 180.0 / math.pi, digits)

   def rad(self, deg: float, digits: int = 6) -> float: 
      """ Convert the 'deg' degrees to radians. """
      return round(deg * math.pi / 180.0, digits)
   
   def transform(self, vector: tuple, old_coor: str, new_coor: str, 
                 digits: int = 6) -> tuple:
      """ Transform the certain `vector` in which has defined in `old_coor` system 
      into particular new `new_coor` system. Note that all angles in three coordinate 
      systems are in form of degrees and consistent systems are `cartesian`, 
      `cylindrical` and `spherical`. For example: 
      
      >>> car, cyl, sph = 3, 4, 5), (8, 120, 6), (1, 120, 240)
      >>> print(Vectors().transform(car, "cartesian", "cylindrical"))
      (5.0, 53.130102, 5.0)
      >>> print(Vectors().transform(cyl, "cylindrical"", "spherical"))
      (10.0, 53.130102, 120.0)
      >>> print(Vectors().transform(sph, "spherical", "cartesian"))
      (-0.433013, -0.75, -0.5)
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      if not len(vector) == 3:
         raise VectorError("Vector must be three-dimensional")
      
      tvec = [0.0, 0.0, 0.0]
      # Indicate the all possible combinations and then transform it.
      if old_coor == "cartesian" and new_coor == "cartesian":
         tvec[0], tvec[1], tvec[2] = vector[0], vector[1], vector[2]
      elif old_coor == "cartesian" and new_coor == "cylindrical":
         tvec[0] = math.sqrt(pow(vector[0], 2) + pow(vector[1], 2))
         tvec[1] = self.deg(math.atan(vector[1] / vector[0]))
         tvec[2] = vector[2]
      elif old_coor == "cartesian" and new_coor == "spherical":
         tvec[0] = math.sqrt(pow(vector[0], 2) + pow(vector[1], 2) + 
                             pow(vector[2], 2))
         tvec[1] = self.deg(math.acos(vector[2] / tvec[0]))
         tvec[2] = self.deg(math.atan(vector[1] / vector[0]))
      elif old_coor == "cylindrical" and new_coor == "cartesian":
         tvec[0] = vector[0] * math.cos(self.rad(vector[1]))
         tvec[1] = vector[0] * math.sin(self.rad(vector[1]))
         tvec[2] = vector[2]
      elif old_coor == "cylindrical" and new_coor == "cylindrical":
         tvec[0], tvec[1], tvec[2] = vector[0], vector[1], vector[2]
      elif old_coor == "cylindrical" and new_coor == "spherical":
         tvec[0] = math.sqrt(pow(vector[0], 2) + pow(vector[2], 2))
         tvec[1] = self.deg(math.atan(vector[0] / vector[2]))
         tvec[2] = vector[1]
      elif old_coor == "spherical" and new_coor == "cartesian":
         tvec[0] = vector[0] * math.sin(self.rad(vector[1])) * \
            math.cos(self.rad(vector[2])) 
         tvec[1] = vector[0] * math.sin(self.rad(vector[1])) * \
            math.sin(self.rad(vector[2])) 
         tvec[2] = vector[0] * math.cos(self.rad(vector[1]))
      elif old_coor == "spherical" and new_coor == "cylindrical":
         tvec[0] = vector[0] * math.sin(self.rad(vector[1]))
         tvec[1] = vector[2]
         tvec[2] = vector[0] * math.cos(self.rad(vector[1]))
      elif old_coor == "spherical" and new_coor == "spherical":
         tvec[0], tvec[1], tvec[2] = vector[0], vector[1], vector[2]
      else:
         raise ValueError("Consistent coordinate systems are 'cartesian', 'cylindrical'," 
                          " and 'spherical'")

      return self.round(tuple(tvec), digits)
   
   def dim(self, vector: tuple) -> int:
      """ Return the dimension of `vector`. For example: 
      
      >>> result = Vectors().dim(vector=(4, -1, 0, 2))
      >>> print(result)
      4
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      return len(vector)

   def lenght(self, vector: tuple, digits: int = 6) -> float:
      """ Calculate the lenght of `vector` that has defined 
      in cartesian system. For example: 
      
      >>> print(Vectors().lenght(vector=(4, 8, -2, 2)))
      9.380832
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      # Calculate the lenght of 'tvec'.
      res = 0
      for point in vector:
         res += point ** 2

      return round(math.sqrt(res), digits)

   def iszeros(self, vector: tuple) -> bool:
      """ Return True, if `vector` contains just 0s, otherwise return False. """
      if not self.isvector(vector):
         return False
      
      for point in vector:
         if not point == 0.0:
            return False

      return True 

   def isones(self, vector: tuple) -> bool:
      """ Return True, if `vector` contains just 1s, otherwise return False. """
      if not self.isvector(vector):
         return False
      
      for point in vector:
         if not point == 1.0:
            return False

      return True 

   def isequal(self, fvector: tuple, svector: tuple) -> bool:
      """ Return True, if `fvector` and `svector` in same coordinates are
      equal, othwerwise return False. """
      if not self.isvector(fvector) or not self.isvector(svector):
         return False
      if not self.dim(fvector) == self.dim(svector):
         return False
      
      for i in range(0, self.dim(fvector)):
         if not fvector[i] == svector[i]:
            return False
         
      return True
   
   def zeros(self, dim: int) -> tuple:
      """ Create a zeros vector that has `dim` dimension. For example: 
      
      >>> print(Vectors().zeros(dim=4))
      (0.0, 0.0, 0.0, 0.0)
      """
      return tuple(float(0) for x in range(0, dim))

   def ones(self, dim: int) -> tuple:
      """ Create a ones vector that has `dim` dimension. For example: 
      
      >>> print(Vectors().ones(dim=4))
      (1.0, 1.0, 1.0, 1.0)
      """
      return tuple(float(1) for x in range(0, dim))

   def arbitrary(self, value: float, dim: int, digits: int = 6) -> tuple: 
      """ Create a arbitrary vector that has `dim` dimension. For example:
      
      >>> print(Vectors().arbitrary(value=-4.7, dim=5))
      (-4.7, -4.7, -4.7, -4.7, -4.7)
      """
      return tuple(float(round(value, digits)) for x in range(0, dim))
   
   def sequential(self, interval: tuple, dim: int, digits: int = 6) -> tuple:
      """ Create a sequential vector that has `dim` dimension. `interval` 
      determines the interval of new vector. For example: 
      
      >>> print(Vectors().sequential(interval=(0, 4), dim=4))
      (0.0, 1.333333, 2.666667, 4.0)
      """
      # Indicate the step interval and then create a zeros vector.
      step = (interval[1] - interval[0]) / (dim - 1)
      point, vector = interval[0], list(self.zeros(dim=dim))
      # Replace the zeros with sequential points.
      for i in range(dim):
         vector[i] = point
         point += step

      return self.round(vector, digits)

   def random(self, dim: int, digits: int = 6) -> tuple:
      """ Create a random (0-1) vector that has `dim` dimension. For example:
       
      >>> print(Vectors().random(dim=4))
      (0.916623, 0.41082, 0.341974, 0.800275)
      """
      return tuple(round(random.random(), digits) for x in range(dim))

   def uniform(self, interval: tuple, dim: int, digits: int = 6) -> tuple: 
      """ Create a uniform vector that have `dim` dimension. `interval` 
      determines interval that points will fit. For example: 
      
      >>> print(Vectors().uniform(interval=(-5, 5), dim=4))
      (2.619821, -3.925125, 3.175097, -3.49111)
      """
      return tuple(round(random.uniform(interval[0], interval[1]), digits)
                   for x in range(dim))

   def randint(self, interval: tuple, dim: int) -> tuple: 
      """ Create a randint vector that have `dim` dimension. `interval`
      determines interval that points will fit. For example: 
      
      >>> print(Vectors().randint(interval=(-5, 5), dim=4))
      (4.0, 3.0, -5.0, -1.0)
      """
      return tuple(float(random.randint(interval[0], interval[1]))
                   for x in range(dim))
   
   def abs(self, vector: tuple, digits: int = 6) -> tuple:
      """ Get the absolute of `vector` in cartesian coordinate. For example: 
      
      >>> print(Vectors().abs(vector=(4, 0, -1, -2)))
      (4.0, 0.0, 1.0, 2.0)
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      return tuple(round(float(abs(point)), digits) for point in vector)

   def radians(self, vector: tuple, digits: int = 6) -> tuple:
      """ Convert `vector` in cartesian coordinate from degrees to radians. 
      For example: 
   
      >>> print(Vectors().radians(vector=(30, 90, 150, 180)))
      (0.523599, 1.570796, 2.617994, 3.141593)
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      return tuple(round(math.radians(vector[i]), digits) 
                   for i in range(len(vector)))

   def degrees(self, vector: tuple, digits: int = 6) -> tuple:
      """ Convert `vector` in cartesian coordinate from radians to degrees.
      For example: 
      
      >>> print(Vectors().degrees(vector=(0.52, 1.57, 2.62, 3.14)))
      (29.793805, 89.954374, 150.114942, 179.908748)
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      return tuple(round(math.degrees(vector[i]), digits) for i in range(len(vector)))

   def pow(self, vector: tuple, n: int, digits: int = 6) -> tuple: 
      """ Get the `n`th pow of `vector` in cartesian coordinate. For example: 
      
      >>> print(Vectors().pow(vector=(4, 7, -1, 0), n=3))
      print(Vectors().pow(vector=(4, 7, -1, 0), n=3))
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      return tuple(round(pow(vector[i], n), digits) for i in range(len(vector)))

   def root(self, vector: tuple, n: int, digits: int = 6) -> tuple:
      """ Get the `n`th root of `vector` in cartesian coordinate. For example: 
      
      >>> res = Vectors().root(vector=(4, 7, 0, 3), n = 3)
      >>> print(res)
      (1.587401, 1.912931, 0.0, 1.44225)
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      cvet = list(self.zeros(self.dim(vector)))
      for i in range(len(vector)):
         cvet[i] = (vector[i]) ** (1 / n)

      return self.round(tuple(cvet), digits)
   
   def factorial(self, vector: tuple, digits: int = 6) -> tuple:
      """ Get the factorial of `vector` in cartesian coordinate. For example:
        
      >>> result = Vectors().factorial(vector=(4, 7, 1, 0))
      >>> print(result)
      (24.0, 5040.0, 1.0, 1.0)
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")

      cvet = list(self.zeros(self.dim(vector)))
      for i in range(len(vector)):
         cvet[i] = math.factorial(vector[i])

      return self.round(tuple(cvet), digits)

   def log(self, vector: tuple, base: float, digits: int = 6) -> tuple:
      """ Get the logorithm of `vector` with `base` in cartesian coordinate. 
      For example:

      >>> result = Vectors().log(vector=(4, 7, 1, 1), base=2.2)
      >>> print(result)
      (1.758236, 2.467997, 0.0, 0.0)
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      cvet = list(self.zeros(self.dim(vector)))
      for i in range(len(vector)):
         cvet[i] = math.log(vector[i], base)

      return self.round(tuple(cvet), digits)

   def unit(self, vector: tuple, digits: int = 6) -> tuple:
      """ Extract the unit vector from `vector` in cartesian coordinate. 
      For example: 
      
      >>> result = Vectors().unit(vector=(3, 4))
      >>> print(result)
      (0.6, 0.8)
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      matrix, lenght = [list(vector)], self.lenght(vector, digits)
      # To find the unit vector corresponding to 'vector', use Matrices()'.
      if lenght == 0.0:
         ZeroLenghtVector("Zero lenght vector found")
      else:
         cvet = Matrices().scaler_mul(matrix, 1 / lenght, digits)

      return tuple(cvet[0])

   def add(self, fvector: tuple, svector: tuple, digits: int = 6) -> tuple:
      """ Add up the `fvector` and `svector` with each other in cartesian 
      coordinate. For example:

      >>> result = Vectors().add(fvector=(7, -4, 1), svector=(0, -2, 7))
      >>> print(result)
      (7.0, -6.0, 8.0)
      """
      if not self.isvector(fvector) or not self.isvector(svector):
         raise VectorError("Inconsistent vector defination")
      if not self.dim(fvector) == self.dim(svector):
         raise DimensionError("Dimension dismatch found")
      
      return tuple(round(float(fvector[i] + svector[i]), digits) 
                   for i in range(len(fvector)))

   def scaler_mul(self, vector: tuple, scaler: float, digits: int = 6) -> tuple:
      """ Multiply the `scaler` and `vector` in cartesian coordinate. 
      For example: 
      
      >>> result = Vectors().scaler_mul(vector=(7, -2, 5), scaler=-2)
      >>> print(result)
      (-14.0, 4.0, -10.0)
      """
      if not self.isvector(vector):
         raise VectorError("Inconsistent vector defination")
      
      return tuple(round(scaler * vector[i], digits) for i in range(len(vector)))

   def distance(self, fvector: tuple, svector: tuple, digits: int = 6) -> float:
      """ Find the distance between `fvector` and `svector` in cartesian 
      coordinates. For example: 
      
      >>> result = Vectors().distance(fvector=(7, 4), svector=(-1, 3))
      >>> print(result)
      8.062258
      """
      if not self.isvector(fvector) or not self.isvector(svector):
         raise VectorError("Inconsistent vector defination")
      if not self.dim(fvector) == self.dim(svector):
         raise DimensionError("Dimension dismatch found")
      
      distance = 0
      for i in range(len(fvector)):
         distance += (fvector[i] - svector[i]) ** 2

      return round(math.sqrt(distance), digits)

   def dot_mul(self, fvector: tuple, svector: tuple, digits: int = 6) -> float:
      """ Multiply the `fvector` and `svector` with each other in cartesian
      coordinates as dot. For example: 
      
      >>> result = Vectors().cross_mul(fvector=(1, -2), svector=(3, 1))
      >>> print(result)
      1
      """
      if not self.isvector(fvector) or not self.isvector(svector):
         raise VectorError("Inconsistent vector defination")
      if not self.dim(fvector) == self.dim(svector):
         raise DimensionError("Dimension dismatch error")
      
      mul = 0
      for i in range(len(fvector)):
         mul += fvector[i] * svector[i]

      return round(mul, digits)

   def cross_mul(self, fvector: tuple, svector: tuple, digits: int = 6) -> tuple:
      """ Multiply the `fvector` and `svector` with each other in cartesian
      coordinates as cross. For example: 
      
      >>> result = Vectors().cross_mul(fvector=(1, -2, 1), svector=(3, 1, -2))
      >>> print(result)
      (3.0, 5.0, 7.0)
      """
      if not self.isvector(fvector) or not self.isvector(svector):
         raise VectorError("Inconsistent vector defination")
      if not self.dim(fvector) == self.dim(svector) == 3:
         raise DimensionError("Dimension dismatch error")

      return tuple(Matrices().cofactors([[1, 1, 1], list(fvector), list(svector)], 
                                        digits)[0])

   def iscasc(self, fvector: tuple, svector: tuple) -> bool:
      """ Return True, if there is Cauchy-Schwarz inequality, otherwise return False. """
      if self.isvector(fvector) and self.isvector(svector):
         if self.dim(fvector) == self.dim(svector):
            eq1 = abs(self.dot_mul(fvector, svector))
            eq2 = self.dot_mul(fvector, fvector)
            eq3 = self.dot_mul(svector, svector)
            if eq2 * eq3 >= eq1:
               return True
            
      return False

   def istriangle(self, fvector: tuple, svector: tuple) -> bool:
      """ Return True, if there is Triangular inequality, otherwise return False. """
      if self.isvector(fvector) and self.isvector(svector):
         if self.dim(fvector) == self.dim(svector):
            eq1 = self.lenght(self.add(fvector, svector))
            if self.lenght(fvector) + self.lenght(svector) >= eq1:
               return True
            
      return False
            
   def ispythag(self, fvector: tuple, svector: tuple) -> bool:
      """ Return True, if there is Pythagorean inequality, otherwise return False. """
      if self.isvector(fvector) and self.isvector(svector):
         if self.dim(fvector) == self.dim(svector):
            eq1 = self.lenght(self.add(fvector, svector)) ** 2
            if self.lenght(fvector) ** 2 + self.lenght(svector) ** 2 == eq1:
               return True
            
      return False

   def angle(self, fvector: tuple, svector: tuple, form: str, digits: int = 6) -> float:
      """ Find the angle between `fvector` and `svector` in cartesian coordinate. 
      The result can be in three `form`. These are `decimal`, `radians`, and `degrees`.
      For example:

      >>> svector, fvector = (-4, 0, 2, -2), (2, 0, -1, 1)
      >>> print(Vectors().angle(svector, fvector, "decimal"))
      -1.0
      >>> print(Vectors().angle(svector, fvector, "radians"))
      3.141593
      >>> print(Vectors().angle(svector, fvector, "degrees"))
      180.0
      """
      if not self.isvector(fvector) or not self.isvector(svector):
         raise VectorError("Inconsistent vector defination")
      if form not in ("decimal", "radians", "degrees"):
         raise ValueError("Form of angle must be 'decimal', 'radians', or 'degrees'")
      if not self.dim(fvector) == self.dim(svector):
         raise DimensionError("Dimension dismatch found")
      if self.iszeros(fvector) or self.iszeros(svector):
         raise ZeroVectorError("Zero vector found")

      # Multiply the 'fvector' and 'svector' as dot.
      muled, pow1, pow2 = self.dot_mul(fvector, svector, digits), 0, 0
      # Get the pows of each point.
      for point in fvector: pow1 += point ** 2
      for point in svector: pow2 += point ** 2
      # Calculate na dreturn the angle in terms of right form.
      res = round(muled / (math.sqrt(pow1) * math.sqrt(pow2)), digits)
      if form == "decimal":
         return round(res, digits)
      if form == "radians":
         return round(math.acos(res), digits)
      if form == "degrees":
         return round(math.degrees(math.acos(res)), digits)

   def issteep(self, fvector: tuple, svector: tuple) -> bool:
      """ Return True, if `fvector` and `svector` are steep with each other  
      in cartesian coordinate, otherwise, return False. """
      return True if self.angle(fvector, svector, "degrees") == 90.0 else False

   def isparallel(self, fvector: tuple, svector: tuple) -> bool:
      """ Return True, if `fvector` and `svector` are parallel with each other  
      in cartesian coordinate, otherwise, return False. """
      return True if self.angle(fvector, svector, "degrees") == 180.0 else False

