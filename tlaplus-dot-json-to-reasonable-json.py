#!/usr/bin/env python3
# PEP 723 metadata:
# /// script
# requires-python = ">=3.9,<4"
# ///
import json
from argparse import ArgumentParser, FileType
from dataclasses import dataclass
from typing import IO, Any

__version__ = "0.1.0"


# Core


@dataclass
class State:
  id: int
  label_tlaplus: str


@dataclass
class Step:
  id: int
  action_name: str
  from_state_id: int
  to_state_id: int
  color_id: str


def parse_and_return_jsonish(file: IO[Any]) -> dict[str, Any]:
  # Load JSON
  d = json.load(file)

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


# CLI


arg_parser = ArgumentParser(
  description='convert JSON produced from TLA+ dot files to "reasonable" '
  "JSON that is easier to work with"
)
arg_parser.add_argument(
  "input",
  type=FileType("r"),
  default="-",
  nargs="?",
  help="input file path or '-' to use stdin (the default)",
)
arg_parser.add_argument(
  "--output",
  "-o",
  type=FileType("w"),
  default="-",
  help="output file path or '-' to use stdout (the default)",
)
arg_parser.add_argument(
  "--pretty",
  action="store_true",
  help="pretty-printed rather than compact JSON",
)
arg_parser.add_argument(
  "--version", action="version", version=f"%(prog)s {__version__}"
)


def run_cli() -> None:
  args = arg_parser.parse_args()

  jsonish = parse_and_return_jsonish(args.input)

  if args.pretty:
    json.dump(jsonish, args.output, indent=2)
  else:
    json.dump(jsonish, args.output)


if __name__ == "__main__":
  run_cli()
