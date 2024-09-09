import json
import subprocess as sp
from io import StringIO
from typing import Any

import pytest

from tlaplus_dot_utils.reasonable_json_to_d2 import parse_and_write_d2


@pytest.fixture
def example_reasonable_json() -> dict[str, Any]:
  # TODO use pkg_resources or w/e
  # TODO combine w/ other fixture reading the same file, use better names
  with open("tests/data/expected-dot-json-example-to-reasonable.json") as f:
    return json.load(f)  # type: ignore[no-any-return]


@pytest.fixture
def expected_example_reasonable_json_to_d2() -> str:
  # TODO use pkg_resources or w/e
  with open("tests/data/expected.d2") as f:
    return f.read()


def format_d2(d2: str) -> str:
  cp = sp.run(
    ["d2", "fmt", "-"], input=d2, check=True, encoding="utf-8", stdout=sp.PIPE
  )
  return cp.stdout


def test_example_against_reference(
  example_reasonable_json: dict[str, Any],
  expected_example_reasonable_json_to_d2: str,
) -> None:
  # Run
  out = StringIO()
  parse_and_write_d2(StringIO(json.dumps(example_reasonable_json)), out)
  out.seek(0)
  d2 = format_d2(out.read())

  # Uncomment to regenerate:
  # from pathlib import Path
  # Path("tests/data/expected.d2").write_text(format_d2(d2))

  # Check
  assert d2 == expected_example_reasonable_json_to_d2
