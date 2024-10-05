import subprocess as sp

from tlaplus_dot_utils.graph.model import TransitionDiagram
from tlaplus_dot_utils.graph.model_to_d2 import (
  BoxesStateDiagramToD2Renderer,
  LatexStateDiagramToD2Renderer,
  SimpleStateDiagramToD2Renderer,
  model_to_d2_str,
)
from tlaplus_dot_utils.state.model_to_d2 import (
  BoxesSimpleValuesInlineNewlineSepStateToD2Renderer,
  BoxesSimpleValuesInlineStateToD2Renderer,
  BoxesStateToD2Renderer,
)


def format_d2(d2: str) -> str:
  cp = sp.run(
    ["d2", "fmt", "-"], input=d2, check=True, encoding="utf-8", stdout=sp.PIPE
  )
  return cp.stdout


def test_long_example_boxes_simple_values_inline_against_reference(
  long_example_model: TransitionDiagram,
  long_example_d2_boxes_simple_values_inline: str,
) -> None:
  # Run
  d2 = format_d2(
    model_to_d2_str(
      long_example_model,
      renderer=BoxesStateDiagramToD2Renderer(
        BoxesSimpleValuesInlineStateToD2Renderer()
      ),
    )
  )

  # Uncomment to regenerate:
  # from pathlib import Path
  # Path("tests/data/long-example/boxes-simple-values-inline.d2").write_text(d2)

  # Check
  assert d2 == long_example_d2_boxes_simple_values_inline


def test_long_example_boxes_simple_values_inline_newline_against_reference(
  long_example_model: TransitionDiagram,
  long_example_d2_boxes_simple_values_inline_newline: str,
) -> None:
  # Run
  d2 = format_d2(
    model_to_d2_str(
      long_example_model,
      renderer=BoxesStateDiagramToD2Renderer(
        BoxesSimpleValuesInlineNewlineSepStateToD2Renderer()
      ),
    )
  )

  # Uncomment to regenerate:
  # from pathlib import Path
  # Path(
  # "tests/data/long-example/boxes-simple-values-inline-newline.d2"
  # ).write_text(d2)

  # Check
  assert d2 == long_example_d2_boxes_simple_values_inline_newline


def test_long_example_boxes_simple_values_not_inline_against_reference(
  long_example_model: TransitionDiagram,
  long_example_d2_boxes_simple_values_not_inline: str,
) -> None:
  # Run
  d2 = format_d2(
    model_to_d2_str(
      long_example_model,
      renderer=BoxesStateDiagramToD2Renderer(BoxesStateToD2Renderer()),
    )
  )

  # Uncomment to regenerate:
  # from pathlib import Path
  # Path("tests/data/long-example/boxes-simple-values-not-inline.d2").write_text(
  # d2
  # )

  # Check
  assert d2 == long_example_d2_boxes_simple_values_not_inline


def test_long_example_latex_against_reference(
  long_example_model: TransitionDiagram,
  long_example_d2_latex: str,
) -> None:
  # Run
  d2 = format_d2(
    model_to_d2_str(
      long_example_model, renderer=LatexStateDiagramToD2Renderer()
    )
  )

  # Uncomment to regenerate:
  # from pathlib import Path
  # Path("tests/data/long-example/latex.d2").write_text(d2)

  # Check
  assert d2 == long_example_d2_latex


def test_long_example_non_latex_against_reference(
  long_example_model: TransitionDiagram,
  long_example_d2_non_latex: str,
) -> None:
  # Run
  d2 = format_d2(
    model_to_d2_str(
      long_example_model, renderer=SimpleStateDiagramToD2Renderer()
    )
  )

  # Uncomment to regenerate:
  # from pathlib import Path
  # Path("tests/data/long-example/non-latex.d2").write_text(d2)

  # Check
  assert d2 == long_example_d2_non_latex
