# Crypts class for ALAT (Advanced Linear Algebra Toolkit)

from .errors import (SquareMatrixError, InconsistentCharacterError, 
                    InvertibleMatrixError)
from .matrices import Matrices

__all__ = ["Crypts"]

CHARACTERS = {
   "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, 

   "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "I": 18, 
   "J": 19, "K": 20, "L": 21, "M": 22, "N": 23, "O": 24, "P": 25, "Q": 26, "R": 27, 
   "S": 28, "T": 29, "U": 30, "V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35, "a": 36, 
   "b": 37, "c": 38, "d": 39, "e": 40, "f": 41, "g": 42, "h": 43, "i": 44, "j": 45, 
   "k": 46, "l": 47, "m": 48, "n": 49, "o": 50, "p": 51, "q": 52, "r": 53, "s": 54, 
   "t": 55, "u": 56, "v": 57, "w": 58, "x": 59, "y": 60, "z": 61, 

   "é": 62, "!": 63, "'": 64, "^": 65, "+": 66, "%": 67, "&": 68, "/": 69, "(": 70, 
   ")": 71, "=": 72, "?": 73, "_": 74, ";": 75, ":": 76, "\"": 77, ">": 78, "<": 79, 
   "|": 80, "#": 81, "$": 82, "{": 83, "[": 84, "]": 85, "}": 86, "*": 87, "\\": 88, 
   "-": 89, "@": 90, "€": 91, "~": 92, ",": 93, "`": 94, ".": 95, " ": 96,
}

class Crypts:
   """ Cryptography methods for ALAT (Advanced Linear Algebra Toolkit) """

   def to_matrix(self, message: str, shape: tuple) -> list[list]:
      """ Convert the `message` into square matrix which has `shape`. Lenght 
      of `message` must be bigger than matrix total elements. If there will 
      be missing element/s, in this case fill the blank element in with -1. 
      For example: 

      >>> message = "Everyting has beauty, but not everyone sees it."
      >>> result = Crypts().to_matrix(message, (7, 7))
      >>> for row in result:
      ...   print(row)
      [14.0, 57.0, 40.0, 53.0, 60.0, 55.0, 44.0]
      [49.0, 42.0, 96.0, 43.0, 36.0, 54.0, 96.0]
      [37.0, 40.0, 36.0, 56.0, 55.0, 60.0, 93.0]
      [96.0, 37.0, 56.0, 55.0, 96.0, 49.0, 50.0]
      [55.0, 96.0, 40.0, 57.0, 40.0, 53.0, 60.0]
      [50.0, 49.0, 40.0, 96.0, 54.0, 40.0, 40.0]
      [54.0, 96.0, 44.0, 55.0, 95.0, -1.0, -1.0]
      """
      if not isinstance(shape, tuple):
         raise TypeError("'shape' must be tuple")
      if not len(shape) == 2:
         raise ValueError("'shape' must include just row and column values")
      if not shape[0] == shape[1]:
         raise SquareMatrixError("Inconsistent square matrix shape")
      
      index, characters, matrix = 0, list(), Matrices().arbitrary(-1.0, shape)
      # Indicate the corresponding numbers from 'message' characters.
      for char in message:
         if char in CHARACTERS.keys():
            characters.append(CHARACTERS[char])
         else:
            error_message = "Inconsistent character found: '%s'" % char
            raise InconsistentCharacterError(error_message)
      # Create a arbitrary matrix and then replace its elements with message.
      for i in range(shape[0]):
         for j in range(shape[1]):
            matrix[i][j] = float(characters[index])
            index += 1
            if index == len(characters):
               break

      return matrix

   def encode(self, message: str, encoding: list[list], digits: int = 6) -> list[list]:
      """ Encode the `message` using invertible `encoding` matrix. For example:
      
      >>> message = "Everyting has beauty, but not everyone sees it."
      >>> encoding = [
         [2.0, 0.0, -1.0, 1.0, 5.0, -4.0, -4.0], 
         [1.0, 4.0, -2.0, 4.0, -3.0, 3.0, -3.0], 
         [-2.0, -2.0, -4.0, -4.0, 0.0, 2.0, -5.0], 
         [-2.0, -1.0, 1.0, -3.0, 2.0, 3.0, -2.0], 
         [1.0, 5.0, 2.0, 4.0, 5.0, 3.0, -5.0], 
         [-2.0, -1.0, 4.0, -5.0, 0.0, 5.0, 2.0], 
         [2.0, -3.0, -1.0, 4.0, 4.0, 0.0, -3.0]
      ]
      >>> result = Crypts().encode(message, encoding)
      >>> for row in result:
      ...   print(row)
      [-63.0, 208.0, 61.0, 64.0, 481.0, 809.0, -855.0]
      [-18.0, -229.0, -282.0, -38.0, 769.0, 629.0, -1248.0]
      [51.0, -32.0, 52.0, 177.0, 824.0, 677.0, -994.0]
      [105.0, 262.0, -1.0, 194.0, 1159.0, 537.0, -1417.0]
      [66.0, 214.0, -118.0, 243.0, 541.0, 704.0, -1096.0]
      [-69.0, 130.0, 16.0, -26.0, 725.0, 677.0, -1049.0]
      [101.0, 720.0, -180.0, 478.0, 563.0, 605.0, -1308.0]
      """
      if not Matrices().isinvertible(encoding):
         raise InvertibleMatrixError("Invertible matrix entrance")
      
      return Matrices().cross_mul(self.to_matrix(message, Matrices().shape(encoding)), 
                                  encoding, digits)

   def decode(self, encoded: list[list], encoding: list[list], digits: int = 6) -> list[list]:
      """ Decode the `encoded` message using `encoding` matrix. For example: 
      
      >>> encoded = [
         [-63.0, 208.0, 61.0, 64.0, 481.0, 809.0, -855.0], 
         [-18.0, -229.0, -282.0, -38.0, 769.0, 629.0, -1248.0], 
         [51.0, -32.0, 52.0, 177.0, 824.0, 677.0, -994.0], 
         [105.0, 262.0, -1.0, 194.0, 1159.0, 537.0, -1417.0], 
         [66.0, 214.0, -118.0, 243.0, 541.0, 704.0, -1096.0], 
         [-69.0, 130.0, 16.0, -26.0, 725.0, 677.0, -1049.0], 
         [101.0, 720.0, -180.0, 478.0, 563.0, 605.0, -1308.0]
      ]
      >>> encoding = [
         [2.0, 0.0, -1.0, 1.0, 5.0, -4.0, -4.0], 
         [1.0, 4.0, -2.0, 4.0, -3.0, 3.0, -3.0], 
         [-2.0, -2.0, -4.0, -4.0, 0.0, 2.0, -5.0], 
         [-2.0, -1.0, 1.0, -3.0, 2.0, 3.0, -2.0], 
         [1.0, 5.0, 2.0, 4.0, 5.0, 3.0, -5.0], 
         [-2.0, -1.0, 4.0, -5.0, 0.0, 5.0, 2.0], 
         [2.0, -3.0, -1.0, 4.0, 4.0, 0.0, -3.0]
      ]
      >>> result = Crypts().decode(encoded, encoding)
      >>> for row in result:
      ...   print(row)
      [14.0, 57.0, 40.0, 53.0, 60.0, 55.0, 44.0]
      [49.0, 42.0, 96.0, 43.0, 36.0, 54.0, 96.0]
      [37.0, 40.0, 36.0, 56.0, 55.0, 60.0, 93.0]
      [96.0, 37.0, 56.0, 55.0, 96.0, 49.0, 50.0]
      [55.0, 96.0, 40.0, 57.0, 40.0, 53.0, 60.0]
      [50.0, 49.0, 40.0, 96.0, 54.0, 40.0, 40.0]
      [54.0, 96.0, 44.0, 55.0, 95.0, -1.0, -1.0]
      """
      # Decode the 'encoded' message using 'encoding' matrix.
      res = Matrices().cross_mul(encoded, Matrices().inverse(encoding, digits), digits)
      # Round the elements of decoded matrix.
      for i in range(len(res)):
         for j in range(len(res[0])):
            res[i][j] = float(round(res[i][j]))

      return res

   def to_message(self, encoded: list[list], encoding: list[list], digits: int = 6) -> str:
      """ Convert the `encoded` message to string message using `encoding` matrix.
      For example:  
      
      >>> encoded = [
         [-63.0, 208.0, 61.0, 64.0, 481.0, 809.0, -855.0], 
         [-18.0, -229.0, -282.0, -38.0, 769.0, 629.0, -1248.0], 
         [51.0, -32.0, 52.0, 177.0, 824.0, 677.0, -994.0], 
         [105.0, 262.0, -1.0, 194.0, 1159.0, 537.0, -1417.0], 
         [66.0, 214.0, -118.0, 243.0, 541.0, 704.0, -1096.0], 
         [-69.0, 130.0, 16.0, -26.0, 725.0, 677.0, -1049.0], 
         [101.0, 720.0, -180.0, 478.0, 563.0, 605.0, -1308.0]
      ]
      >>> encoding = [
         [2.0, 0.0, -1.0, 1.0, 5.0, -4.0, -4.0], 
         [1.0, 4.0, -2.0, 4.0, -3.0, 3.0, -3.0], 
         [-2.0, -2.0, -4.0, -4.0, 0.0, 2.0, -5.0], 
         [-2.0, -1.0, 1.0, -3.0, 2.0, 3.0, -2.0], 
         [1.0, 5.0, 2.0, 4.0, 5.0, 3.0, -5.0], 
         [-2.0, -1.0, 4.0, -5.0, 0.0, 5.0, 2.0], 
         [2.0, -3.0, -1.0, 4.0, 4.0, 0.0, -3.0]
      ]
      >>> result = Crypts().to_message(encoded, encoding)
      >>> print(result)
      "Everyting has beauty, but not everyone sees it."
      """
      # Reverse the keys and values with each other.
      characters = dict()
      for key, value in CHARACTERS.items():
         characters[value] = key
      # Convert the numeric elements to charcters.
      result = ""
      for row in self.decode(encoded, encoding, digits):
         for el in row:
            if el != -1.0:
               result += characters[el]

      return result
