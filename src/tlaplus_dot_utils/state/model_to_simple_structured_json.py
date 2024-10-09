from typing import Any

from .model import (
  FunctionMerge,
  Record,
  RecordField,
  SealedValue,
  SimpleValue,
  SingleElemDomainFunction,
)


def model_to_simple_structured_state_jsonish(
  model: dict[bytes, SealedValue]
) -> dict[str, Any]:
  d = {}
  for key, value in model.items():
    d[key.decode("utf-8")] = _sealed_value_to_reasonable_jsonish(value)
  return d


def _sealed_value_to_reasonable_jsonish(
  model: SealedValue,
) -> dict[str, Any] | str:
  match model:
    case Record(fields):
      return dict(_record_field_to_key_value_tuple(rf) for rf in fields)
    case FunctionMerge(functions):
      return dict(
        _single_elem_domain_function_to_key_value_tuple(fu) for fu in functions
      )
    case SimpleValue(value):
      return value.decode("utf-8")


def _record_field_to_key_value_tuple(model: RecordField) -> tuple[str, Any]:
  return (model.key.decode("utf-8"), model.value.decode("utf-8"))


def _single_elem_domain_function_to_key_value_tuple(
  model: SingleElemDomainFunction,
) -> tuple[str, Any]:
  return (
    model.elem.decode("utf-8"),
    _sealed_value_to_reasonable_jsonish(model.value),
  )
