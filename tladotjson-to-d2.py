#!/usr/bin/env python3
import json
from collections import defaultdict
from dataclasses import dataclass
from sys import stderr, stdin
from textwrap import dedent, indent

latex: bool = True


@dataclass
class State:
  id: int
  label_tlaplus: str

  @property
  def label_latex(self) -> str:
    # TODO Surely there is a way to use TLA+'s own LaTeX-output
    #  programmatically somehow so we don't have to do this?
    return (
      self.label_tlaplus.replace("/\\", "\\land")
      .replace(r"\/", "\\lor")
      .replace("|->", "\\mapsto")
      .replace("\n", " \\\\ ")
      .replace("FALSE", "\\mathrm{FALSE}")
      .replace("TRUE", "\\mathrm{TRUE}")
      .replace('"', '\\text{"}')  # these look like garbage otherwise
    )


@dataclass
class Action:
  id: int
  name: str
  from_state_id: int
  to_state_id: int
  color_id: str


if __name__ == "__main__":
  # Parse TLA+-produced dot-JSON
  d = json.load(stdin)
  edge_ds, object_ds = d["edges"], d["objects"]
  state_object_ds = [
    d
    for d in object_ds
    if d["label"]
    and d.get("shape") != "record"
    and d.get("name") != "cluster_legend"
  ]
  legend_ds = [d for d in object_ds if d.get("shape") == "record"]
  legend_color_to_name = {d["fillcolor"]: d["name"] for d in legend_ds}

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
  actions = [
    Action(
      id=d["_gvid"],
      name=legend_color_to_name[d["color"]],
      from_state_id=d["tail"],
      to_state_id=d["head"],
      color_id=d["color"],
    )
    for d in edge_ds
  ]

  # Output as D2
  for state in states:
    # States
    if latex:
      label = repr(state.label_latex)[1:-1]
      print(
        dedent(
          f"""\
            state{state.id}: "" {{
                equation: |latex
                    \\\\displaylines {{
                        {indent(label, "    ")}
                    }}
                    % add some spacing (otherwise it messes up)
                    \\\\ \\\\ \\\\ \\\\ \\\\ \\\\
                |
            }}
            """
        )
      )
    else:
      label = repr(state.label_tlaplus).replace('"', '\\"')
      label = f'"{label[1:-1]}"'
      print(f"state{state.id}: {label}")

  print("")

  # Actions
  color_id_to_color = defaultdict(
    lambda: "black",
    {
      "0": "red",
      "1": "blue",
      "2": "green",
      "3": "orange",
      "4": "purple",
      "5": "cyan",
    },
  )
  for action in actions:
    label = repr(action.name)
    label = f'"{label[1:-1]}"'
    print(
      f"state{action.from_state_id} -> state{action.to_state_id}: {label} {{"
    )
    print("  style: {")
    print(f"     stroke: {color_id_to_color[action.color_id]}")
    print("  }")
    print("}")

  print("All done", file=stderr)
