# tlaplus-dot-utils.py

Python utilities for transforming GraphViz dot files produced by TLA+

## Installation

```bash
pip install https://github.com/smheidrich/tlaplus-dot-utils.py.git
```

## Using the CLI

Installing the package puts a CLI program named `tlaplus-dot-utils.py` in your
`PATH`. Here is its `--help` text:

```
usage: tlaplus-dot-utils.py [-h] [--version] COMMAND ...

utilities for transforming TLA+-produced GraphViz dot files

options:
  -h, --help  show this help message and exit
  --version   show program's version number and exit

subcommands:
  COMMAND     description
    convert   convert between state graph formats
```

It currently has only one subcommand called `convert` which can be used to
convert between different representations of TLA+ state graphs. Here is its
`--help` text:

```
usage: tlaplus-dot-utils.py convert [-h] [--output OUTPUT]
                                    [--from {reasonable-json,tlaplus-dot-json}]
                                    [--to {reasonable-json,d2}] [--pretty]
                                    [--d2-output-state-as D2_OUTPUT_STATE_AS]
                                    [input]

convert between TLA+ state graph formats/representations

positional arguments:
  input                 input file path or '-' to use stdin (the default)

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        output file path or '-' to use stdout (the default)
  --from {reasonable-json,tlaplus-dot-json}, -f {reasonable-json,tlaplus-dot-json}
                        input format (guessed from extension & content if not
                        given)
  --to {reasonable-json,d2}, -t {reasonable-json,d2}
                        output format (if not given, defaults to reasonable-
                        json when outputting to stdout, otherwise guessed from
                        extension)
  --pretty              produce pretty-printed rather than compact output

D2 options:
  options relevant when outputting in D2 format

  --d2-output-state-as D2_OUTPUT_STATE_AS
                        how to represent individual states in the D2 output:
                        label: without modification as a D2 node label; latex:
                        as a LaTeX equation which D2 will render; nested-
                        containers: as nested containers, one per variable,
                        record, etc.; nested-containers-simple-values-inline:
                        as above but with terminal/simple values not getting
                        their own container; nested-containers-simple-values-
                        inline-newline: as above but with keys and terminal
                        values separated by newlines
```

For instance, this converts a GraphViz dot file produced by TLA+'s state
diagram output into a "reasonable" JSON format that's easier to work with:

```bash
# In your TLA+ Model directory:
dot -Tjson Model_1.dot | tlaplus-dot-utils.py convert -t reasonable-json
```

The following sections go into more details about the supported input and
output formats.

### Input formats

#### dot JSON

TLA+ does not currently have a "canonical" format for state graphs (see
[TLA+ GitHub issue #639](https://github.com/tlaplus/tlaplus/issues/639)) and
so the only halfway convenient way to get this information out of TLA+ is to
process the GraphViz `dot` files it produces.

In particular, as suggested in
[a comment](https://github.com/tlaplus/tlaplus/issues/639#issuecomment-1003163720)
on the aforementioned issue, `dot` itself can convert these into a JSON
representation (`dot -Tjson`), which can then by read in by this utility (it
automatically considers filenames ending in `.dot.json` to be such files).

#### Reasonable JSON

Another possible input format is the "reasonable JSON" format produced by this
tool itself - it is explained in more detail in the *Output formats* section
below.

### Output formats

#### "Reasonable JSON"

The aforementioned "reasonable JSON" format is meant to make it easier for
other tools to work with TLA+ state graphs. It looks like this:

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

#### D2

Another supported output format is [D2](https://d2lang.com/), but to use it,
the package's `d2` extra needs to be installed:

```bash
pip install 'https://github.com/smheidrich/tlaplus-dot-utils.py.git[d2]'
```

There are many different ways to represent the *contents* of each state (i.e.
the set of variables and their values) in D2, which can be configured via
the `--d2-output-state-as` option.

Here is an example showing how to go from a `dot` file produced by TLA+ to
a graph rendered using D2 in one shell command:

```bash
# In your TLA+ Model directory:
dot -Tjson Model_1.dot \
| tlaplus-dot-utils.py convert -t d2 \
| D2_LAYOUT=elk d2 - > Model_1.svg
```

This writes the rendered graph into an SVG file named `Model_1.svg`.

Here is an example of what a rendered graph looks like:

![Example TLA+ state graph rendered with D2](https://github.com/user-attachments/assets/21b5406f-408b-4cd5-9370-fbcb66c032be)


## Use as a library

I'm too lazy to write this or set up automated API docs, especially considering
nobody is going to use it.
If you want to use this as a library, please just open an issue saying so and
I'll get started (and maybe clean things up a little).
