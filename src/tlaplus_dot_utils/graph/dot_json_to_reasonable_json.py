from typing import Any

from .dot_json_to_model import dot_jsonish_to_model
from .model_to_reasonable_json import model_to_reasonable_jsonish


def dot_jsonish_to_reasonable_jsonish(
  d: dict[str, Any],
  structured_state: bool,
  simple_structured_state: bool,
  itf_state: bool,
) -> dict[str, Any]:
  model = dot_jsonish_to_model(d)
  return model_to_reasonable_jsonish(
    model, structured_state, simple_structured_state, itf_state
  )
