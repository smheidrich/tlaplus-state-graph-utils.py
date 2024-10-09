from typing import Any

from tlaplus_dot_utils.graph.dot_json_to_reasonable_json import (
  dot_jsonish_to_reasonable_jsonish,
)


def test_example_against_reference(
  long_example_dot_json: dict[str, Any],
  long_example_reasonable_json: dict[str, Any],
) -> None:
  # Run
  reasonable = dot_jsonish_to_reasonable_jsonish(long_example_dot_json, False)

  # Uncomment to regenerate, then run jq over the result:
  # from pathlib import Path
  # import json
  # Path("tests/data/long-example/reasonable.json").write_text(
  # json.dumps(reasonable, indent=2)
  # )

  # Check
  assert reasonable == long_example_reasonable_json


def test_example_against_reference_structured_state(
  long_example_dot_json: dict[str, Any],
  long_example_reasonable_json_structured_state: dict[str, Any],
) -> None:
  # Run
  reasonable = dot_jsonish_to_reasonable_jsonish(long_example_dot_json, True)

  # Uncomment to regenerate, then run jq over the result:
  # from pathlib import Path
  # import json
  # Path("tests/data/long-example/reasonable-structured-state.json").write_text(
  # json.dumps(reasonable, indent=2)
  # )

  # Check
  assert reasonable == long_example_reasonable_json_structured_state
