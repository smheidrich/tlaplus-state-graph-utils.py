from typing import Any

from .model import (
  FunctionMerge,
  Record,
  RecordField,
  SealedValue,
  SimpleValue,
  SingleElemDomainFunction,
)

# TODO Move to model_to_structured_json or sth. b/c this is not strictly part
# of the reasonable-json format


def model_to_reasonable_jsonish(
  model: dict[str, SealedValue]
) -> dict[str, Any]:
  return {
    key: _sealed_value_to_reasonable_jsonish(value)
    for key, value in model.items()
  }


def _sealed_value_to_reasonable_jsonish(model: SealedValue) -> dict[str, Any]:
  match model:
    case Record(fields):
      return {
        "type": "record",
        "fields": [_record_field_to_reasonable_jsonish(rf) for rf in fields],
      }
    case FunctionMerge(functions):
      return {
        "type": "functionMerge",
        "functions": [
          _single_elem_domain_function_to_reasonable_jsonish(fu)
          for fu in functions
        ],
      }
    case SimpleValue(value):
      return {"type": "simpleValue", "value": value}


def _record_field_to_reasonable_jsonish(model: RecordField) -> dict[str, Any]:
  return {"type": "recordField", "key": model.key, "value": model.value}


def _single_elem_domain_function_to_reasonable_jsonish(
  model: SingleElemDomainFunction,
) -> dict[str, Any]:
  return {
    "type": "singleElemDomainFunction",
    "elem": model.elem,
    "value": _sealed_value_to_reasonable_jsonish(model.value),
  }
