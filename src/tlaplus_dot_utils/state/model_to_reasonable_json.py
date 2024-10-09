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
  model: dict[bytes, SealedValue]
) -> dict[str, Any]:
  d = {}
  for key, value in model.items():
    d[key.decode("utf-8")] = _sealed_value_to_reasonable_jsonish(value)
  return d


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
      return {"type": "simpleValue", "value": value.decode("utf-8")}


def _record_field_to_reasonable_jsonish(model: RecordField) -> dict[str, Any]:
  return {
    "type": "recordField",
    "key": model.key.decode("utf-8"),
    "value": model.value.decode("utf-8"),
  }


def _single_elem_domain_function_to_reasonable_jsonish(
  model: SingleElemDomainFunction,
) -> dict[str, Any]:
  return {
    "type": "singleElemDomainFunction",
    "elem": model.elem.decode("utf-8"),
    "value": _sealed_value_to_reasonable_jsonish(model.value),
  }
