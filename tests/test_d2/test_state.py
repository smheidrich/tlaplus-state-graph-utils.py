from textwrap import dedent

from tlaplus_dot_utils.state.model_to_d2 import (
  BoxesSimpleValuesInlineStateToD2Renderer,
  BoxesStateToD2Renderer,
)
from tlaplus_dot_utils.state.tlaplus_to_model import (
  tlaplus_state_to_dataclasses,
)


def test_state_as_d2() -> None:
  # Setup
  state_as_tlaplus = dedent(
    r"""
    /\ a = "b"
    /\ c = [ d |-> "e", d2 |-> "e2" ]
    /\ f = ( G :> "H" @@ I :> "J" )
    """
  )
  renderer = BoxesStateToD2Renderer()

  # Run
  d2 = renderer(tlaplus_state_to_dataclasses(state_as_tlaplus))

  # Check
  print(d2)
  assert d2 == dedent(
    """\
    var0: "a" {
      value: '"b"'
    }
    var1: "c" {
      var0: "d |->" {
        value: '"e"'
      }
      var1: "d2 |->" {
        value: '"e2"'
      }
    }
    var2: "f" {
      var0: "G :>" {
        value: '"H"'
      }
      var1: "I :>" {
        value: '"J"'
      }
    }"""
  )


def test_state_as_d2_simple_values_inline() -> None:
  # Setup
  state_as_tlaplus = dedent(
    r"""
    /\ a = "b"
    /\ c = [ d |-> "e", d2 |-> "e2" ]
    /\ f = ( G :> "H" @@ I :> "J" )
    """
  )
  renderer = BoxesSimpleValuesInlineStateToD2Renderer()

  # Run
  d2 = renderer(tlaplus_state_to_dataclasses(state_as_tlaplus))

  # Check
  print(d2)
  assert d2 == dedent(
    """\
    var0: "a \\"b\\""
    var1: "c" {
      var0: "d |-> \\"e\\""
      var1: "d2 |-> \\"e2\\""
    }
    var2: "f" {
      var0: "G :> \\"H\\""
      var1: "I :> \\"J\\""
    }"""
  )
