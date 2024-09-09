#!/usr/bin/env python3
# PEP 723 metadata:
# /// script
# requires-python = ">=3.9,<4"
# ///
import json
from argparse import FileType
from typing import Any

from ..dot_json_to_reasonable_json import dot_jsonish_to_reasonable_jsonish
from .root import subparsers

__version__ = "0.1.0"


arg_parser = subparsers.add_parser(
  name="dot-json-to-reasonable-json",
  description='convert JSON produced from TLA+ dot files to "reasonable" '
  "JSON that is easier to work with",
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
  "--pretty",
  action="store_true",
  help="pretty-printed rather than compact JSON",
)
arg_parser.add_argument(
  "--version", action="version", version=f"%(prog)s {__version__}"
)


def run_for_cli_args(args: Any) -> None:
  d = json.load(args.input)
  jsonish = dot_jsonish_to_reasonable_jsonish(d)

  if args.pretty:
    json.dump(jsonish, args.output, indent=2)
  else:
    json.dump(jsonish, args.output)


arg_parser.set_defaults(func=run_for_cli_args)


def run_cli() -> None:
  args = arg_parser.parse_args()
  run_for_cli_args(args)


def main() -> None:
  run_cli()


if __name__ == "__main__":
  main()
