from textwrap import dedent

from tlaplus_dot_utils.state_parsing import (
  FunctionMerge,
  Record,
  RecordField,
  SimpleValue,
  SingleElemDomainFunction,
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
    b"a": SimpleValue(value=b'"b"'),
    b"c": Record(
      fields=[
        RecordField(
          key=b"d",
          value=b'"e"',
        ),
        RecordField(
          key=b"d2",
          value=b'"e2"',
        ),
      ],
    ),
    b"f": FunctionMerge(
      [
        SingleElemDomainFunction(b"G", SimpleValue(b'"H"')),
        SingleElemDomainFunction(b"I", SimpleValue(b'"J"')),
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
    b"a": FunctionMerge(
      [
        SingleElemDomainFunction(b"B", SimpleValue(b'"C"')),
        SingleElemDomainFunction(b"D", SimpleValue(b'"E"')),
        SingleElemDomainFunction(b"F", SimpleValue(b'"G"')),
      ]
    )
  }
