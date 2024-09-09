from argparse import ArgumentParser

arg_parser = ArgumentParser(
  description="utilities for transforming TLA+-produced GraphViz dot files"
)

subparsers = arg_parser.add_subparsers(help="sub-command help")
