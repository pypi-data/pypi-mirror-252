"""The apply decorator permits decoration by setting a particular
attribute. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Callable


def apply(key: str, value: Any) -> Callable:
  """Decorates object by changing given attribute to given value."""

  def func(callMeMaybe: Callable) -> Callable:
    """The apply decorator creates this callable which is then called on
    the decorated object"""
    setattr(callMeMaybe, key, value)
    return callMeMaybe

  return func
