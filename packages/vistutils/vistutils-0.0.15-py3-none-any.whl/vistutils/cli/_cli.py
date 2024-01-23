"""CLI exposes terminal commands to python objects. Instantiate CLI with
one or more strings that are combined to a single terminal command.
Positional string arguments will be combined with spaces. Positional
arguments that are not strings are replaced with their string
representation. This is recommended only for common types such as ints or
floats. The CLI instantiation can then be used as a decorator on a
standalone function or on a method in a class. The decorated callable
receives an instance of the Res dataclass. This class has slots for stdout
and stderr at 'Res.out' and 'Res.err'. When the decorated callable is
called, the command in the decorator is run and the Res object then passed
to the decorated function as the first positional argument followed by any
other arguments received in the original call."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import subprocess
from typing import Callable, Any

from vistutils import monoSpace
from vistutils.cli import Res


class CLI:
  """The CLI class provides a method decorator to indicate that the
  decorated method is to receive the stdout and stderr from the commands
  sent to the constructor."""

  @staticmethod
  def _cleanString(msg: str) -> str:
    """Returns a cleaned up version of the string"""
    return msg.replace('\t', '  ')

  def __init__(self, *args, **kwargs) -> None:
    strArgs = [arg for arg in args if isinstance(arg, str)]
    self._command = ' '.join(strArgs)
    self.__inner_function__ = None

  def __call__(self, *args, **kwargs) -> Any:
    """Sets the inner function or if inner function is already defined,
    runs the defined command and passes stdout and stderr to inner
    function."""
    callMeMaybe = None
    if len(args) == 1 and not kwargs:
      if callable(args[0]):
        callMeMaybe = args[0]
    if self.__inner_function__ is None and callMeMaybe is None:
      if self._command is None:
        raise RuntimeError
      return self._run()
    if self.__inner_function__ is None and callable(callMeMaybe):
      self._setInnerFunction(callMeMaybe)
      return self
    if callMeMaybe is not None and not callable(callMeMaybe):
      e = """Expected a callable but received '%s' of type '%s'."""
      actType = type(callMeMaybe)
      raise TypeError(monoSpace(e % (callMeMaybe, actType)))
    res = self._run()
    return self.__inner_function__(res, *args, **kwargs)

  def _setInnerFunction(self, callMeMaybe: Callable) -> None:
    """Sets the inner function to given callable"""
    self.__inner_function__ = callMeMaybe

  def _run(self) -> Res:
    """Executes the command in the command line"""
    res = subprocess.run(self._command, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = self._cleanString(res.stdout.decode('utf-8'))
    err = self._cleanString(res.stderr.decode('utf-8'))
    return Res(out, err)
