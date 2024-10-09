import importlib.resources
import json
from importlib.resources.abc import Traversable
from typing import Any

import pytest

from tlaplus_dot_utils.graph.dot_json_to_model import dot_jsonish_to_model
from tlaplus_dot_utils.graph.model import TransitionDiagram


@pytest.fixture
def data_files() -> Traversable:
  return importlib.resources.files("tests.data")


@pytest.fixture
def long_example_dot_json_traversable(data_files: Traversable) -> Traversable:
  return data_files / "long-example/dot.json"


@pytest.fixture
def long_example_dot_json(
  long_example_dot_json_traversable: Traversable,
) -> dict[str, Any]:
  with long_example_dot_json_traversable.open() as f:
    return json.load(f)  # type: ignore[no-any-return]


@pytest.fixture
def long_example_model(
  long_example_dot_json: dict[str, Any],
) -> TransitionDiagram:
  return dot_jsonish_to_model(long_example_dot_json)


@pytest.fixture
def long_example_reasonable_json_traversable(
  data_files: Traversable,
) -> Traversable:
  return data_files / "long-example/reasonable.json"


@pytest.fixture
def long_example_reasonable_json(
  long_example_reasonable_json_traversable: Traversable,
) -> dict[str, Any]:
  with long_example_reasonable_json_traversable.open() as f:
    return json.load(f)  # type: ignore[no-any-return]


@pytest.fixture
def long_example_reasonable_json_structured_state_traversable(
  data_files: Traversable,
) -> Traversable:
  return data_files / "long-example/reasonable-structured-state.json"


@pytest.fixture
def long_example_reasonable_json_structured_state(
  long_example_reasonable_json_structured_state_traversable: Traversable,
) -> dict[str, Any]:
  with long_example_reasonable_json_structured_state_traversable.open() as f:
    return json.load(f)  # type: ignore[no-any-return]


@pytest.fixture
def long_example_d2_containers_simple_values_inline_traversable(
  data_files: Traversable,
) -> Traversable:
  return data_files / "long-example/containers-simple-values-inline.d2"


@pytest.fixture
def long_example_d2_containers_simple_values_inline(
  long_example_d2_containers_simple_values_inline_traversable: Traversable,
) -> str:
  return (
    long_example_d2_containers_simple_values_inline_traversable.read_text()
  )


@pytest.fixture
def long_example_d2_containers_simple_values_inline_newline(
  data_files: Traversable,
) -> str:
  return (
    data_files / "long-example/containers-simple-values-inline-newline.d2"
  ).read_text()


@pytest.fixture
def long_example_d2_containers_simple_values_not_inline(
  data_files: Traversable,
) -> str:
  return (
    data_files / "long-example/containers-simple-values-not-inline.d2"
  ).read_text()


@pytest.fixture
def long_example_d2_latex(data_files: Traversable) -> str:
  return (data_files / "long-example/latex.d2").read_text()


@pytest.fixture
def long_example_d2_non_latex(data_files: Traversable) -> str:
  return (data_files / "long-example/non-latex.d2").read_text()
