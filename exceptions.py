# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 16:53:18 2021

@author: David
"""

class UnitizeException(Exception):
  pass

class FileException(UnitizeException):
  pass

class TupleLengthError(UnitizeException):
  pass