from typing import Any

from .model import State, Step


def dot_jsonish_to_reasonable_jsonish(d: dict[str, Any]) -> dict[str, Any]:
  # Extract relevant parts
  edge_ds, object_ds = d["edges"], d["objects"]
  state_object_ds = [
    d
    for d in object_ds
    if d["label"]
    and d.get("shape") != "record"
    and d.get("name") != "cluster_legend"
  ]
  legend_ds = [d for d in object_ds if d.get("shape") == "record"]
  legend_color_to_action_name = {d["fillcolor"]: d["name"] for d in legend_ds}

  # Construct dataclass instances
  states = [
    State(
      id=d["_gvid"],
      label_tlaplus=d["label"]
      .replace("\\\\", "\\")
      .replace("\\n", "\n")
      .replace("\\\\", "\\"),
    )
    for d in state_object_ds
  ]
  steps = [
    Step(
      id=d["_gvid"],
      action_name=legend_color_to_action_name[d["color"]],
      from_state_id=d["tail"],
      to_state_id=d["head"],
      color_id=d["color"],
    )
    for d in edge_ds
  ]

  # Return as JSON-ish data structure
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
