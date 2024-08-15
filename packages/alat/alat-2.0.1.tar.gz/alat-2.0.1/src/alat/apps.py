# Apps class for ALAT (Advanced Linear Algebra Toolkit)

from .errors import VectorError, DimensionError
from .matrices import Matrices
from .vectors import Vectors

__all__ = ["Apps"]

class Apps:
   """ Some application methods for ALAT (Advanced Linear Algebra Toolkit) """

   def poly_curve_fitting(self, xvector: tuple, yvector: tuple, digits: int = 6) -> tuple:
      """ Apply polynomial curve fitting to both `xvector` and `yvector`. For example: 
      
      >>> xvector = (1, 2, 3) # x axis points
      >>> yvector = (4, 0, 12) # y axis points
      >>> res = Apps().poly_curve_fitting(xvector, yvector)
      >>> print(res)
      (24.0, -28.0, 8.0)   # f(x) = 24.0 - 28.0x + 8.0x ** 2
      """
      if not Vectors().isvector(xvector) or not Vectors().isvector(yvector):
         raise VectorError("Inconsistent vector defination")
      if not Vectors().dim(xvector) == Vectors().dim(yvector):
         raise DimensionError("Dimension dismatch found")
      
      main = Matrices().zeros(shape=(Vectors().dim(xvector), Vectors().dim(yvector)))
      target = Matrices().transpose([list(yvector)], digits)
      # Create the main matrix and then fill its elements with new values.
      for i in range(Vectors().dim(xvector)):
         index = 0
         while True:
            main[i][index] = pow(xvector[i], index)
            index += 1
            # Break up the loop.
            if (index == Vectors().dim(xvector)):
               break
      # Get the inverse of 'main' matrix and then multiply it with 'target' matrix.
      res = Matrices().cross_mul(Matrices().inverse(main, digits), target, digits)

      return tuple(res[i][0] for i in range(Vectors().dim(xvector)))

   def least_squares_reg(self, xvector: tuple, yvector: tuple, digits: int = 6)-> tuple:
      """ Apply least squares regression to both `xvector` and `yvector`. For example: 
      
      >>> xvector = (1, 2, 3, 4, 5) # x axis points
      >>> yvector = (1, 2, 4, 4, 6) # y axis points
      >>> res = Apps().least_squares_reg(xvector, yvector)
      >>> print(res)
      (-0.2, 1.2)    # f(x) = -0.2 + 1.2x 
      """
      if not Vectors().isvector(xvector) or not Vectors().isvector(yvector):
         raise VectorError("Inconsistent vector defination")
      if not Vectors().dim(xvector) == Vectors().dim(yvector):
         raise DimensionError("Dimension dismatch found")
      
      # Make a lots of matrix operations and find the result.
      main = Matrices().ones(shape=(2, Vectors().dim(xvector)))
      for i in range(Vectors().dim(xvector)):
         main[1][i] = xvector[i]
      target = Matrices().transpose([list(yvector)], digits)
      tmain = Matrices().transpose(main, digits)
      cmul1 = Matrices().cross_mul(main, tmain, digits)
      cmul2 = Matrices().cross_mul(main, target, digits)
      cofact = Matrices().cofactors(cmul1, digits)
      cmul3 = Matrices().cross_mul(cofact, cmul2, digits)
      smul = Matrices().scaler_mul(cmul3, 1 / 50, digits)

      return tuple(smul[i][0] for i in range(2))
      
   def area(self, xvector: tuple, yvector: tuple, digits: int = 6) -> float:
      """ Calculate the area of triangular using determinant. `xvector` and 
      `yvector` indicates in order x and y axis points. For example: 
      
      >>> xvector = (1, 2, 4) # x axis points
      >>> yvector = (0, 2, 3) # y axis points
      >>> res = Apps().area(xvector, yvector)
      >>> print(res)
      1.5
      """
      if not Vectors().isvector(xvector) or not Vectors().isvector(yvector):
         raise VectorError("Inconsistent vector defination")
      if not Vectors().dim(xvector) == Vectors().dim(yvector) == 3:
         raise DimensionError("Dimension dismatch found")
      
      main = Matrices().ones(shape=(3, 3))
      # Create new ones matrix and then fill its elements with axis points.
      for i in range(3):
         main[0][i], main[1][i] = xvector[i], yvector[i]
      # Calculate the area.
      res = Matrices().det(Matrices().transpose(main, digits), digits) / 2
   
      return -1.0 * res if res < 0 else res

   def volume(self, xvector: tuple, yvector: tuple, zvector: tuple, 
              digits: int = 6) -> float:
      """ Calculate the volume of tetrahedron using determinant. `xvector`, `yvector`, 
      and `zvector` indicates in order x, y and z axis points. For example: 
      
      >>> xvector = (0, 4, 3, 2) # x axis points
      >>> yvector = (4, 0, 5, 2) # y axis points
      >>> zvector = (1, 0, 2, 5) # z axis points
      >>> res = Apps().volume(xvector, yvector, zvector)
      >>> print(res)
      12.0
      """
      if not Vectors().isvector(xvector) or not Vectors().isvector(yvector) or \
         not Vectors().isvector(zvector):
         raise VectorError("Inconsistent vector defination")
      if not Vectors().dim(xvector) == Vectors().dim(yvector) == Vectors().dim(zvector) == 4:
         raise DimensionError("Dimension dismatch found")
      
      main = Matrices().ones(shape=(4, 4))
      # Create new ones matrix and then fill its elements with axis points.
      for i in range(4):
         main[0][i], main[1][i], main[2][i] = xvector[i], yvector[i], zvector[i]
      # Calculate the volume.
      res = Matrices().det(Matrices().transpose(main, digits), digits) / 6
   
      return -1.0 * res if res < 0 else res
