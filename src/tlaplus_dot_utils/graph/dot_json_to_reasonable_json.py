from typing import Any

from .dot_json_to_model import dot_jsonish_to_model
from .model_to_reasonable_json import model_to_reasonable_jsonish


def dot_jsonish_to_reasonable_jsonish(d: dict[str, Any]) -> dict[str, Any]:
  model = dot_jsonish_to_model(d)
  return model_to_reasonable_jsonish(model)
