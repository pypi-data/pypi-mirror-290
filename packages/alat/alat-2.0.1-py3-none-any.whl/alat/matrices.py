# Matrices class for ALAT (Advanced Linear Algebra Toolkit)

import math
import random as _random

from .errors import (MatrixError, SquareMatrixError, 
                    DimensionError, MinorsMapError, 
                    CofactorsMapError, InvertibleMatrixError)

__all__ = ["Matrices"]

class Matrices:
   """ Matrix methods in ALAT (Advanced Linear Algebra Toolkit) """

   def ismatrix(self, matrix: list[list]) -> bool:
      """ Check if the `matrix` is defined appropriately. """
      # Outher form must be in 'list' data type.
      if not isinstance(matrix, list):
         return False
      # Inner form must be in 'list' data type as well.
      for row in matrix:
         if not isinstance(row, list):
            return False
         # Each entity of matrix must be in 'int' or 'float' data type.
         for entity in row:
            if not isinstance(entity, (int, float)):
               return False
         # Each row has the same lenght.
         if not len(row) == len(matrix[0]):
            return False
            
      return True
   
   def issquare(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` is square, otherwise return False. """
      return True if self.ismatrix(matrix) and len(matrix) == len(matrix[0]) else False
            
   def shape(self, matrix: list[list]) -> tuple:
      """ Return the dimension of `matrix`. For example:

      >>> matrix = [
         [4, 7, 3], 
         [0, 1, 9]
      ]
      >>> result = Matrices().shape(matrix)
      >>> print(result)
      (2, 3)
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")

      return (len(matrix), len(matrix[0])) # (row, col)
   
   def copy(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Copy the 'matrix' into new matrix. """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Copy the all elements of 'matrix'.
      cmatrix = self.zeros(self.shape(matrix))
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            cmatrix[i][j] = round(float(matrix[i][j]), digits)

      return cmatrix

   def diagonal(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Return the diagonal section of `matrix`. For example:

      >>> matrix = [
         [4, 3, 0], 
         [1, 5, 7], 
         [0, 3, 8]
      ] 
      >>> result = Matrices().diagonal(matrix)
      >>> print(result)

      [[4.0, 5.0,  8.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      if not self.issquare(matrix):
         raise SquareMatrixError("Inconsistent square matrix defination")
      
      return [[float(round(matrix[i][i], digits)) for i in range(len(matrix))]]

   def ishomogen(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` is homogen matrix, otherwise return False. """
      if not self.ismatrix(matrix):
         return False
      
      # Homogeneneous matrix contains zeros in the last of each row.
      for i in range(len(matrix[0])):
         if matrix[i][-1] != 0.0:
            return False
      
      return True

   def iszeros(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` is zeros matrix, otherwise return False. """
      if not self.ismatrix(matrix):
         return False
      
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            if matrix[i][j] != 0.0:
               return False
            
      return True

   def isones(self, matrix: list[list]) -> bool: 
      """ Return True, if `matrix` is ones matrix, otherwise return False. """
      if not self.ismatrix(matrix):
         return False
      
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            if matrix[i][j] != 1.0:
               return False
            
      return True

   def isidentity(self, matrix: list[list]) -> bool: 
      """ Return True, if `matrix` is identity matrix, otherwise return False. """
      if not self.issquare(matrix):
         return False
      
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
               return False
            
      return True
   
   def zeros(self, shape: tuple) -> list[list]: 
      """ Create a new zeros matrix. For example: 
      
      >>> result = Matrices().zeros(shape=(2, 3))
      >>> print(result)
      [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
      """
      if not isinstance(shape, tuple):
         raise TypeError("'shape' must be tuple")
      if not len(shape) == 2:
         raise ValueError("'shape' must just contain row and column values")
      
      return [[float(0) for x in range(shape[1])] for x in range(shape[0])]

   def ones(self, shape: tuple) -> list[list]: 
      """ Create a new ones matrix. For example: 
      
      >>> result = Matrices().ones(shape=(2, 3))
      >>> print(result)
      [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
      """
      if not isinstance(shape, tuple):
         raise TypeError("'shape' must be tuple")
      if not len(shape) == 2:
         raise ValueError("'shape' must just contains row and column values")
      
      return [[float(1) for x in range(shape[1])] for x in range(shape[0])]

   def identity(self, shape: tuple) -> list[list]: 
      """ Create a new identity matrix. For example: 
      
      >>> result = Matrices().identity(shape=(3, 3))
      >>> print(result)
      [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
      """
      if not isinstance(shape, tuple):
         raise TypeError("'shape' must be tuple")
      if not len(shape) == 2:
         raise ValueError("'shape' must just contains row and column values")
      if not shape[0] == shape[1]:
         raise SquareMatrixError("Matrix that will be created must be square")
      
      # Derivate the identity matrix from zeros matrix.
      matrix = self.zeros(shape=shape)
      # Replace the main diagonal of 'matrix' with 1s.
      for i in range(len(matrix)):
         matrix[i][i] = 1.0

      return matrix

   def arbitrary(self, value: float, shape: tuple) -> list[list]:
      """ Create a new arbitrary matrix. For example:  
      
      >>> result = Matrices().arbitrary(value=4, shape=(2, 3))
      >>> print(result)
      [[4.0, 4.0, 4.0], [4.0, 4.0, 4.0]]
      """
      if not isinstance(shape, tuple):
         raise TypeError("'shape' must be tuple")
      if not len(shape) == 2:
         raise ValueError("'shape' must just contains row and column values")
      
      return [[float(value) for x in range(shape[1])] for x in range(shape[0])]

   def sequential(self, interval: tuple, shape: tuple, digits: int = 6) -> list[list]:
      """ Create a new sequential matrix. For example: 
      
      >>> matrices = Matrices().sequential(interval=(1, 10), shape=(2, 5))
      >>> print(result)
      [[1, 2.0, 3.0, 4.0, 5.0], [6.0, 7.0, 8.0, 9.0, 10.0]]
      """
      if not isinstance(shape, tuple) or not isinstance(interval, tuple):
         raise TypeError("'hape' and 'interval' must be tuple")
      if not len(shape) == 2 or not len(interval) == 2:
         raise ValueError("'shape' and 'interval' must just contains row and column values")
      
      # Indicate the step interval and create a new zeros matrix.
      step = (interval[1] - interval[0]) / (shape[0] * shape[1] - 1)
      matrix = self.zeros(shape=shape)
      # Start replacing with first interval step.
      el = interval[0]
      # Replace the all elements with new values.
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            matrix[i][j] = round(el, digits)
            el += step

      return matrix

   def random(self, shape: tuple, digits: int = 6) -> list[list]:
      """ Create a new random matrix. For example: 
      
      >>> result = Matrices().random(shape=(2, 3))
      >>> print(result)
      [[0.982888, 0.360174, 0.832604], [0.044411, 0.562919, 0.324173]]
      """
      if not isinstance(shape, tuple):
         raise TypeError("'shape' must be tuple")
      if not len(shape) == 2:
         raise ValueError("'shape' must just contain row and column values")
      
      # Initially create any kind of matrix and then replace its elements with new.
      matrix = self.zeros(shape=shape)
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            matrix[i][j] = round(_random.random(), digits)

      return matrix

   def uniform(self, interval: tuple, shape: tuple, digits: int = 6) -> list[list]:
      """ Create a new uniform matrix. For example: 
      
      >>> result = Matrices().uniform(interval=(1, 10), shape=(2, 4))
      >>> print(result)
      [[6.630704, 2.8935, 9.52904, 5.755943], [9.13, 1.763477, 7.205818, 2.732938]]
      """
      if not isinstance(shape, tuple) or not isinstance(interval, tuple):
         raise TypeError("'shape' and 'interval' must be tuple")
      if not len(shape) == 2 or not len(interval) == 2:
         raise ValueError("'shape' and 'interval' must just contain row and column values")
      
      # Create a zero matrix and then replace its elements with uniform numbers.
      matrix = self.zeros(shape=shape)
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            matrix[i][j] = round(_random.uniform(interval[0], interval[1]), digits)

      return matrix

   def randint(self, interval: tuple, shape: tuple) -> list[list]:
      """ Create a new randint matrix. For example: 
      
      >>> result = Matrices().randint(interval=(-5, 5), shape=(4, 3))
      >>> print(result)
      [[-5.0, -5.0, -3.0], [-1.0, 4.0, 5.0], [-3.0, 4.0, -4.0], [-3.0, 3.0, -5.0]]
      """
      if not isinstance(shape, tuple) or not isinstance(interval, tuple):
         raise TypeError("'shape' and 'interval' must be tuple")
      if not len(shape) == 2 or not len(interval) == 2:
         raise ValueError("'shape' and 'interval' must just contain row and column values")
      
      # Create a zero matrix and then replace its elements with randint numbers.
      matrix = self.zeros(shape=shape)
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            matrix[i][j] = float(_random.randint(interval[0], interval[1]))

      return matrix
 
   def max(self, matrix: list[list], digits: int = 6) -> float: 
      """ Find the highest element in `matrix`. For example: 
      
      >>> matrix = [
         [4, 7, 3], 
         [0, 7, 9], 
         [3, 6, 7]
      ]
      >>> result = Matrices().max(matrix)
      >>> print(result)
      9.0
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      return round(float(max(el for row in matrix for el in row)), digits)

   def min(self, matrix: list[list], digits: int = 6) -> float: 
      """ Find the lowest element in `matrix`. For example:

      >>> matrix = [
         [4, 7, 3], 
         [0, 7, 9], 
         [3, 6, 7]
      ]
      >>> result = Matrices().min(matrix)
      >>> print(result)
      0.0
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defintion")
      
      return round(float(min(el for row in matrix for el in row)), digits)

   def elmax(self, matrix: list[list]) -> tuple:
      """ Return the index of first highest element in 'matrix'. For example:
      
      >>> matrix = [
         [7, 4, -1], 
         [8, -4, 0]
      ]
      >>> result = Matrices().elmax(matrix)
      >>> print(result)
      (1, 0)
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Find the index of first highest matrix.
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            if round(float(matrix[i][j]), 6) == self.max(matrix):
               return tuple([i, j])
            
   def elmin(self, matrix: list[list]) -> tuple:
      """ Return the index of first lowest element in `matrix`. For example:
      
      >>> matrix = [
         [7, 4, -1], 
         [8, -4, 0]
      ]
      >>> result = Matrices().elmin(matrix)
      >>> print(result)
      (1, 1)
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Find the index of first highest matrix.
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            if round(float(matrix[i][j]), 6) == self.min(matrix):
               return tuple([i, j])

   def mean(self, matrix: list[list], digits: int = 6) -> float: 
      """ Calculate the mean of `matrix`. For example: 
      
      >>> matrix = [
         [5, 7, 1], 
         [4, 1, 2], 
         [8, -5, 8]
      ]
      >>> result = Matrices().mean(matrix)
      >>> print(result)
      3.444444
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      return round(sum([el for row in matrix for el in row]) / 
                   (len(matrix) * len(matrix[0])), digits)

   def sort(self, matrix: list[list], reverse: bool = False, digits: int = 6) -> list[list]:
      """ Sort the elements of `matrix` ascendingly. If `reverse` is True, 
      and then sort descendingly. For example: 
          
      >>> matrix = [
         [5, 7, 1], 
         [4, 1, 2], 
         [8, -5, 8]
      ]
      >>> result = Matrices().sort(matrix, True)
      >>> print(result)
      [[8, 8, 7], [5, 4, 2], [1, 1, -5]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Collect the all elements of 'matrix', and then sort it.
      els = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix[0]))]
      els.sort(reverse=reverse)
      # Again, to gather them together, firstly create a new zeros matrix, 
      # and then replace its elements with sorted sole elements.
      ordered, index = self.zeros(self.shape(matrix)), 0
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            ordered[i][j] = round(els[index], digits)
            index += 1

      return ordered
   
   def stddev(self, matrix: list[list], digits: int = 6) -> float: 
      """ Calculate the standard deviation of `matrix`. For example: 
      
      >>> matrix = [
         [5, 7, 1], 
         [4, 1, 2], 
         [8, -5, 8]
      ]
      >>> result = Matrices().stddev(matrix)
      >>> print(result)
      3.975232
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Calculate the mean of 'matrix', and calculate standard deviation.
      mean, tpow = self.mean(matrix, digits), 0
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            tpow += pow(abs(mean - matrix[i][j]), 2)

      return round(math.sqrt(tpow / (len(matrix) * len(matrix[0]))), digits)

   def mode(self, matrix: list[list], digits: int = 6) -> tuple:
      """ Return the mode or modes of `matrix`. If there is not any mode/s, in this 
          case, return empty tuple. For example:
          
      >>> matrix = [
         [5, 7, 1], 
         [4, 1, 2], 
         [8, -5, 8]
      ]
      >>> result = Matrices().mode(matrix)
      >>> print(result)
      (1.0, 8.0)
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Mode means the value/s which repeats mostly.
      els = [el for row in matrix for el in row]
      repeated = {value: els.count(value) for value in els}
      # Create a new empty list and fill in it with mode/s, and then convert it tuple.
      modes = list()
      for key, value in repeated.items():
         if repeated[key] == max(repeated.values()):
            modes.append(round(float(key), digits))

      return tuple(modes)

   def median(self, matrix: list[list], digits: int = 6) -> float:
      """ Return the median elements of `matrix`. For example: 
      
      >>> matrix = [
         [5, 7, 1], 
         [4, 1, 2], 
         [8, -5, 8]
      ]
      >>> result = Matrices().median(matrix)
      >>> print(result)
      2.0
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Pool the all elements of 'matrix' and sort it.
      els = [el for row in matrix for el in row]
      els.sort()
      # Calculate the median.
      if len(els) % 2 == 1:
         return round(float(els[round(len(els) / 2) -1]), digits)
      else:
         p1, p2 = int(len(els) / 2 - 1), int(len(els) / 2)
         return round((els[p1] + els[p2]) / 2, digits)

   def aggregate(self, matrix: list[list], axis: int = 0, digits: int = 6) -> list[list]: 
      """ Aggregate the `matrix` according to `axis`. `axis` must be 0 (horizontal) or 
          1 (vertical). For example: 
          
      >>> matrix = [
         [5, 7, 1], 
         [4, 1, 2]
      ]
      >>> result = Matrices().aggregate(matrix, 0) # as horizontally
      >>> print(result)
      [[9.0, 8.0, 3.0]]
      >>> result = Matrices().aggregate(matrix, 1) # as vertically
      >>> print(result)
      [[13.0], [7.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      if not axis in (0, 1):
         raise ValueError("'axis' must be 0 (horizontal) or 1 (vertical)")
      
      total = 0
      # Aggregate the 'matrix' as horizontally.
      if axis == 0:
         # Create the zeros matrix and replace the elements.
         aggregated = self.zeros(shape=(1, len(matrix[0])))
         for i in range(len(matrix[0])):
            for row in matrix:
               total += row[i]
            # Put aggregated elements in 'aggregated'.
            aggregated[0][i] = round(float(total), digits)
            total = 0
      # Aggregate the 'matrix' as vertically.
      else:
         # Create the zeros matrix and replace the elements.
         aggregated = self.zeros(shape=(len(matrix), 1))
         for i in range(len(matrix)):
            for j in range(len(matrix[0])):
               total += matrix[i][j]
            # Put aggregated elements in 'aggregated'.
            aggregated[i][0] = round(float(total), digits)
            total = 0

      return aggregated

   def iselementary(self, matrix: list[list]) -> bool: 
      """ Return True, if `matrix` is elementary matrix, otherwise return False. """
      # Elementary matrix must be square form.
      if not self.ismatrix(matrix):
         return False
      
      diffs = list()
      # Create an identity matrix and then compare both matrices.
      identity = self.identity(self.shape(matrix))
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            if not matrix[i][j] == identity[i][j]:
               diffs.append(matrix[i][j])
      
      # If identity matrix was changed by one operation, in this case:
      if len(diffs) == 1 and diffs[0] != 0:
         return True
      
      # If the row of main matrix was changed with each other, in this case:
      if self.ones(shape=(1, len(matrix))) == self.aggregate(matrix, 0):
         return True
      
      return False

   def shuffle(self, matrix: list[list], digits: int = 6) -> list[list]: 
      """ Shuffle the  `matrix` randomly. For example: 
      
      >>> matrix = [
         [5, 7, 1], 
         [4, 1, 2]
      ]
      >>> result = Matrices().shuffle(matrix)
      >>> print(result)
      [[2.0, 1.0, 5.0], [1.0, 7.0, 4.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Collect the all elements of 'matrix' and shuffle it randomly. 
      gathered = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix[0]))]
      _random.shuffle(gathered)

      shuffled, index = self.zeros(self.shape(matrix)), 0
      # Again, collect the all elements together into new matrix.
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            shuffled[i][j] = round(float(gathered[index]), digits)
            index += 1

      return shuffled
   
   def abs(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Get the absolute of 'matrix'. For example: 

      >>> matrix = [
         [7, -2, 0], 
         [-8, 7, 1]
      ]
      >>> result = Matrices().abs(matrix)
      >>> print(result)
      [[7.0, 2.0, 0.0], [8.0, 7.0, 1.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      cmat = self.zeros(shape=self.shape(matrix))
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            cmat[i][j] = round(float(abs(matrix[i][j])), digits)

      return cmat

   def reshape(self, matrix: list[list], shape: tuple, digits: int = 6) -> list[list]:
      """ Reshape the `matrix` with new shapeension. The new shapeension will be
          determined using `shape`. For example: 
      
      >>> matrix = [
         [5, 7, 1], 
         [4, 1, 2]
      ]
      >>> result = Matrices().reshape(matrix, (1, 6))
      >>> print(result)
      [[5.0, 7.0, 1.0, 4.0, 1.0, 2.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      if not isinstance(shape, tuple):
         raise TypeError("'shape' must be tuple")
      if not len(shape) == 2:
         raise ValueError("'shape' must just contain row and column values")
      if not len(matrix) * len(matrix[0]) == shape[0] * shape[1]:
         raise DimensionError("Dimension mismatch found")
      
      # Collect the all elements of 'matrix' into a array.
      index = 0
      els = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix[0]))]
      # Create a new zeros matrix with new shape, and then replace its elements.
      reshaped = self.zeros(shape)
      for i in range(shape[0]):
         for j in range(shape[1]):
            reshaped[i][j] = round(float(els[index]), digits)
            index += 1

      return reshaped

   def transpose(self, matrix: list[list], digits: int = 6) -> list[list]: 
      """ Get the transpose of `matrix`. For example: 
      
      >>> matrix = [
         [5, 7, 1], 
         [4, 1, 2]
      ]
      >>> result = Matrices().transpose(matrix)
      >>> print(result)
      [[5.0, 4.0], [7.0, 1.0], [1.0, 2.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Change the rows and columns in turn.
      trans = self.zeros((len(matrix[0]), len(matrix)))
      for j in range(len(matrix[0])):
         for i in range(len(matrix)):
            trans[j][i] = round(float(matrix[i][j]), digits)

      return trans

   def concat(self, fmatrix: list[list], smatrix: list[list], axis: int = 0, 
              digits: int = 6) -> list[list]:
      """ Concatenate `fmatrix` and `smatrix` according to `axis`. `axis` 
          must be 0 (horizontally) or 1 (vertically). For example: 
          
      >>> fmatrix = [
         [0, 1], 
         [1, 5]
      ]
      >>> smatrix = [
         [1, 0], 
         [0, 1]
      ]
      >>> result = Matrices().concat(fmatrix, smatrix, 0) # as horizontal
      >>> print(result)
      [[0.0, 1.0], [1.0, 5.0], [1.0, 0.0], [0.0, 1.0]]

      >>> result = Matrices().concat(fmatrix, smatrix, 1) # as vertical
      >>> print(result)
      [[0.0, 1.0, 1.0, 0.0], [1.0, 5.0, 0.0, 1.0]]
      """
      if not self.ismatrix(fmatrix) or not self.ismatrix(smatrix):
         raise MatrixError("Inconsistent matrix defination")
      if not axis in (0, 1):
         raise ValueError("'axis' must be 0 (horizontal) or 1 (vertical)")
      if (axis == 0 and not len(fmatrix[0]) == len(smatrix[0])) or (axis == 1 \
          and not len(fmatrix) == len(smatrix)):
         raise DimensionError("Dimension dismatch found")
      
      # Copy the 'fmatrix' as a new matrix.
      matrix = self.copy(fmatrix, digits)
      # Concatenate the matrices as horizontal.
      if axis == 0:
         for row in smatrix:
            matrix.append(row)
      # Concatenate the matrices as vertical.
      if axis == 1:
         for i in range(len(matrix)):
            matrix[i] = matrix[i] + smatrix[i]
      # Shape the elements of result concatenated matrix.
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            matrix[i][j] = round(float(matrix[i][j]), digits)

      return matrix
   
   def islowertri(self, matrix: list[list]) -> bool: 
      """ Return True, if `matrix` is lower triangular, otherwise return False. """
      if not self.issquare(matrix):
         return False
      # Check the elements of upper triangular portion of 'matrix'.
      for i in range(len(matrix) - 1):
         for el in matrix[i][i + 1:]:
            if not el == 0.0:
               return False
            
      return True
      
   def isuppertri(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` is upper triangular, otherwise return False. """
      return True if self.islowertri(self.transpose(matrix)) else False

   def istriangle(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` is triangular, otherwise return False. """
      return True if self.islowertri(matrix) or self.isuppertri(matrix) else False

   def add(self, fmatrix: list[list], smatrix: list[list], digits: int = 6) -> list[list]:
      """ Add up the `fmatrix` and `smatrix` with each other. For example: 
      
      >>> fmatrix = [
         [0, 1], 
         [1, 5]
      ]
      >>> smatrix = [
         [1, 0], 
         [0, 1]
      ]
      >>> result = Matrices().add(fmatrix, smatrix)
      >>> print(result)
      [[1.0, 1.0], [1.0, 6.0]]
      """
      if not self.ismatrix(fmatrix) or not self.ismatrix(smatrix):
         raise MatrixError("Inconsistent matrix defination")
      if not self.shape(fmatrix) == self.shape(smatrix):
         raise DimensionError("Dimension dismatch found")
      
      # Create a new zeros matrix, and then add the elements with each other.
      matrix = self.zeros(self.shape(fmatrix))
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            matrix[i][j] = round(float(fmatrix[i][j] + smatrix[i][j]), digits)

      return matrix
   
   def scaler_mul(self, matrix: list[list], scaler:float, digits: int = 6) -> list[list]:
      """ Multiply the `scaler` and `matrix` with each other. For example: 
      
      >>> matrix = [
         [5, 0, 4], 
         [2, 1, -4], 
         [9, 9, 0]
      ]
      >>> result = Matrices().scaler_mul(matrix, -4.8)
      >>> print(result)
      [[-24.0, -0.0, -19.2], [-9.6, -4.8, 19.2], [-43.2, -43.2, -0.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Copy the 'matrix', and then multiply its elements with 'scaler'.
      muled = self.copy(matrix, digits)
      for i in range(len(muled)):
         for j in range(len(muled[0])):
            muled[i][j] = round(float(muled[i][j] * scaler), digits)

      return muled

   def subtract(self, fmatrix: list[list], smatrix: list[list], 
                digits: int = 6) -> list[list]:
      """ Subtract the `smatrix` from `fmatrix`. For example: 
      
      >>> fmatrix = [
         [5, 0, 4], 
         [2, 1, -4], 
         [9, 9.5, 0]
      ]
      >>> smatrix = [
         [5, 0, 4], 
         [2, 1, -4], 
         [9, 9.5, 0]
      ]
      >>> result = Matrices().subtract(fmatrix, smatrix)
      >>> print(result)
      [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
      """
      return self.add(fmatrix, self.scaler_mul(smatrix, -1.0), digits)

   def dot_mul(self, fmatrix: list[list], smatrix: list[list], 
               digits: int = 6) -> list[list]:
      """ Multiply the `fmatrix` and `smatrix` as dot. For example: 
      
      >>> fmatrix = [
         [-4, 1], 
         [1, 5]
      ]
      >>> smatrix = [
         [1, 9], 
         [8, -1]
      ]
      >>> result = Matrices().dot_mul(fmatrix, smatrix)
      >>> print(result)
      [[-4.0, 9.0], [8.0, -5.0]]
      """
      if not self.ismatrix(fmatrix) or not self.ismatrix(smatrix):
         raise MatrixError("Inconsistent matrix defination")
      if not self.shape(fmatrix) == self.shape(smatrix):
         raise DimensionError("Dimension dismatch found")
      
      # Create a new zeros matrix and then relapce its elements with news.
      muled = self.zeros(self.shape(fmatrix))
      for i in range(len(muled)):
         for j in range(len(muled[0])):
            muled[i][j] = round(float(fmatrix[i][j] * smatrix[i][j]), digits)

      return muled

   def cross_mul(self, fmatrix: list[list], smatrix: list[list], 
                 digits: int = 6) -> list[list]: 
      """ Multiply the `fmatrix` and `smatrix` as cross. For example: 
      
      >>> fmatrix = [
         [-4, 1], 
         [1, 5],
         [-5, 7]
      ]
      >>> smatrix = [
         [1, 9, 8], 
         [8, -1, 8]
      ]
      >>> result = Matrices().cross_mul(fmatrix, smatrix)
      >>> print(result)
      [[4.0, -37.0, -24.0], [41.0, 4.0, 48.0], [51.0, -52.0, 16.0]]
      """
      if not self.ismatrix(fmatrix) or not self.ismatrix(smatrix):
         raise MatrixError("Inconsistent matrix defination")
      if not len(fmatrix[0]) == len(smatrix):
         raise DimensionError("Dimension dismatch found")
      
      # Create the new matrices using 'fmatrix' and 'smatrix'.
      matrix = self.zeros(shape=(len(fmatrix), len(smatrix[0])))
      smatrix = self.transpose(smatrix)
      total = 0
      # Multiply the elements of new matrices as cross.
      for i in range(len(matrix)):
         for j in range(len(smatrix)):
            for k in range(len(smatrix[0])):
               total += fmatrix[i][k] * smatrix[j][k]
            matrix[i][j] = round(float(total), digits)
            total = 0

      return matrix
            
   def scaler_div(self, matrix: list[list], scaler: float, digits: int = 6):
      """ Divide the `scaler` to `matrix`. For example: 
      
      >>> matrix = [
         [1, 9, 8], 
         [8, -1, 8]
      ]
      >>> result = Matrices().scaler_div(matrix, -2)
      >>> print(result)
      [[-0.5, -4.5, -4.0], [-4.0, 0.5, -4.0]]
      """
      return self.scaler_mul(matrix, 1 / scaler, digits)

   def pow(self, matrix: list[list], n: float, digits: int = 6) -> list[list]:
      """ Get the `n`th. pow of `matrix`. For example: 
      
      >>> matrix = [
         [-4, 1, 2], 
         [1, 5, 7]
      ]
      >>> result = Matrices().pow(matrix, 2.0)
      >>> print(result)
      [[16.0, 1.0, 4.0], [1.0, 25.0, 49.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Create a new zeros matrix and then replace its elements with new.
      powed = self.zeros(self.shape(matrix))
      for i in range(len(powed)):
         for j in range(len(powed[0])):
            powed[i][j] = round(float(matrix[i][j] ** n), digits)

      return powed 

   def root(self, matrix: list[list], n: float, digits: int = 6) -> list[list]:
      """ Get the `n`th. root of `matrix`. For example:
      
      >>> matrix = [
         [4, 1, 2], 
         [1, 5, 7]
      ]
      >>> result = Matrices().root(matrix, 3.2)
      >>> print(result)
      [[1.542211, 1.0, 1.241858], [1.0, 1.653591, 1.836932]]
      """ 
      return self.pow(matrix, (1 / n), digits)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
   def factorial(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Get the factorial of `matrix`. For example:                                         
      
      >>> matrix = [
         [4, 1, 2], 
         [1, 5, 7]
      ]
      >>> result = Matrices().factorial(matrix)                                       
      >>> print(result)
      [[24.0, 1.0, 2.0], [1.0, 120.0, 5040.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Create a new matrix and then replace its elements with news.
      facted = self.zeros(self.shape(matrix))
      for i in range(len(facted)):
         for j in range(len(facted[0])):
            facted[i][j] = round(float(math.factorial(matrix[i][j])), digits)

      return facted

   def log(self, matrix: list[list], base: float, digits: int = 6) -> list[list]:
      """ Get the logorithm of `matrix` with base `base`. For example: 
      
      >>> matrix = [
         [4, 10, 2], 
         [10, 5, 7]
      ]
      >>> result = Matrices().log(matrix, 10.0)
      >>> print(result)
      [[0.60206, 1.0, 0.30103], [1.0, 0.69897, 0.845098]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Create a new matrix and then replace it with calculated new elements.
      loged = self.zeros(self.shape(matrix))
      for i in range(len(loged)):
         for j in range(len(loged[0])):
            loged[i][j] = round(math.log(matrix[i][j], base), digits)
            
      return loged
   
   def swap(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Get the swap of `matrix`. For example: 
      
      >>> matrix = [
         [4, 1, 2], 
         [1, 0, 7]
      ]
      >>> result = Matrices().swap(matrix)
      >>> print(result)
      [[0.25, 1.0, 0.5], [1.0, 2.5, 0.142857]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Create a new zeros matrix and then replace its elements with news.
      revered = self.zeros(self.shape(matrix))
      for i in range(len(matrix)):
         for j in range(len(matrix[0])): 
            revered[i][j] = round(1 / matrix[i][j], digits) 

      return revered

   def sin(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Calculate the sine of `matrix` (in radians). For example: 
      
      >>> matrix = [
         [4, 10, 2], 
         [10, 5, 7]
      ]
      >>> result = Matrices().sin(matrix)
      >>> print(result)
      [[-0.756802, -0.544021, 0.909297], [-0.544021, -0.958924, 0.656987]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Create a new matrix and then replace its elements.
      sinus = self.zeros(self.shape(matrix))
      for i in range(len(sinus)):
         for j in range(len(sinus[0])):
            sinus[i][j] = round(math.sin(matrix[i][j]), digits)

      return sinus
   
   def cos(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Calculate the cosine of `matrix` (in radians). For example:
      
      >>> matrix = [
         [4, 10, 2], 
         [10, 5, 7]
      ]
      >>> result = Matrices().cos(matrix)
      >>> print(result) 
      [[-0.653644, -0.839072, -0.416147], [-0.839072, 0.283662, 0.753902]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matix defination")

      # Create a new matrix and then replace its elements.
      cosinus = self.zeros(self.shape(matrix))
      for i in range(len(cosinus)):
         for j in range(len(cosinus[0])):
            cosinus[i][j] = round(math.cos(matrix[i][j]), digits)

      return cosinus 

   def tan(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Calculate the tangent of `matrix` (in radians). For example: 
      
      >>> matrix = [
         [4, 10, -2], 
         [10, -5, 7]
      ]
      >>> result = Matrices().tan(matrix)
      >>> print(result)
      [[1.157821, 0.648361, 2.18504], [0.648361, 3.380515, 0.871448]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Create a new matrix and then replace its elements.
      tangent = self.zeros(self.shape(matrix))
      for i in range(len(tangent)):
         for j in range(len(tangent[0])):
            tangent[i][j] = round(math.tan(matrix[i][j]), digits)

      return tangent

   def cot(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Calculate the cotangent of `matrix` (in radians). For example: 
      
      >>> matrix = [
         [4, 10, -2], 
         [10, -5, 7]
      ]
      >>> result = Matrices().cot(matrix)
      >>> print(result)
      [[0.863691, 1.542351, 0.457658], [1.542351, 0.295813, 1.147515]]
      """
      return self.swap(self.tan(matrix, digits), digits)

   def sec(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Calculate the sekant of `matrix` (in radians). For example: 
      
      >>> matrix = [
         [4, 10, -2], 
         [10, -5, 7]
      ]
      >>> result = Matrices().sec(matrix)
      >>> print(result)
      [[-1.529885, -1.191793, -2.402997], [-1.191793, 3.525322, 1.326432]]
      """
      return self.swap(self.cos(matrix, digits), digits)

   def cosec(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Calculate the cosekant of `matrix` (in radians). For example: 
      
      >>> matrix = [
         [4, 10, -2], 
         [10, -5, 7]
      ]
      >>> result = Matrices().cosec(matrix)
      >>> print(result)
      [[-1.32135, -1.838164, -1.099751], [-1.838164, 1.042836, 1.5221]]
      """
      return self.swap(self.sin(matrix, digits), digits)

   def asin(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Calculate the arc sine of `matrix` (in radians). For example:  
      
      >>> matrix = [
         [0.4, 0.1, -0.2], 
         [0.1, -0.5, 0.7]
      ]
      >>> result = Matrices().asin(matrix)
      >>> print(result)
      [[0.411517, 0.100167, -0.201358], [0.100167, -0.523599, 0.775397]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Iconsistent matrix defination")
      
      # Create a new matrix and get it arc sine.
      arcsin = self.zeros(self.shape(matrix))
      for i in range(len(arcsin)):
         for j in range(len(arcsin[0])):
            arcsin[i][j] = round(math.asin(matrix[i][j]), digits)
         
      return arcsin

   def acos(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Calculate the arc cosine of `matrix` (in radians). For example:
       
      >>> matrix = [
         [0.4, 0.1, -0.2], 
         [0.1, -0.5, 0.7]
      ]
      >>> result = Matrices().acos(matrix)
      >>> print(result)
      [[1.159279, 1.470629, 1.772154], [1.470629, 2.094395, 0.795399]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")

      # Create a new matrix and then replace its elements.
      arccos = self.zeros(self.shape(matrix))
      for i in range(len(arccos)):
         for j in range(len(arccos[0])):
            arccos[i][j] = round(math.acos(matrix[i][j]), digits)
            
      return arccos
   
   def atan(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Calculate the arc tangent of `matrix` (in radians). For example: 
      
      >>> matrix = [
         [0.4, 0.1, -0.2], 
         [0.1, -0.5, 0.7]
      ]
      >>> result = Matrices().atan(matrix)
      >>> print(result)
      [[0.380506, 0.099669, -0.197396], [0.099669, -0.463648, 0.610726]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      
      # Create a new matrix and then replace its elements.
      arctan = self.zeros(self.shape(matrix))
      for i in range(len(arctan)):
         for j in range(len(arctan[0])):
            arctan[i][j] = round(math.atan(matrix[i][j]), digits)
            
      return arctan

   def degrees(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Convert the `matrix` from radians into degrees. For example: 
      
      >>> matrix = [
         [5, 0.1, -0.4], 
         [0.6, -0.3, 0.7]
      ]
      >>> result = Matrices().degrees(matrix)
      >>> print(result)
      [[286.478898, 5.729578, -22.918312], [34.377468, -17.188734, 40.107046]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")

      # Create a new matrix and then replace its elements.
      deg = self.zeros(self.shape(matrix))
      for i in range(len(deg)):
         for j in range(len(deg[0])):
            deg[i][j] = round(math.degrees(matrix[i][j]), digits)

      return deg
   
   def radians(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Convert the `matrix` from degrees to radians. For example: 
      
      >>> matrix = [
         [22.918312, 5.729578, -11.459156], 
         [5.729578, -28.64789, 40.107046]
      ]
      >>> result = Matrices().radians(matrix)
      >>> print(result)
      [[0.4, 0.1, -0.2], [0.1, -0.5, 0.7]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")

      # Create a new matrix and then replace its elements.
      rad = self.zeros(self.shape(matrix))
      for i in range(len(rad)):
         for j in range(len(rad[0])):
            rad[i][j] = round(matrix[i][j] * math.pi / 180, digits)

      return rad
   
   def dot_div(self, fmatrix: list[list], smatrix: list[list], 
               digits: int = 6) -> list[list]:
      """ Divide the `fmatrix` to `smatrix` as dot. If zero divison error
      occurs, and the replace element that caused zero division with mean of 
      `smatrix`. For example: 
      
      >>> fmatrix = [
         [4, 1, 2], 
         [1, 5, 7],
      ]
      >>> smatrix = [
         [1, 0, 8], 
         [8, -1, 8]
      ]
      >>> result = Matrices().dot_div(fmatrix, smatrix)
      >>> print(result)
      [[4.0, 0.25, 0.25], [0.125, -5.0, 0.875]]
      """ 
      return self.dot_mul(fmatrix, self.swap(smatrix, digits), digits) 

   def det(self, matrix: list[list], digits: int = 6) -> float:
      """ Calculate the determinant of `matrix`. For example: 
         
      >>> matrix = [
         [0, 4, 1, 2], 
         [2, 0, 7, 8], 
         [6, 8, 0, 9], 
         [1, 0, 2, 0]
      ]
      >>> result = Matrices().det(matrix)
      >>> print(result)
      -508.000024
      """
      if not self.issquare(matrix):
         raise SquareMatrixError("Inconsistent square matrix defination")
      
      cmat = self.copy(matrix, digits)
      # Calculate the determinant of 1x1 matrix.
      if self.shape(cmat) == (1, 1):
         return cmat[0][0]
      # Calculate the determinant of 2x2 matrix.
      if self.shape(cmat) == (2, 2):
         return cmat[0][0] * cmat[1][1] - cmat[0][1] * cmat[1][0]
      
      k, switching, nonzero = 0, 1, -1
      # Calculate the determinant of 3x3 or more matrix.
      while (True):
         for i in range(1 + k, len(cmat)):
            # Create the new submatrices for some opertions.
            mat1 = self.zeros(shape=(1, len(cmat[0])))
            mat2 = self.zeros(shape=(1, len(cmat[0])))
            # If any element in main diagonal of `matrix` is zero, and then
            # replace the rows and save the number of switching.
            if cmat[k][k] == 0.0:
               # Find the nonzero element in the diagonal.
               for j in range(0, len(cmat[0])):
                  if not cmat[j][k] == 0.0:
                     nonzero = j
               # If all elements of an column are zeros, then return 0.
               if nonzero == -1:
                  return 0
               # Switch the row.
               mat3 = self.zeros(shape=(1, len(cmat[0])))
               for j in range(0, len(cmat[0])):
                  mat3[0][j] = cmat[k][j]
                  cmat[k][j] = cmat[nonzero][j]
                  cmat[nonzero][j] = mat3[0][j]
               switching *= -1
            # Find the coefficient value of `matrix`.
            coef = -1 * cmat[i][k] / cmat[k][k]
            # Fill the submatrices in appropriate way.
            for j in range(len(cmat[0])):
               mat1[0][j], mat2[0][j] = cmat[k][j], cmat[i][j]
            # Create the matrix using submatrices.
            res = self.add(mat2, self.scaler_mul(mat1, coef, digits), digits)
            for j in range(0, len(cmat[0])):
               cmat[i][j] = res[0][j]
         # Count up the control index.
         k += 1
         # Break up the loop.
         if k == len(cmat):
            break
            
      determinant = 1.0
      # Calculate the determinant using main diagonal of 'res' matrix.
      for i in range(0, len(cmat)):
         determinant *= cmat[i][i]

      return round(determinant * switching, digits)

   def minors(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Extract the minors map of `matrix`. For example: 
      
      >>> matrix = [
         [0, 4, 1], 
         [2, 0, 7], 
         [6, 8, 0]
      ]
      >>> result = Matrices().minors(matrix)
      >>> print(result)
      [[-56.0, -42.0, 16.0], [-8.0, -6.0, -24.0], [28.0, -2.0, -8.0]]
      """
      if not self.issquare(matrix):
         raise SquareMatrixError("Inconsistent square matrix defination")
      if self.shape(matrix) == (1, 1):
         raise MinorsMapError("Couldn't not extracted minors map")
      
      submatrices = list()
      # Extract the submatrices from `matrix`.
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            cmat = self.copy(matrix, digits)
            del cmat[i]
            tcmat = self.transpose(cmat)
            del tcmat[j]
            submatrices.append(self.transpose(tcmat))
      row, minors_map = list(), list()
      # Calculate the determinant  each submatrix.
      for submatrix in submatrices:
         row.append(self.det(submatrix, digits))
         if len(row) == len(matrix[0]):
            minors_map.append(row)
            row = list()

      return minors_map
   
   def cofactors(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Extract the cofactors map of `matrix`. For example: 
      
      >>> matrix = [
         [0, 4, 1], 
         [2, 0, 7], 
         [6, 8, 0]
      ]
      >>> result = Matrices().minors(matrix)
      >>> print(result)
      [[-56.0, 42.0, 16.0], [8.0, -6.0, 24.0], [28.0, 2.0, -8.0]]
      """
      if not self.issquare(matrix):
         raise SquareMatrixError("Inconsistent square matrix defination")
      if self.shape(matrix) == (1, 1):
         raise CofactorsMapError("Couldn't not extracted cofactors map")
      
      # Previously, extract the minors map and then derivate it.
      cofactors_map = self.minors(matrix, digits)
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            if (i + j) % 2 == 1 and cofactors_map[i][j] != 0:
               cofactors_map[i][j] = -1 * cofactors_map[i][j]

      return cofactors_map

   def isinvertible(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` is invertible, otherwise return False. """
      return True if self.det(matrix) != 0.0 else False

   def adjoint(self, matrix: list[list], digits: int = 6) -> list[list]: 
      """ Extract the adjoint of `matrix`. For example:
      
      >>> matrix = [
         [0, 4, 1], 
         [2, 0, 7], 
         [6, 8, 0]
      ]
      >>> result = Matrices().adjoint(matrix)
      >>> print(result)
      [[-56.0, 8.0, 28.0], [42.0, -6.0, 2.0], [16.0, 24.0, -8.0]]
      """
      return self.transpose(self.cofactors(matrix, digits), digits) 

   def inverse(self, matrix: list[list], digits: int = 6) -> list[list]: 
      """ Calculate the inverse of `matrix`. For example: 
      
      >>> matrix = [
         [-1, 2, 3], 
         [-4, 6, 8], 
         [7, -8, 9]
      ]
      >>> result = Matrices().inverse(matrix, 3)
      >>> print(result)
      [[3.278, -1.167, -0.056], [2.556,3 -0.833, -0.111], [-0.278, 0.167, 0.056]]
      """
      if not self.isinvertible(matrix):
         raise InvertibleMatrixError("Invertible matrix entrance")
      
      return self.scaler_div(self.adjoint(matrix, digits), 
                             self.det(matrix, digits), digits)
 
   def solve(self, matrix: list[list], digits: int = 6) -> list[list]:
      """ Solve the linear equation systems. `matrix` must be in augmented 
      form. For example: 
      
      >>> matrix = [
         [1, -2, 3, 9], 
         [-1, 3, 0, -4], 
         [2, -5, 5, 17]
      ]
      >>> result = Matrices().solve(matrix)
      >>> print(result)
      [[1.0], [-1.0], [2.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      if not len(matrix[0]) - len(matrix) == 1:
         raise DimensionError("Dimension dismatch found")
      
      # Split the 'matrix' into two submatrices named 'main', 'target'.
      main = self.zeros(shape=(len(matrix), len(matrix)))
      target = self.zeros(shape=(len(matrix), 1))
      # Fill the submatrices in using 'matrix'.
      for i in range(len(matrix)):
         for j in range(len(matrix)):
            main[i][j] = round(float(matrix[i][j]), digits)
      for i in range(len(matrix)):
         target[i][0] = round(float(matrix[i][len(matrix)]), digits)

      return self.cross_mul(self.inverse(main, digits), target, digits)
