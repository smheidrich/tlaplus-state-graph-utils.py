import json
import subprocess as sp
from io import StringIO
from typing import Any
from unittest.mock import patch

from tlaplus_dot_utils.reasonable_json_to_d2 import parse_and_write_d2


def format_d2(d2: str) -> str:
  cp = sp.run(
    ["d2", "fmt", "-"], input=d2, check=True, encoding="utf-8", stdout=sp.PIPE
  )
  return cp.stdout


def test_long_example_boxes_inline_simple_values_against_reference(
  long_example_reasonable_json: dict[str, Any],
  long_example_d2_boxes_inline_simple_values: str,
) -> None:
  # Run
  out = StringIO()
  parse_and_write_d2(StringIO(json.dumps(long_example_reasonable_json)), out)
  out.seek(0)
  d2 = format_d2(out.read())

  # Uncomment to regenerate:
  # from pathlib import Path
  # Path("tests/data/long-example/boxes-inline-simple-values.d2").write_text(d2)

  # Check
  assert d2 == long_example_d2_boxes_inline_simple_values


@patch("tlaplus_dot_utils.reasonable_json_to_d2.latex", True)
@patch("tlaplus_dot_utils.reasonable_json_to_d2.latex", False)
def test_long_example_latex_against_reference(
  long_example_reasonable_json: dict[str, Any],
  long_example_d2_latex: str,
) -> None:
  # Run
  out = StringIO()
  parse_and_write_d2(StringIO(json.dumps(long_example_reasonable_json)), out)
  out.seek(0)
  d2 = format_d2(out.read())

  # Uncomment to regenerate:
  # from pathlib import Path
  # Path("tests/data/long-example/latex.d2").write_text(d2)

  # Check
  assert d2 == long_example_d2_latex
