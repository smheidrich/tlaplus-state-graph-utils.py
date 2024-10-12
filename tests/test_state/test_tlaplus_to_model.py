from textwrap import dedent

from tlaplus_dot_utils.state.model import (
  FunctionMerge,
  Record,
  RecordField,
  SimpleValue,
  SingleElemDomainFunction,
)
from tlaplus_dot_utils.state.tlaplus_to_model import (
  tlaplus_state_to_dataclasses,
)


def test_mixed() -> None:
  # Setup
  state_as_tlaplus = dedent(
    r"""
    /\ a = "b"
    /\ c = [ d |-> "e", d2 |-> "e2" ]
    /\ f = ( G :> "H" @@ I :> "J" )
    """
  )

  # Run
  parsed = tlaplus_state_to_dataclasses(state_as_tlaplus)

  # Check
  assert parsed == {
    "a": SimpleValue(value='"b"'),
    "c": Record(
      fields=[
        RecordField(
          key="d",
          value='"e"',
        ),
        RecordField(
          key="d2",
          value='"e2"',
        ),
      ],
    ),
    "f": FunctionMerge(
      [
        SingleElemDomainFunction("G", SimpleValue('"H"')),
        SingleElemDomainFunction("I", SimpleValue('"J"')),
      ]
    ),
  }


def test_three_merged_functions() -> None:
  # Setup
  state_as_tlaplus = dedent(
    r"""
    /\ a = ( B :> "C" @@ D :> "E" @@ F :> "G" )
    """
  )

  # Run
  parsed = tlaplus_state_to_dataclasses(state_as_tlaplus)

  # Check
  assert parsed == {
    "a": FunctionMerge(
      [
        SingleElemDomainFunction("B", SimpleValue('"C"')),
        SingleElemDomainFunction("D", SimpleValue('"E"')),
        SingleElemDomainFunction("F", SimpleValue('"G"')),
      ]
    )
  }
