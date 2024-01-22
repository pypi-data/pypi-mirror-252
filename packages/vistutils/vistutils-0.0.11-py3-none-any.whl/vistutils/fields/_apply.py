"""The apply decorator permits decoration by setting a particular
attribute. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Callable


def apply(attribute: str, value: Any) -> Callable:
  """Decorates object by changing given attribute to given value."""
  return lambda callMeMaybe: setattr(callMeMaybe, attribute, value)
