#!/usr/bin/env python3
# PEP 723 metadata:
# /// script
# requires-python = ">=3.9,<4"
# ///
from argparse import FileType
from typing import Any

from ..reasonable_json_to_d2 import parse_and_write_d2
from .root import subparsers

__version__ = "0.1.0"


arg_parser = subparsers.add_parser(
  name="reasonable-json-to-d2",
  description='convert "reasonable TLA+ state graph dot file JSON" '
  "(cf. other script) to D2 (https://d2lang.com/)",
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
  "--version", action="version", version=f"%(prog)s {__version__}"
)


def run_for_cli_args(args: Any) -> None:
  parse_and_write_d2(args.input, args.output)


arg_parser.set_defaults(func=run_for_cli_args)


def run_cli() -> None:
  args = arg_parser.parse_args()
  run_for_cli_args(args)


def main() -> None:
  run_cli()


if __name__ == "__main__":
  main()
