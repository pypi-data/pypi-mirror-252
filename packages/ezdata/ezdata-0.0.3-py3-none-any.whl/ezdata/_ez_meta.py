"""EZMetaclass provides the metaclass from which the EZData class is
derived."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Callable, Any

from icecream import ic

from ezdata import EZNamespace
from utilities import TypedField

if TYPE_CHECKING:
  if sys.version_info >= (3, 8):
    Bases = list[type]
  else:
    from typing import List

    Bases = List[type]
else:
  Bases = tuple[type, ...]

ic.configureOutput(includeContext=True)


class EZMetaMeta(type):
  """Meta-metaclass used to create the EZMeta metaclass. This allows
  customization of __call__ to intercept the namespace between __prepare__
  and __new__. Further, it allows customization of __str__ and __repr__."""

  def __str__(cls) -> str:
    return cls.__qualname__


class EZMeta(type, metaclass=EZMetaMeta):
  """EZMetaclass provides the metaclass from which the EZData class is
  derived."""

  @staticmethod
  def _getCommonTypes() -> list:
    """Returns a list of common types"""
    return [int, float, complex, str, bool, list, dict, set, ]

  @staticmethod
  def _getCommonTypeNames() -> dict:
    """Returns a dictionary containing name, type pairs for common types,
    where name is the value of __qualname__."""
    types = EZMeta._getCommonTypes()
    return {cls.__qualname__: cls for cls in types}

  @staticmethod
  def _getCommonDefaults() -> dict:
    """Returns the default value of the given type or None, if type is not
    a common type. """
    base = {int: 0, float: 0.0, complex: 0j, str: '', bool: False, }
    col = {list: [], dict: dict(), set: set(), }
    out = base | col
    named = {cls.__qualname__: val for (cls, val) in out.items()}
    return out | named

  @staticmethod
  def _getDefaultInstance(type_: type | str) -> Any:
    """Getter-function for the default instance of the given class. If the
    class is a builtin, the value of that class that is Falsy is returned.
    Otherwise, the class should define a default instance at the
    __default_null__ attribute. Finally, an attempt is made to instantiate
    the given class, by invoking its __new__ method."""
    if isinstance(type_, str):
      commonNamespace = EZMeta._getCommonTypeNames()
      localNamespace = locals()
      globalNamespace = globals()
      baseNamespace = commonNamespace | localNamespace | globalNamespace
      namedType = baseNamespace.get(type_, None)
      if namedType is None:
        raise NameError(type_)
      if isinstance(namedType, type):
        return EZMeta._getDefaultInstance(namedType)
      raise TypeError(namedType)
    if type_ in EZMeta._getCommonTypes():
      commonDefaults = EZMeta._getCommonDefaults()
      return commonDefaults.get(type_, )
    if hasattr(type_, '__default_null__'):
      return getattr(type_, '__default_null__', )
    if isinstance(type_, type):
      return type_()
    raise TypeError

  @staticmethod
  def _initSubFactory(cls: type) -> Callable:
    """Why must this exist?"""

    oldInitSub = getattr(cls, '__init_subclass__', object.__init_subclass__)

    def newInitSub(*args, **kwargs) -> None:
      """Fine, I'll take those keyword arguments lmao!"""
      return oldInitSub(*args)

    return newInitSub

  def _initFactory(cls) -> Callable:
    """Factory method creating the __init__ method for the derived
    classes."""

    def __init__(self, *args, **kwargs) -> None:
      if not hasattr(cls, '__field_namespace__'):
        e = """No field namespace were found!"""
        raise ValueError(e)
      fields = getattr(cls, '__field_namespace__', )
      initVals = [*args, ]
      for (i, (name, field)) in enumerate(fields.items()):
        defVal = None
        if i > len(initVals) - 1:
          defVal = field.__default_value__
          valType = field.__value_type__
          if defVal is None:
            defVal = cls._getDefaultInstance(valType)
          initVals.append(defVal)

      for (arg, (name, field)) in zip(initVals, fields.items()):
        field.__set__(self, arg)

    return __init__

  @staticmethod
  def _strFactory() -> Callable:
    """Factory method creating the __str__ method for the derived classes."""

    def __str__(self) -> str:
      cls = self.__class__
      fields = getattr(cls, '__field_namespace__', )
      clsName = cls.__name__
      lines = ['Instance of %s with fields:' % (clsName), ]
      for (key, val) in fields.items():
        lines.append('  %s: %s' % (val, val.__get__(self, cls)))
      return '\n'.join(lines)

    return __str__

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> EZNamespace:
    """Implementation of namespace preparation"""
    nameSpace = EZNamespace()
    nameSpace.className = name
    nameSpace.baseClasses = bases
    return nameSpace

  def __new__(mcls,
              name: str,
              bases: Bases,
              namespace: EZNamespace,
              **kwargs) -> type:
    """Implementation of class creation"""
    fields = namespace.getFields()
    fieldsNamespace = dict()
    for (key, val) in fields.items():
      defaultValue = val.get('defaultValue', None)
      valueType = val.get('fieldClassType', None)
      field = TypedField(defaultValue, valueType)
      fieldsNamespace[key] = field
    simpleNamespace = dict(__field_namespace__=fieldsNamespace, )
    simpleNamespace = {**simpleNamespace, **fieldsNamespace}
    simpleNamespace = {**simpleNamespace, **namespace.getFuncNamespace()}
    varDict = namespace.get('__annotations__', None)
    strFunc = mcls._strFactory()
    simpleNamespace = {**simpleNamespace, **{'__annotations__': varDict}}
    bases = namespace.baseClasses
    for base in bases:
      setattr(base, '__init_subclass__', mcls._initSubFactory(base))
    cls = type.__new__(mcls, name, (*bases,), simpleNamespace, **kwargs)
    initFunc = mcls._initFactory(cls)
    for (key, field) in fieldsNamespace.items():
      field.__set_name__(cls, key)
    setattr(cls, '__initial_name_space__', namespace)
    setattr(cls, '__str__', strFunc)
    setattr(cls, '__init__', initFunc)
    initSubclassFunc = mcls._initSubFactory(cls)
    setattr(cls, '__init_subclass__', initSubclassFunc)
    return cls

  def __str__(cls) -> str:
    """Simplifies the name of the created class"""
    mcls = cls.__class__
    return '%s.%s' % (mcls.__qualname__, cls.__qualname__)

  def __repr__(cls) -> str:
    """Returns the name of the class itself"""
    return cls.__qualname__


class EZData(metaclass=EZMeta):
  """In-between class exposing the functionality from the metaclass"""

  def __init__(self, *args, **kwargs) -> None:
    pass
