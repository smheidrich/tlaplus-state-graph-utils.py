import json
from argparse import FileType
from typing import Any

from ..format_determination import GraphFormat, guess_graph_file_format
from ..graph.any_to_model import any_file_to_model
from ..graph.dot_json_to_model import dot_jsonish_to_model
from ..graph.model import TransitionDiagram
from ..graph.model_to_d2 import SimpleStateDiagramToD2Renderer
from ..graph.model_to_reasonable_json import model_to_reasonable_jsonish
from ..graph.reasonable_json_to_model import parse_from_reasonable_json_file
from .root import subparsers

arg_parser = subparsers.add_parser(
  name="convert",
  # Short help in subcommands list:
  help="convert between state graph formats",
  # Long help in subcommand's own --help:
  description="convert between TLA+ state graph formats/representations",
)
arg_parser.add_argument(
  "input",
  type=FileType("r"),
  default="-",
  nargs="?",
  help="input file path or '-' to use stdin (the default)",
)
arg_parser.add_argument(
  "--output",
  "-o",
  type=FileType("w"),
  default="-",
  help="output file path or '-' to use stdout (the default)",
)
arg_parser.add_argument(
  "--from",
  "-f",
  type=str,
  default=None,
  choices=["reasonable-json", "tlaplus-dot-json"],
  help="input format (guessed from extension & content if not given)",
  dest="input_format",
)
arg_parser.add_argument(
  "--to",
  "-t",
  type=str,
  default="reasonable-json",
  choices=["reasonable-json", "d2"],
  help="output format (guessed from extension if not given)",
  dest="output_format",
)
arg_parser.add_argument(
  "--pretty",
  action="store_true",
  help="produce pretty-printed rather than compact output",
)


def run_for_cli_args(args: Any) -> None:
  input_format: GraphFormat | None
  match args.input_format:
    case "reasonable-json":
      input_format = GraphFormat.reasonable_json
    case "tlaplus-dot-json":
      input_format = GraphFormat.tlaplus_dot_json
    case _:
      input_format = guess_graph_file_format(args.input)

  match args.output_format:
    case "reasonable-json":
      output_format = GraphFormat.reasonable_json
    case "d2":
      output_format = GraphFormat.d2
    case _:
      guessed_output_format = guess_graph_file_format(args.output)
      if guessed_output_format is None:
        raise ValueError(
          "Could not guess output format. Please specify it explicitly or "
          "ensure your output filename makes it unambiguous."
        )
      output_format = guessed_output_format

  match input_format:
    case GraphFormat.tlaplus_dot_json:
      d = json.load(args.input)
      # TODO Shouldn't have to convert to TransitionDiagram here
      model = TransitionDiagram(*dot_jsonish_to_model(d))
    case GraphFormat.reasonable_json:
      model = parse_from_reasonable_json_file(args.input)
    case None:
      model = any_file_to_model(args.input)
    case _ as other:
      raise NotImplementedError(
        f"Input in format {other} is not currently supported."
      )

  match output_format:
    case GraphFormat.reasonable_json:
      # TODO Shouldn't have to destructure
      jsonish = model_to_reasonable_jsonish(model.states, model.steps)
      if args.pretty:
        json.dump(jsonish, args.output, indent=2)
      else:
        json.dump(jsonish, args.output)
    case GraphFormat.d2:
      # TODO Other renderers depending on CLI opts
      renderer = SimpleStateDiagramToD2Renderer()
      d2_diag = renderer(model)
      args.output.write(str(d2_diag))
    case _ as other:
      raise NotImplementedError(
        f"Output in format {other} is not currently supported."
      )


arg_parser.set_defaults(func=run_for_cli_args)


def run_cli() -> None:
  args = arg_parser.parse_args()
  run_for_cli_args(args)


def main() -> None:
  run_cli()


if __name__ == "__main__":
  main()
