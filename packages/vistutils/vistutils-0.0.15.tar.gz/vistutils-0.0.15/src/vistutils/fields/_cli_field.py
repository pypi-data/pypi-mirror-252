"""CLIField provides a descriptor like decorator where the __get__ is the
method decorated."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.cli import CLI
from vistutils.fields import AbstractField


class CLIField(AbstractField):
  """CLIField provides a descriptor like decorator where the __get__
  returns the stdout and stderr from a given command. By default,
  if the stderr is empty, stdout is returned. Otherwise, a RuntimeError is
  raised on the stderr."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)
    strArgs = [arg.strip() for arg in args if isinstance(arg, str)]
    if not strArgs:
      raise TypeError
    self._command = ' '.join(strArgs)
    self._cli = CLI(self._command)

  def __prepare_owner__(self, owner: type) -> type:
    """Implementation of abstract method"""
    return owner
