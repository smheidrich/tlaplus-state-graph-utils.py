from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from typing import assert_never

from py_d2 import D2Diagram, D2Shape  # type: ignore

from ..state_parsing import FunctionMerge, Record, SealedValue, SimpleValue


@dataclass
class BaseStateToD2Renderer(ABC):
  def __call__(
    self, var_name_to_dc: Mapping[bytes, SealedValue | bytes]
  ) -> str:
    diag = D2Diagram(shapes=self.to_d2_shapes(var_name_to_dc))
    return str(diag)

  def to_d2_shapes(
    self, var_name_to_dc: Mapping[bytes, SealedValue | bytes]
  ) -> list[D2Shape]:
    return self._dataclasses_state_to_d2_recursive(var_name_to_dc)

  def _dataclasses_state_to_d2_recursive(
    self, var_name_to_dc: Mapping[bytes, SealedValue | bytes]
  ) -> list[D2Shape]:
    shapes = [
      self._dataclass_state_to_d2_recursive(var_name, dc, i)
      for i, (var_name, dc) in enumerate(var_name_to_dc.items())
    ]

    return shapes

  @abstractmethod
  def _dataclass_state_to_d2_recursive(
    self, var_name: bytes, dc: SealedValue | bytes, i: int
  ) -> D2Shape:
    ...


class BoxesStateToD2Renderer(BaseStateToD2Renderer):
  def _dataclass_state_to_d2_recursive(
    self, var_name: bytes, dc: SealedValue | bytes, i: int
  ) -> D2Shape:
    subshapes = []
    match dc:
      case Record(fields=fields):
        subshapes = self._dataclasses_state_to_d2_recursive(
          {
            f"{field.key.decode('utf-8')} |->".encode("utf-8"): field.value
            for field in fields
          },
        )
      case FunctionMerge(functions=functions):
        subshapes = self._dataclasses_state_to_d2_recursive(
          {
            f"{function.elem.decode('utf-8')} :>".encode(
              "utf-8"
            ): function.value
            for function in functions
          },
        )
      case SimpleValue(value=value):
        subshapes = [D2Shape(name="value", label=f"{value.decode('utf-8')!r}")]
      case bytes() as value:
        subshapes = [D2Shape(name="value", label=f"{value.decode('utf-8')!r}")]
      case _ as unreachable:
        assert_never(unreachable)

    label = f"{var_name.decode('utf-8')}"
    label = '"' + label.strip("'").replace('"', '\\"') + '"'
    shape = D2Shape(name=f"var{i}", label=label)
    for subshape in subshapes:
      shape.add_shape(subshape)

    return shape


class BoxesSimpleValuesInlineStateToD2Renderer(BaseStateToD2Renderer):
  def _dataclass_state_to_d2_recursive(
    self, var_name: bytes, dc: SealedValue | bytes, i: int
  ) -> D2Shape:
    subshapes = []
    simple_value = ""
    match dc:
      case Record(fields=fields):
        subshapes = self._dataclasses_state_to_d2_recursive(
          {
            f"{field.key.decode('utf-8')} |->".encode("utf-8"): field.value
            for field in fields
          },
        )
      case FunctionMerge(functions=functions):
        subshapes = self._dataclasses_state_to_d2_recursive(
          {
            f"{function.elem.decode('utf-8')} :>".encode(
              "utf-8"
            ): function.value
            for function in functions
          },
        )
      case SimpleValue(value=value):
        simple_value = f" {value.decode('utf-8')}"
      case bytes() as value:
        simple_value = f" {value.decode('utf-8')}"
      case _ as unreachable:
        assert_never(unreachable)

    label = f"{var_name.decode('utf-8') + simple_value}"
    label = '"' + label.strip("'").replace('"', '\\"') + '"'
    shape = D2Shape(name=f"var{i}", label=label)
    for subshape in subshapes:
      shape.add_shape(subshape)

    return shape


class BoxesSimpleValuesInlineNewlineSepStateToD2Renderer(
  BaseStateToD2Renderer
):
  def _dataclass_state_to_d2_recursive(
    self, var_name: bytes, dc: SealedValue | bytes, i: int
  ) -> D2Shape:
    subshapes = []
    simple_value = ""
    match dc:
      case Record(fields=fields):
        subshapes = self._dataclasses_state_to_d2_recursive(
          {
            f"{field.key.decode('utf-8')} |->".encode("utf-8"): field.value
            for field in fields
          },
        )
      case FunctionMerge(functions=functions):
        subshapes = self._dataclasses_state_to_d2_recursive(
          {
            f"{function.elem.decode('utf-8')} :>".encode(
              "utf-8"
            ): function.value
            for function in functions
          },
        )
      case SimpleValue(value=value):
        simple_value = f" {value.decode('utf-8')}"
      case bytes() as value:
        simple_value = f" {value.decode('utf-8')}"
      case _ as unreachable:
        assert_never(unreachable)

    label = f"{var_name.decode('utf-8')}\\n{simple_value}"
    label = '"' + label.strip("'").replace('"', '\\"') + '"'
    shape = D2Shape(name=f"var{i}", label=label)
    for subshape in subshapes:
      shape.add_shape(subshape)

    return shape
