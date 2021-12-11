# -*- coding: utf-8 -*-

#
# © 2021 David Strip - david@stripfamily.net
#




class UnitizeException(Exception):
  pass

class FileException(UnitizeException):
  pass

class TupleLengthError(UnitizeException):
  pass
