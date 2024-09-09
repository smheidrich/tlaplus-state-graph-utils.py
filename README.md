# tlaplus-dot-utils.py

Python utilities for transforming GraphViz dot files produced by TLA+

## Installing and running the CLI

The easiest way to install the CLI into an automatically-created venv (so it's
isolated from your global or user Python libs) is using a tool like
[pipx](https://pipx.pypa.io/), e.g.:

```bash
pipx install https://github.com/smheidrich/tlaplus-dot-utils.py.git
```

You should then be able to run `tlaplus-dot-utils.py` from anywhere.

## CLI commands

The CLI bundles multiple separate functionalities as different subcommands.

### dot-json-to-reasonable-json

This is mainly a workaround for TLA+ being as yet unable to output its state
graph in some kind of JSON format - see
[TLA+ GitHub issue #639](https://github.com/tlaplus/tlaplus/issues/639).

What we do instead is parse output produced by GraphViz dot in JSON-output
mode (`dot -Tjson`), as was suggested in
[a comment](https://github.com/tlaplus/tlaplus/issues/639#issuecomment-1003163720)
on the aforementioned issue, and transform it into another JSON representation
that is easier to work with than the GraphViz-specific one.

Usage is normally going to look something like this:

```bash
# In your TLA+ Model directory:
dot -Tjson Model_1.json | tlaplus-dot-utils.py dot-json-to-reasonable-json
```

This writes compact JSON to standard output. Refer to the `--help` text for
other options.

The JSON's structure looks like this:

```json
{
  "metadata": {
    "format": {
      "name": "reasonable-tlaplus-state-graph-json",
      "version": "0.1"
    }
  },
  "states": [
    {
      "id": 1,
      "labelTlaPlus": "/\\ a = 1 /\\ b = 2 \n ..."
    },
    ...
  ],
  "steps": [
    {
      "id": 0,
      "actionName": "CheckFileExists",
      "fromStateId": 1,
      "toStateId": 2,
      "colorId": "1"
    },
    ...
  ]
}
```

### reasonable-json-to-d2

This needs the `d2` extra to be installed. Refer to the documentation of the
relevant package installer (e.g. `pipx` or `pip`) for how to install extras.

This transforms the "reasonable" JSON format output by the previous script
into a [D2](https://d2lang.com/) graph with LaTeX formatting for the TLA+
states, which might look a bit nicer than the regular ASCII representation in
TLA+'s native state graph.

Most commonly, this will have the output of the previous script piped into it
like this:

```bash
# In your TLA+ Model directory:
dot -Tjson Model_1.json \
| tlaplus-dot-utils.py dot-json-to-reasonable-json \
| tlaplus-dot-utils.py reasonable-json-to-d2
```

As before, this writes to standard output and you can refer to the `--help`
text for other options.

You can pipe this output into `d2` in turn to render the graph.
I recommend using the Elk layout engine rather than the default (Dagre) for
optimal results:

```bash
# In your TLA+ Model directory:
dot -Tjson Model_1.json \
| tlaplus-dot-utils.py dot-json-to-reasonable-json \
| tlaplus-dot-utils.py reasonable-json-to-d2 \
| D2_LAYOUT=elk d2 - > Model_1.svg
```

This writes the rendered graph into an SVG file named `Model_1.svg`.

Here is an example of what a rendered graph looks like:

![Example TLA+ state graph rendered with D2](https://github.com/user-attachments/assets/21b5406f-408b-4cd5-9370-fbcb66c032be)
