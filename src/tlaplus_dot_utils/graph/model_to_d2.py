from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from textwrap import dedent, indent
from typing import IO, Any

from py_d2 import D2Shape  # type: ignore[import-untyped]
from py_d2 import D2Connection, D2Diagram, D2Style, D2Text

from ..state.model_to_d2 import BaseStateToD2Renderer
from ..state.tlaplus_to_latex import state_tlaplus_to_latex
from ..state.tlaplus_to_model import tlaplus_state_to_dataclasses
from .model import State, TransitionDiagram
from .reasonable_json_to_model import parse_from_reasonable_json_file


def parse_and_render_d2(
  infile: IO[Any], renderer: "BaseDiagramToD2Renderer"
) -> str:
  diagram = parse_from_reasonable_json_file(infile)

  rendered_as_d2 = renderer(diagram)

  return str(rendered_as_d2) + "\n"


class BaseDiagramToD2Renderer(ABC):
  def __call__(self, diagram: TransitionDiagram) -> D2Diagram:
    shapes = []
    for state in diagram.states:
      self._render_state(state)
      # States
      shape = self._render_state(state)
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

  @abstractmethod
  def _render_state(self, state: State) -> D2Shape:
    ...


class LatexStateDiagramToD2Renderer(BaseDiagramToD2Renderer):
  def _render_state(self, state: State) -> D2Shape:
    label = repr(state_tlaplus_to_latex(state.label_tlaplus))[1:-1]
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
    return shape


@dataclass
class BoxesStateDiagramToD2Renderer(BaseDiagramToD2Renderer):
  box_state_render: BaseStateToD2Renderer

  def _render_state(self, state: State) -> D2Shape:
    box_renderer = self.box_state_render
    state_boxes = box_renderer.to_d2_shapes(
      tlaplus_state_to_dataclasses(state.label_tlaplus)
    )
    shape = D2Shape(name=f"state{state.id}", label='""')
    for subshape in state_boxes:
      shape.add_shape(subshape)
    return shape


class SimpleStateDiagramToD2Renderer(BaseDiagramToD2Renderer):
  def _render_state(self, state: State) -> D2Shape:
    label = repr(state.label_tlaplus).replace('"', '\\"')
    label = f'"{label[1:-1]}"'
    shape = D2Shape(name=f"state{state.id}", label=label)
    return shape


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
