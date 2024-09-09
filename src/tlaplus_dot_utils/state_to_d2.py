from collections.abc import Mapping
from typing import assert_never

from py_d2 import D2Diagram, D2Shape  # type: ignore

from .state_parsing import FunctionMerge, Record, SealedValue, SimpleValue


def dataclasses_state_to_d2(
  var_name_to_dc: Mapping[bytes, SealedValue | bytes],
  simple_values_inline: bool = True,
) -> str:
  diag = D2Diagram(
    shapes=_dataclasses_state_to_d2_recursive(
      var_name_to_dc, simple_values_inline=simple_values_inline
    )
  )
  return str(diag)


def _dataclasses_state_to_d2_recursive(
  var_name_to_dc: Mapping[bytes, SealedValue | bytes],
  simple_values_inline: bool,
) -> list[D2Shape]:
  shapes = [
    _dataclass_state_to_d2_recursive(
      var_name, dc, i, simple_values_inline=simple_values_inline
    )
    for i, (var_name, dc) in enumerate(var_name_to_dc.items())
  ]

  return shapes


def _dataclass_state_to_d2_recursive(
  var_name: bytes,
  dc: SealedValue | bytes,
  i: int,
  simple_values_inline: bool,
) -> D2Shape:
  subshapes = []
  simple_value = ""
  match dc:
    case Record(fields=fields):
      subshapes = _dataclasses_state_to_d2_recursive(
        {
          f"{field.key.decode('utf-8')} |->".encode("utf-8"): field.value
          for field in fields
        },
        simple_values_inline=simple_values_inline,
      )
    case FunctionMerge(functions=functions):
      subshapes = _dataclasses_state_to_d2_recursive(
        {
          f"{function.elem.decode('utf-8')} :>".encode("utf-8"): function.value
          for function in functions
        },
        simple_values_inline=simple_values_inline,
      )
    case SimpleValue(value=value):
      if simple_values_inline:
        simple_value = f" {value.decode('utf-8')}"
      else:
        subshapes = [D2Shape(name="value", label=f"{value.decode('utf-8')!r}")]
    case bytes() as value:
      if simple_values_inline:
        simple_value = f" {value.decode('utf-8')}"
      else:
        subshapes = [D2Shape(name="value", label=f"{value.decode('utf-8')!r}")]
    case _ as unreachable:
      assert_never(unreachable)

  nl = "\\n" if False else ""  # TODO make configurable
  label = f"{var_name.decode('utf-8') + nl + simple_value}"
  label = '"' + label.strip("'").replace('"', '\\"') + '"'
  shape = D2Shape(name=f"var{i}", label=label)
  for subshape in subshapes:
    shape.add_shape(subshape)

  return shape
