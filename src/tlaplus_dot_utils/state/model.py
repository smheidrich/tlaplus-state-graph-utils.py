from dataclasses import dataclass
from typing import TypeAlias


@dataclass
class RecordField:
  key: bytes
  value: bytes  # TODO! Nested model instead of bytes


@dataclass
class Record:
  fields: list[RecordField]


@dataclass
class SingleElemDomainFunction:
  elem: bytes
  value: "SealedValue"


@dataclass
class FunctionMerge:
  functions: list[SingleElemDomainFunction]


@dataclass
class SimpleValue:
  value: bytes


SealedValue: TypeAlias = Record | FunctionMerge | SimpleValue
