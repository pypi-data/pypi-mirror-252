"""TypedField provides a strongly typed descriptor class. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Any

from ezdata import EZData

from vistutils import monoSpace, stringList, searchKey
from vistutils.fields import AbstractField
from vistutils.waitaminute import typeMsg


class TypedValue(EZData):
  """Dataclass representing a type and an optional value"""
  valueType: type
  defaultValue: object

  @classmethod
  def null(cls) -> Self:
    """Creates the null instance. This has type NoneType, and default
    value None."""
    return cls(type(None), None)

  def __bool__(self, ) -> bool:
    if self.valueType is type(None):
      return False
    return True

  def __mul__(self, other: Self) -> Self:
    """New instance has same type as self, but may have the default value
    from other"""
    valueType = None
    if self.valueType is not type(None):
      valueType = self.valueType
    elif other.valueType is not type(None):
      valueType = other.valueType
    else:
      return TypedValue.null()
    if isinstance(self.defaultValue, valueType):
      return TypedValue(valueType, self.defaultValue)
    if isinstance(other.defaultValue, valueType):
      return TypedValue(valueType, other.defaultValue)
    return TypedValue(valueType)

  def __str__(self, ) -> str:
    """String representation"""
    defVal = self.defaultValue
    type_ = self.valueType
    return 'TypedValue of type: %s and value: %s' % (type_, defVal)

  def __repr__(self, ) -> str:
    """Code representation"""
    defVal = self.defaultValue
    type_ = self.valueType
    return 'TypedValue(%s, %s)' % (type_, defVal)


class TypedField(AbstractField):
  """TypedField provides a strongly typed descriptor class. """

  @staticmethod
  def _parseKwargs(**kwargs) -> TypedValue:
    """Parses keyword arguments"""
    valueTypeKeys = stringList("""type, type_, valueType, cls""")
    valueTypeKwarg = searchKey(type, *valueTypeKeys, **kwargs)
    defValKeys = stringList("""default, defaultValue, defVal, val0""")
    defValKwarg = searchKey(*defValKeys, **kwargs)
    if valueTypeKwarg is None:
      return TypedValue.null()
    return TypedValue(valueTypeKwarg, defValKwarg)

  @staticmethod
  def _parseArgs(*args, ) -> TypedValue:
    """Parses positional arguments"""
    if not args:
      return TypedValue.null()
    typeArg = None
    defValArg = None
    for arg in args:
      if isinstance(arg, type):
        typeArg = arg
    if typeArg is None:
      defValArg = args[0]
      typeArg = type(defValArg)
      return TypedValue(typeArg, defValArg)
    for arg in args:
      if isinstance(arg, typeArg):
        return TypedValue(typeArg, arg)
    return TypedValue(typeArg, )

  @staticmethod
  def _parse(*args, **kwargs) -> TypedValue:
    """Parses arguments"""
    valueKwarg = TypedField._parseKwargs(**kwargs)
    valueArg = TypedField._parseArgs(*args)
    if not all([isinstance(a, TypedValue) for a in [valueKwarg, valueArg]]):
      raise TypeError
    return valueKwarg * valueArg

  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)
    parsed = self._parse(*args, **kwargs)
    self._valueType = parsed.valueType
    self._defaultValue = parsed.defaultValue
    if self._valueType is type(None):
      raise TypeError

  def typeGuard(self, value: Any) -> bool:
    """If the given value does not belong to the value type, this method
    returns False, otherwise True"""
    return True if isinstance(value, self._valueType) else False

  def _getPrivateName(self) -> str:
    """Getter-function for the private name"""
    return '_%s' % self.__field_name__

  def __prepare_owner__(self, owner: type) -> type:
    """Implementation of abstract method"""
    if not hasattr(owner, '__descriptor_fields__'):
      setattr(owner, '__descriptor_fields__', [])

      def fieldInit(this, *args, **kwargs) -> None:
        """Addition to initiator"""
        fields = getattr(owner, '__descriptor_fields__', [])
        args = [*args, ]
        while len(args) < len(fields):
          args.append(None)
        for (field, arg) in zip(fields, args):
          if isinstance(field, TypedField):
            if field.typeGuard(arg) or arg is None:
              setattr(this, field._getPrivateName(), arg)
            else:
              raise TypeError
          else:
            raise TypeError

      oldInit = getattr(owner, '__init__', None)
      if oldInit is object.__init__:
        oldInit = lambda this, *args, **kwargs: None
      if hasattr(oldInit, '__func__'):
        oldInit = getattr(oldInit, '__func__')

      def newInit(this, *args, **kwargs) -> None:
        """Replacement init function"""
        oldInit(this, *args, **kwargs)
        fieldInit(this, *args, **kwargs)

      setattr(owner, '__init__', newInit)

    existingFields = getattr(owner, '__descriptor_fields__')
    setattr(owner, '__descriptor_fields__', [*existingFields, self])
    pvtName = self._getPrivateName()
    if hasattr(owner, pvtName) or self._defaultValue is None:
      return owner
    setattr(owner, pvtName, self._defaultValue)
    return owner

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """Implementation of getter"""
    pvtName = self._getPrivateName()
    if hasattr(instance, pvtName):
      return getattr(instance, pvtName)
    if kwargs.get('_recursion', False):
      raise RecursionError
    setattr(instance, pvtName, self._defaultValue)
    return self.__get__(instance, owner, _recursion=True, **kwargs)

  def __set__(self, instance: Any, value: Any) -> None:
    """Implementation of setter"""
    if not isinstance(value, self._valueType):
      e = typeMsg('value', value, self._valueType)
      raise TypeError(e)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, value)

  def __delete__(self, instance: Any) -> None:
    """Runs delattr, but raises attribute error if not assigned"""
    pvtName = self._getPrivateName()
    if hasattr(instance, pvtName):
      return delattr(instance, pvtName)
    e = """Tried to delete attribute named '%s', which is not defined on 
    the instance!"""
    raise AttributeError(monoSpace(e % pvtName))
