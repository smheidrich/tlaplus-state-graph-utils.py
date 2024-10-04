import json
from io import StringIO
from typing import IO, Any

from ..format_determination import GraphFormat, guess_graph_file_format
from .dot_json_to_model import dot_jsonish_to_model
from .model import TransitionDiagram
from .reasonable_json_to_model import parse_from_reasonable_json_file


def any_file_to_model(file: IO[Any]) -> TransitionDiagram:
  input_format = guess_graph_file_format(file)
  match input_format:
    case GraphFormat.tlaplus_dot_json:
      d = json.load(file)
      return dot_jsonish_to_model(d)
    case GraphFormat.reasonable_json:
      return parse_from_reasonable_json_file(file)
    case _:
      # TODO Refactor w/r/t to ^ after done unifying these functions'
      #   interfaces
      # Fall back to guessing based on content, which we do by just trying one
      # option after another:
      file = StringIO(file.read())  # TODO: Replace w/ seekable wrapper (lib?)
      start_pos = file.tell()  # remember current position for rewinding
      try:
        d = json.load(file)
        return dot_jsonish_to_model(d)
      except Exception:
        file.seek(start_pos)  # rewind & move on
      try:
        return parse_from_reasonable_json_file(file)
      except Exception:
        file.seek(start_pos)  # rewind & move on
      # We've exhausted all options, so give up:
      raise ValueError(
        f"Could not determine format of input file {file} from either name or contents - giving up."
      )
