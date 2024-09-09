import json
from typing import Any

import pytest

from tlaplus_dot_utils.dot_json_to_reasonable_json import (
  dot_jsonish_to_reasonable_jsonish,
)


@pytest.fixture
def example_dot_json() -> dict[str, Any]:
  # TODO use pkg_resources or w/e
  with open("tests/data/dot-json-example.json") as f:
    return json.load(f)  # type: ignore[no-any-return]


@pytest.fixture
def expected_example_dot_json_to_reasonable() -> dict[str, Any]:
  # TODO use pkg_resources or w/e
  with open("tests/data/expected-dot-json-example-to-reasonable.json") as f:
    return json.load(f)  # type: ignore[no-any-return]


def test_example_against_reference(
  example_dot_json: dict[str, Any],
  expected_example_dot_json_to_reasonable: dict[str, Any],
) -> None:
  # Run
  reasonable = dot_jsonish_to_reasonable_jsonish(example_dot_json)

  # Uncomment to regenerate:
  # from pathlib import Path
  # Path("tests/data/expected-dot-json-example-to-reasonable.json").write_text(
  # json.dumps(reasonable)
  # )

  # Check
  assert reasonable == expected_example_dot_json_to_reasonable
