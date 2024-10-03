from typing import IO, Any

from .formats import GraphFormat
from .utils.io import get_file_filename


def guess_graph_file_format(file: IO[Any]) -> GraphFormat:
  filename = get_file_filename(file)
  if filename is None:
    raise NotImplementedError(
      "Guessing file type from contents alone not yet implemented. "
      "Please specify file type explicitly, e.g. by using a named file "
      "with an appropriate extension."
    )
  lower_filename = filename.lower()
  if lower_filename.endswith(".dot.json"):
    return GraphFormat.tlaplus_dot_json
  elif lower_filename.endswith(".reasonable.json"):
    return GraphFormat.reasonable_json
  elif lower_filename.endswith(".d2"):
    return GraphFormat.d2
  else:
    # TODO Raise more specific exc. & catch/transform in CLI
    raise ValueError(
      f"Could not determine type of file {filename!r} based on its name. "
      "Make sure it's in a supported format."
    )


__all__ = ["guess_graph_file_format", "GraphFormat"]
