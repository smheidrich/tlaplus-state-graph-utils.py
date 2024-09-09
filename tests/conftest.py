import importlib.resources
import json
from importlib.resources.abc import Traversable
from typing import Any

import pytest


@pytest.fixture
def data_files() -> Traversable:
  return importlib.resources.files("tests.data")


@pytest.fixture
def long_example_dot_json(data_files: Traversable) -> dict[str, Any]:
  with (data_files / "long-example/dot.json").open() as f:
    return json.load(f)  # type: ignore[no-any-return]


@pytest.fixture
def long_example_reasonable_json(data_files: Traversable) -> dict[str, Any]:
  with (data_files / "long-example/reasonable.json").open() as f:
    return json.load(f)  # type: ignore[no-any-return]


@pytest.fixture
def long_example_d2_boxes_simple_values_inline(data_files: Traversable) -> str:
  return (
    data_files / "long-example/boxes-simple-values-inline.d2"
  ).read_text()


@pytest.fixture
def long_example_d2_boxes_simple_values_inline_newline(
  data_files: Traversable,
) -> str:
  return (
    data_files / "long-example/boxes-simple-values-inline-newline.d2"
  ).read_text()


@pytest.fixture
def long_example_d2_boxes_simple_values_not_inline(
  data_files: Traversable,
) -> str:
  return (
    data_files / "long-example/boxes-simple-values-not-inline.d2"
  ).read_text()


@pytest.fixture
def long_example_d2_latex(data_files: Traversable) -> str:
  return (data_files / "long-example/latex.d2").read_text()
