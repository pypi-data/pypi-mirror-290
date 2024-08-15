# Complexes class for ALAT (Advanced Linear Algebra Toolkit)

import math

from .errors import ComplexError

__all__ = ["Complexes"]

class Complexes:
   """ Complex number methods for ALAT (Advanced Linear Algebra Toolkit) """

   def iscomplex(self, complex: dict) -> bool:
      """ Return True, if `complex` is in right form, otherwise, return False. """
      if not isinstance(complex, dict):
         return False
      # complex contains just 're', 'im', and 'form' parts.
      if not len(complex.keys()) == 3:
         return False
      for key in complex.keys():
         if key not in ("x",   # real for 'cartesian' or modules for 'polar'
                        "y",   # imaginary for 'cartesian' or argument for 'polar'
                        "form" # cartesian for 'cartesian' and polar for 'polar'
                        ):
            return False
      if not isinstance(complex["x"], (int ,float)) or \
         not isinstance(complex["y"], (int, float)):
         return False
      # For this class, there are two types of representation for complex
      # number: 'cartesian' and 'polar'.
      if not complex["form"] == "cartesian" and not complex["form"] == "polar":
         return False

      return True

   def round(self, complex: dict, digits: int = 6) -> dict:
      """ Round the `complex` number according to `digits`. """
      if not self.iscomplex(complex):
         raise ComplexError("Inconsistent complex number defination")
      
      return {"x": round(float(complex["x"]), digits), 
              "y": round(float(complex["y"]), digits),
              "form": complex["form"]}

   def deg(self, rad: float, digits: int = 6) -> float:
      """ Convert the `rad` raidans to degrees. """
      return round(rad * 180.0 / math.pi, digits)

   def rad(self, deg: float, digits: int = 6) -> float: 
      """ Convert the 'deg' degrees to radians. """
      return round(deg * math.pi / 180.0, digits)

   def transform(self, complex: dict, new_form: str, digits: int = 6) -> dict:
      """ Transform the `complex` in a particular form to `new_form`. `new_form` 
      must be `cartesian` or `polar`. Note that argument of polar form will be
      in forms of degrees. For example: 
      
      >>> c = {"x": 3, "y": 4, "form": "cartesian"} # real, imaginary, form
      >>> print(Complexes().transform(c, "polar"))
      {'x': 5.0, 'y': 233.130102, 'form': 'polar'} # modules, argument, form
      """
      if not self.iscomplex(complex):
         raise ComplexError("Inconsistent complex number defination")
      if not new_form == "cartesian" and not new_form == "polar":
         raise ValueError("Complex number form must be 'cartesian' or 'polar'")
      
      res = dict()
      # Transform the complex in to another form.
      if complex["form"] == "cartesian":
         if new_form == "cartesian":
            res["x"], res["y"] = complex["x"], complex["y"]
            res["form"] = complex["form"]
         else:
            res["x"] = math.sqrt(pow(complex["x"], 2) + pow(complex["y"], 2))
            res["y"] = self.deg(math.atan(complex["y"] / complex["x"])) + 180.0
            res["form"] = "polar"
      else:
         if new_form == "cartesian":
            res["x"] = complex["x"] * math.cos(self.rad(complex["y"]))
            res["y"] = complex["x"] * math.sin(self.rad(complex["y"]))
            res["form"] = "cartesian"
         else:
            res["x"], res["y"] = complex["x"], complex["y"]
            res["form"] = complex["form"]

      return self.round(res, digits)

   def isequal(self, fcomplex: dict, scomplex: dict) -> bool:
      """ Return True, if `fcomplex` and `scomplex` are equal, otherwise return False. """
      if self.iscomplex(fcomplex) and self.iscomplex(scomplex):
         if fcomplex["x"] == scomplex["x"] and fcomplex["y"] == scomplex["y"] \
               and fcomplex["form"] == scomplex["form"]:
            return True
         
      return False
  
   def iscartesian(self, complex: dict) -> bool:
      """ Return True, if `complex` is in cartesian form, otherwise return False. """
      return True if self.iscomplex(complex) and complex["form"] == "cartesian" else False

   def ispolar(self, complex: dict) -> bool:
      """ Return True, if `complex` is in polar form, otherwise return False. """
      return True if self.iscomplex(complex) and complex["form"] == "polar" else False

   def iszero(self, complex: dict) -> bool:
      """ Return True, if `complex` is zero, otherwise return False. """
      return True if self.iscomplex(complex) and complex["x"] == 0.0 and \
             complex["y"] == 0.0 else False
   
   def istriangle(self, fcomplex: dict, scomplex: dict) -> bool:
      """ Return True, if there is Triangle inequality, otherwise return False. """
      fcomplex, scomplex = self.transform(fcomplex, "polar"), self.transform(scomplex, "polar")
      return True if self.iscomplex(fcomplex) and self.iscomplex(scomplex) and \
             fcomplex["y"] + scomplex["y"] >= self.add(fcomplex, scomplex)["y"] else False

   def zero(self, output_form: str):
      """ Create a new zero complex number that has `output_form` form. `output_form`
      must be 'cartesian' and 'polar'. """
      if not output_form == "cartesian" and not output_form == "polar":
         raise ValueError("Complex number form must be 'cartesian' or 'polar'")

      return {"x": 0.0, "y": 0.0, "form": output_form}
   
   def real(self, complex: dict, digits: int = 6) -> float: 
      """ Return the real part of `complex`. If form of `complex` is polar, then 
      convert it to cartesian. For example: 
      
      >>> c = {"x":28.7, "y":150, "form":"polar"} # modules, argument, form
      >>> print(Complexes().real(c))
      -24.854929
      """
      if not self.iscomplex(complex):
         raise ComplexError("Inconsistent complex number defination")
      
      if complex["form"] == "cartesian":
         return round(float(complex["x"]), digits)
      else:
         return round(self.transform(complex, "cartesian")["x"], digits)

   def imaginary(self, complex: dict, digits: int = 6) -> float: 
      """ Return the imaginary part of `complex`. If form of `complex` is polar, 
      then convert it to cartesian. For example: 
      
      >>> c = {"x":28.7, "y":150, "form":"polar"} # modules, argument, form
      >>> print(Complexes().imaginary(c))
      14.35
      """
      if not self.iscomplex(complex):
         raise ComplexError("Inconsistent complex number defination")
      
      if complex["form"] == "cartesian":
         return round(float(complex["y"]), digits)
      else:
         return round(self.transform(complex, "cartesian")["y"], digits)

   def modules(self, complex: dict, digits: int = 6) -> float:
      """ Return the modules part of `complex`. If form of `complex` is
      cartesian, then convert it to polar. For example:
      
      >>> c = {"x":7.4, "y":-4, "form":"cartesian"} # real, imaginary, form
      >>> print(Complexes().modules(c))
      8.411896 
      """
      if not self.iscomplex(complex):
         raise ComplexError("Inconsistent complex number defination")
      
      if complex["form"] == "polar":
         return round(float(complex["x"]), digits)
      else:
         return round(self.transform(complex, "polar")["x"], digits)

   def argument(self, complex: dict, digits: int = 6) -> float:
      """ Return the argument part of `complex`. If form of `complex` is 
      cartesian, then convert it to polar. For example:
      
      >>> c = {"x":7.4, "y":-4, "form":"cartesian"} # real, imaginary, form
      >>> print(Complexes().argument(c))
      151.606981  # (degrees)
      """
      if not self.iscomplex(complex):
         raise ComplexError("Inconsistent complex number defination")
      
      if complex["form"] == "polar":
         return round(float(complex["y"]), digits)
      else:
         return round(self.transform(complex, "polar")["y"], digits)

   def add(self, fcomplex: dict, scomplex: dict, output_form: str = "cartesian", 
           digits: int = 6) -> dict:
      """ Add up the `fcomplex` and `scomplex` with each other. The result complex 
      number will be in `output_form` ("cartesian" or "polar") form. For exampe: 
      
      >>> c1 = {"x": 7.4, "y": -4, "form": "cartesian"} # real, imaginary, form
      >>> c2 = {"x": 28.7, "y": 150, "form": "polar"} # modules, argument, form
      >>> print(Complexes().add(c1, c2, "polar"))
      {'x': 20.292783, 'y': 149.333936, 'form': 'polar'}
      """
      if not self.iscomplex(fcomplex) or not self.iscomplex(scomplex):
         raise ComplexError("Inconsistent complex number defination") 
       
      res = self.zero("cartesian")
      # Convert the complex numbers to cartesian forms.
      fcomplex = self.transform(fcomplex, "cartesian", digits)
      scomplex = self.transform(scomplex, "cartesian", digits)

      res["x"] = fcomplex["x"] + scomplex["x"]
      res["y"] = fcomplex["y"] + scomplex["y"]

      return self.round(res, digits) if output_form == "cartesian" else \
             self.round(self.transform(res, "polar", digits), digits)

   def subtract(self, fcomplex: dict, scomplex: dict, output_form: str = "cartesian",  
                digits: int = 6) -> dict:
      """ Subtract the `scomplex` from `fcomplex` with each other. The result complex 
      number will be in `output_form` ("cartesian" or "polar") form. For exampe: 
      
      >>> c1 = {"x": 7.4, "y": -4, "form": "cartesian"} # real, imaginary, form
      >>> c2 = {"x": 28.7, "y": 150, "form": "polar"} # modules, argument, form
      >>> print(Complexes().subtract(c1, c2, "cartesian"))
      {'x': 32.254929, 'y': -18.35, 'form': 'cartesian'}
      """
      if not self.iscomplex(fcomplex) or not self.iscomplex(scomplex):
         raise ComplexError("Inconsistent complex number defination") 
      
      res = self.zero("cartesian")
      # Convert the complex numbers to cartesian forms.
      fcomplex = self.transform(fcomplex, "cartesian", digits)
      scomplex = self.transform(scomplex, "cartesian", digits)

      res["x"] = fcomplex["x"] - scomplex["x"]
      res["y"] = fcomplex["y"] - scomplex["y"]

      return self.round(res, digits) if output_form == "cartesian" else \
             self.round(self.transform(res, "polar", digits), digits)

   def multiply(self, fcomplex: dict, scomplex: dict, output_form: str = "cartesian",
                digits: int = 6) -> dict:
      """ Multiply the `fcomplex` and `scomplex` with each other. The result complex 
      number will be in `output_form` ('cartesian' or 'polar') form. For example: 
      
      >>> c1 = {"x": 7.4, "y": -4, "form": "cartesian"} # real, imaginary, form
      >>> c2 = {"x": 28.7, "y": 150, "form": "polar"} # modules, argument, form
      >>> print(Complexes().multiply(c1, c2, "polar"))
      {'x': 241.421415, 'y': 301.606981, 'form': 'polar'}
      """
      if not self.iscomplex(fcomplex) or not self.iscomplex(scomplex):
         raise ComplexError("Inconsistent complex number defination") 
      
      res = self.zero("polar")
      # Convert the complex numbers to polar forms.
      fcomplex = self.transform(fcomplex, "polar", digits)
      scomplex = self.transform(scomplex, "polar", digits)

      res["x"] = fcomplex["x"] * scomplex["x"]
      res["y"] = fcomplex["y"] + scomplex["y"]

      return self.round(res, digits) if output_form == "polar" else \
             self.round(self.transform(res, "cartesian", digits), digits)

   def divide(self, fcomplex: dict, scomplex: dict, output_form: str = "cartesian",
             digits: int = 6) -> dict: 
      """ Divide the `scomplex` to `fcomplex`. The result complex number will be 
      in `output_form` ("cartesian" or "polar") form. For example: 
      
      >>> c1 = {"x": 7.4, "y": -4, "form": "cartesian"} # real, imaginary, form
      >>> c2 = {"x": 28.7, "y": 150, "form": "polar"} # modules, argument, form
      >>> print(Complexes().divide(c1, c2, "cartesian"))
      {'x': 0.292982, 'y': 0.008219, 'form': 'cartesian'}
      """
      if not self.iscomplex(fcomplex) or not self.iscomplex(scomplex):
         raise ComplexError("Inconsistent complex number defination") 
      
      res = self.zero("polar")
      # Convert the complex numbers to polar forms.
      fcomplex = self.transform(fcomplex, "polar", digits)
      scomplex = self.transform(scomplex, "polar", digits)

      res["x"] = fcomplex["x"] / scomplex["x"]
      res["y"] = fcomplex["y"] - scomplex["y"]

      return self.round(res, digits) if output_form == "polar" else \
             self.round(self.transform(res, "cartesian", digits), digits)

   def power(self, complex: dict, n: float, output_form: str = "cartesian", 
             digits: int = 6) -> dict: 
      """ Get the `n`.th power of `complex` number. The result complex number 
      will be in `output_form` ("cartesian" or "polar") form. For example: 
      
      >>> c = {"x": 7.4, "y": -4, "form": "cartesian"} # real, imaginary, form
      >>> print(Complexes().power(c, 2, "cartesian"))
      {'x': 38.759998, 'y': -59.199995, 'form': 'cartesian'}
      """
      if not self.iscomplex(complex):
         raise ComplexError("Inconsistent complex number defination") 
      
      res = self.zero("polar")
      # Convert the complex number to polar form.
      complex = self.transform(complex, "polar", digits)

      res["x"], res["y"] = pow(complex["x"], n), complex["y"] * n

      return self.round(res, digits) if output_form == "polar" else \
             self.round(self.transform(res, "cartesian", digits), digits)

   def root(self, complex: dict, n: float, output_form: str = "cartesian", 
            digits: int = 6) -> dict:
      """ Get the `n`.th root of `complex` number. The result complex number 
      will be in `output_form` ("cartesian" or "polar") form. For example: 
      
      >>> c = {"x": 7.4, "y": -4, "form": "cartesian"} # real, imaginary, form
      >>> print(Complexes().root(c, 2, "cartesian"))
      {'x': 0.711302, 'y': 2.811751, 'form': 'cartesian'}
      """
      if not self.iscomplex(complex):
         raise ComplexError("Inconsistent complex number defination") 
      
      res = self.zero("polar")
      # Convert the complex number to polar form.
      complex = self.transform(complex, "polar", digits)

      res["x"], res["y"] = pow(complex["x"], (1 / n)), complex["y"] / n

      return self.round(res, digits) if output_form == "polar" else \
             self.round(self.transform(res, "cartesian", digits), digits)

   def conjugate(self, complex: dict, output_form: str = "cartesian", 
                 digits: int = 6) -> dict:
      """ Get the conjugate of `complex`. The result complex number will be in
      `output_form` ("cartesian", "polar"). For example: 
      
      >>> c = {"x": 7.4, "y": -4, "form": "cartesian"} # real, imaginary, form
      >>> print(Complexes().conjugate(c, "cartesian"))
      {'x': 7.4, 'y': 4.0, 'form': 'cartesian'}
      """
      if not self.iscomplex(complex):
         raise ComplexError("Inconsistent complex number defination")
      
      res = self.zero("cartesian")
      # Convert the complex number to cartesian form.
      complex = self.transform(complex, "cartesian", digits)

      res["x"], res["y"] = complex["x"], -1.0 * complex["y"]

      return self.round(res, digits) if output_form == "cartesian" else \
             self.round(self.transform(res, "polar", digits), digits)

   def reciprocal(self, complex: dict, output_form: str = "cartesian", 
                  digits: int = 6) -> dict: 
      """ Get the reciprocal of `complex`. The result complex number will be in
      `output_form` ("cartesian" or "polar"). For example: 
      
      >>> c = {"x": 7.4, "y": -4, "form": "cartesian"} # real, imaginary, form
      >>> print(Complexes().reciprocal(c, "cartesian"))
      {'x': -0.104579, 'y': -0.056529, 'form': 'cartesian'}
      """
      return self.power(complex, -1.0, output_form, digits)
