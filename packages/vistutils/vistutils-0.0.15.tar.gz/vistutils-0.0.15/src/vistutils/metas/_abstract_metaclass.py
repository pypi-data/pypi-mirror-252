"""AbstractMetaclass provides an abstract metaclass. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.metas import Bases, Namespace, BaseNamespace


class MetaMetaClass(type):
  """This class is the only way to change the __str__ in the metaclass."""

  def __str__(cls) -> str:
    if cls is MetaMetaClass:
      return MetaMetaClass.__qualname__
    return cls.__qualname__


class AbstractMetaclass(MetaMetaClass, metaclass=MetaMetaClass):
  """AbstractMetaclass provides an abstract metaclass. """

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    """This method creates the namespace object for the class. """
    namespace = BaseNamespace(name, bases, **kwargs)
    namespace.setMetaclass(mcls)
    return namespace

  def __new__(mcls,
              name: str,
              bases: Bases,
              namespace: Namespace,
              **kwargs) -> type:
    """Remember not to decorate the __new__ method as a class method.
    Doing so results in undefined behaviour. """
    return type.__new__(mcls, name, bases, namespace, **kwargs)

  def __init__(cls, *args, **kwargs) -> None:
    """This is the final method called before the class is passed to
    decorators. """
    type.__init__(cls, *args, **kwargs)

  def __call__(cls, *args, **kwargs) -> Any:
    """This method defines what happens when calling the class itself. By
    default, this invokes the __new__ defined on the class to create the
    new instance. Then the __init__ method on the class is called on the
    new instance. Finally, the new instance is returned. This mirrors the
    default behaviour of instance creation."""
    if not hasattr(cls, '__new__'):
      return type.__call__(cls, *args, **kwargs)
    __new__ = getattr(cls, '__new__')
    __init__ = getattr(cls, '__init__', None)
    self = __new__(cls)
    if callable(__init__):
      if hasattr(__init__, '__self__'):
        __init__(*args, **kwargs)
      else:
        __init__(self, *args, **kwargs)
      return self
    else:
      object.__init__(self)
      return self
