"""AbstractDecorator provides an abstract baseclass for decorators. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Self


class _MetaDecorator(type):
  """This metaclass allows the decorator class to define a __call__ on
  itself. To do this, the decorator class must implement a method called
  '__class_call__'. If not, the normal __call__ is used."""

  def __call__(cls, *args, **kwargs) -> Any:
    """Invokes __class_call__ on decorator class, if it implements it."""
    callMeMaybe = getattr(cls, '__class_call__')
    if callable(callMeMaybe):
      try:
        if hasattr(callMeMaybe, '__self__'):
          return callMeMaybe(*args, **kwargs)
        else:
          return callMeMaybe(cls, *args, **kwargs)
      except NotImplementedError:
        return type.__call__(cls, *args, **kwargs)


class AbstractDecorator(metaclass=_MetaDecorator):
  """AbstractDecorator provides an abstract baseclass for decorators. """

  @classmethod
  def __class_call__(cls, *args, **kwargs) -> Any:
    """Subclasses may reimplement this method to define what happens
    when the class is called directly on an object to be decorated. This
    is optional. The method on the abstract class will raise
    NotImplemented to indicate to the metaclass that the fallback should
    be used. """
    raise NotImplementedError

  def __init__(self, *args, **kwargs) -> None:
    self.__inner_object__ = None
    self.__inner_self__ = None
    self.__inner_callable__ = None

  def _setInnerObject(self, innerObject: Any) -> None:
    if self.__inner_object__ is not None:
      raise AttributeError
    if callable(innerObject):
      if hasattr(innerObject, '__self__'):
        self.__inner_self__ = getattr(innerObject, '__self__')
    self.__inner_object__ = innerObject
    if isinstance(innerObject, type) or callable(innerObject):
      self.__inner_callable__ = True
    else:
      self.__inner_callable__ = False

  def __call__(self, *args, **kwargs) -> Self:
    """Updates the inner object or calls inner object"""
    if args:
      try:
        self._setInnerObject(args[0])
      except AttributeError:
        return self._callInnerObject(*args, **kwargs)
    return self._callInnerObject(**kwargs)

  def _callInnerObject(self, *args, **kwargs) -> Any:
    """Calls the inner object"""
    if self.__inner_object__ is None:
      raise RuntimeError
    if not self.__inner_callable__:
      raise TypeError
    if self.__inner_self__ is None:
      return self.__inner_object__(*args, **kwargs)
    return self.__inner_object__(self.__inner_self__, *args, **kwargs)
