import json
from collections import defaultdict
from collections.abc import Callable
from os import getenv
from textwrap import dedent, indent
from typing import IO, Any

from py_d2 import D2Shape  # type: ignore[import-untyped]
from py_d2 import D2Connection, D2Diagram, D2Style, D2Text

from .model import State, Step, TransitionDiagram
from .state_parsing import tlaplus_state_to_dataclasses
from .state_to_d2 import BaseStateToD2Renderer

latex: bool = bool(getenv("TLAPLUS_D2_LATEX", False))


def state_label_to_latex(state: State) -> str:
  # TODO Surely there is a way to use TLA+'s own LaTeX-output
  #  programmatically somehow so we don't have to do this?
  return (
    state.label_tlaplus.replace("/\\", "\\land")
    .replace(r"\/", "\\lor")
    .replace("|->", "\\mapsto")
    .replace("\n", " \\\\ ")
    .replace("FALSE", "\\mathrm{FALSE}")
    .replace("TRUE", "\\mathrm{TRUE}")
    .replace('"', '\\text{"}')  # these look like garbage otherwise
  )


def parse_from_reasonable_json_file(infile: IO[Any]) -> TransitionDiagram:
  # Parse JSON
  d = json.load(infile)

  # Check metadata version
  try:
    version_str = d["metadata"]["format"]["version"]
    version = tuple(int(x) for x in version_str.split("."))
    if len(version) < 3:
      version = (*version, 0)
  except Exception as e:
    raise ValueError(
      "Couldn't determine format version (see errors above)"
    ) from e
  if not (0, 1, 0) <= version < (0, 2, 0):
    raise ValueError(f"Can't handle format version {version_str}")

  # Construct dataclass instances
  states = [
    State(
      id=state_d["id"],
      label_tlaplus=state_d["labelTlaPlus"],
    )
    for state_d in d["states"]
  ]
  steps = [
    Step(
      id=step_d["id"],
      action_name=step_d["actionName"],
      from_state_id=step_d["fromStateId"],
      to_state_id=step_d["toStateId"],
      color_id=step_d["colorId"],
    )
    for step_d in d["steps"]
  ]

  return TransitionDiagram(states, steps)


def parse_and_write_d2(
  infile: IO[Any],
  outfile: IO[str],
  box_state_render_cls: type[BaseStateToD2Renderer] | None = None,
) -> None:
  diagram = parse_from_reasonable_json_file(infile)

  # Shortcut:
  writeln: Callable[[str], Any] = lambda s: outfile.write(f"{s}\n")

  writeln(
    str(to_d2_diagram(diagram, box_state_render_cls=box_state_render_cls))
  )


def to_d2_diagram(
  diagram: TransitionDiagram,
  box_state_render_cls: type[BaseStateToD2Renderer] | None,
) -> D2Diagram:
  shapes = []
  for state in diagram.states:
    # States
    if latex:
      label = repr(state_label_to_latex(state))[1:-1]
      shape = D2Shape(
        name=f"state{state.id}",
        label='""',
        equation=D2Text(
          dedent(
            f"""\
           \\\\displaylines {{
               {indent(label, "    ")}
           }}
           % add some spacing (otherwise it messes up)
           \\\\ \\\\ \\\\ \\\\ \\\\ \\\\
           """.rstrip(),
          ),
          "latex",
        ),
      )
    elif box_state_render_cls is not None:
      box_renderer = box_state_render_cls()
      state_boxes = box_renderer.to_d2_shapes(
        tlaplus_state_to_dataclasses(state.label_tlaplus)
      )
      shape = D2Shape(name=f"state{state.id}", label='""')
      for subshape in state_boxes:
        shape.add_shape(subshape)
    else:
      label = repr(state.label_tlaplus).replace('"', '\\"')
      label = f'"{label[1:-1]}"'
      shape = D2Shape(name=f"state{state.id}", label=label)
    shapes.append(shape)

  # Steps
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
  connections = []
  for step in diagram.steps:
    label = repr(step.action_name)
    label = f'"{label[1:-1]}"'
    conn = CustomD2Connection(
      f"state{step.from_state_id}",
      f"state{step.to_state_id}",
      label,
      style=D2Style(stroke=color_id_to_color[step.color_id]),
    )
    connections.append(conn)

  return D2Diagram(shapes=shapes, connections=connections)


# TODO Remove once this is implemented in py-d2 itself:
#   https://github.com/MrBlenny/py-d2/issues/22
class CustomD2Connection(D2Connection):  # type: ignore[misc]
  style: D2Style

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    if "style" in kwargs:
      self.style = kwargs.pop("style")
    else:
      self.style = None
    super().__init__(*args, **kwargs)

  def lines(self) -> list[str]:
    lines = super().lines()
    if self.style is not None:
      lines[0] = f"{lines[0]} {{"
      lines.extend(self.style.lines())
      lines.append("}")
    return lines  # type: ignore[no-any-return]
