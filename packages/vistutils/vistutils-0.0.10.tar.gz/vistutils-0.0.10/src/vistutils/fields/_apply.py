"""The apply decorator permits decoration by setting a particular
attribute. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.fields import AbstractDecorator


class _Apply(AbstractDecorator):
  """The apply decorator permits decoration by setting a particular
  attribute. """

  def __init__(self, key: str, value: Any) -> None:
    pass
