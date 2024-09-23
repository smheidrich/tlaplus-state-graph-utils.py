from ..graph.model import State


# TODO This shouldn't have a dependency on graph.model.State, just take a str
def state_label_to_latex(state: State) -> str:
  # TODO Surely there is a way to use TLA+'s own LaTeX-output
  #  programmatically somehow so we don't have to do this?
  return (
    state.label_tlaplus.replace("/\\", "\\land")
    .replace(r"\/", "\\lor")
    .replace("|->", "\\mapsto")
    .replace("\n", " \\\\ ")
    .replace("FALSE", "\\mathrm{FALSE}")
    .replace("TRUE", "\\mathrm{TRUE}")
    .replace('"', '\\text{"}')  # these look like garbage otherwise
  )
