from typing import Any

from ..state.model_to_reasonable_json import (
  model_to_reasonable_jsonish as state_model_to_reasonable_jsonish,
)
from ..state.tlaplus_to_model import tlaplus_state_to_dataclasses
from .model import TransitionDiagram


def model_to_reasonable_jsonish(
  model: TransitionDiagram, structured_state: bool
) -> dict[str, Any]:
  return {
    "metadata": {
      "format": {
        "name": "reasonable-tlaplus-state-graph-json",
        "version": "0.1.1",
      },
    },
    "states": [
      {
        "id": state.id,
        "labelTlaPlus": state.label_tlaplus,
        **(
          {
            "structuredState": state_model_to_reasonable_jsonish(
              tlaplus_state_to_dataclasses(state.label_tlaplus)
            )
          }
          if structured_state
          else {}
        ),
      }
      for state in model.states
    ],
    "steps": [
      {
        "id": step.id,
        "actionName": step.action_name,
        "fromStateId": step.from_state_id,
        "toStateId": step.to_state_id,
        "colorId": step.color_id,
      }
      for step in model.steps
    ],
  }
