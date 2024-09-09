from . import dot_json_to_reasonable_json, reasonable_json_to_d2
from .root import arg_parser


def run_cli() -> None:
  args = arg_parser.parse_args()

  args.func(args)

def main() -> None:
  run_cli()

__all__ = ["dot_json_to_reasonable_json", "reasonable_json_to_d2"]
