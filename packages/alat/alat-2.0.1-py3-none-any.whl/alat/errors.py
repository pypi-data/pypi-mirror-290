# Errors for ALAT (Advanced Linear Algebra Toolkit)

class MatrixError(Exception):
   """ Raise matrix error. """
   pass

class SquareMatrixError(Exception):
   """ Raise square matrix error. """
   pass

class DimensionError(Exception):
   """ Raise dimension error. """
   pass

class MinorsMapError(Exception):
   """ Raise minors map error. """
   pass

class CofactorsMapError(Exception):
   """ Raise cofactors map error. """
   pass

class InvertibleMatrixError(Exception):
   """ Raise invertible matrix error. """
   pass

class VectorError(Exception):
   """ Raise vector error. """
   pass

class ZeroLenghtVector(Exception):
   """ Raise zero lenght vector error. """
   pass

class ZeroVectorError(Exception):
   """ Raise zeros vector error. """
   pass

class ComplexError(Exception):
   """ Raise complex number error. """
   pass

class InconsistentCharacterError(Exception):
   """ Raise inconsistent character error. """
   pass
