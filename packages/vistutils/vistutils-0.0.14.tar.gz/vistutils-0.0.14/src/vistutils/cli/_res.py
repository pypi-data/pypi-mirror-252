"""Res provides a dataclass representation of the results of a call to the
external command line. The stdout and stderr received are accessed by the
slots: out and err."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezdata import EZData

from vistutils import monoSpace


class Res(EZData):
  """Res provides a dataclass representation of the results of a call to the
  external command line. The stdout and stderr received are accessed by the
  slots: out and err."""
  out: str
  err: str
  cmd: str

  def _getOutLines(self) -> list[str]:
    """Getter-function for stdout as list of lines:"""
    if self.out:
      return [arg.strip() for arg in self.out.split('\n')]
    return []

  def _getErrLines(self) -> list[str]:
    """Getter-function for stderr as list of lines:"""
    if self.err:
      return [arg.strip() for arg in self.err.split('\n')]
    return []

  def __str__(self) -> str:
    """String representation"""
    header = monoSpace("Terminal command: <%s>" % self.cmd)
    if self.err:
      err = '\n  '.join(self._getErrLines())
      if self.out:
        out = '\n  '.join(self._getOutLines())
        msg = '%s\nStandard Output:\n%s\nStandard Error:\n%s'
        return msg % (header, out, err)
      else:
        msg = '%s\nStandard Error:\n%s'
        return msg % (header, err)
    else:
      if self.out:
        out = '\n  '.join(self._getOutLines())
        msg = '%s\nStandard Output:\n%s'
        return msg % (header, out)
      else:
        return monoSpace('%s yielded no response' % header)
