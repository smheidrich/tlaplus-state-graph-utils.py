from typing import Any

from .model import State, Step


def dot_jsonish_to_model(d: dict[str, Any]) -> tuple[list[State], list[Step]]:
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
  return states, steps
