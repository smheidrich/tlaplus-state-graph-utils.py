from typing import Any

from .model import State, Step


def model_to_reasonable_jsonish(
  states: list[State], steps: list[Step]
) -> dict[str, Any]:
  return {
    "metadata": {
      "format": {
        "name": "reasonable-tlaplus-state-graph-json",
        "version": "0.1",
      },
    },
    "states": [
      {
        "id": state.id,
        "labelTlaPlus": state.label_tlaplus,
      }
      for state in states
    ],
    "steps": [
      {
        "id": step.id,
        "actionName": step.action_name,
        "fromStateId": step.from_state_id,
        "toStateId": step.to_state_id,
        "colorId": step.color_id,
      }
      for step in steps
    ],
  }
