# tlaplus-dot-utils.py

Python scripts for transforming GraphViz dot files produced by TLA+

## How to run these

So far, all scripts in this repository have no dependencies other than a
recent (3.9+) Python version, so you should be able to just download and run
them using a matching Python interpreter.

But if you don't like to have scripts lying around on your system, you can also
use a tool like e.g. [pipx](https://pipx.pypa.io/) or
[fades](https://github.com/PyAr/) to run them without needing to download them
manually. Refer to the relevant documentation of these tools.


## tlaplus-dot-json-to-reasonable-json.py

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
dot -Tjson Model_1.json | tlaplus-dot-json-to-reasonable-json.py
```

This writes compact JSON to standard output. Refer to the `--help` text for
other options.


## tlaplus-dot-reasonable-json-to-d2.py

This transforms the "reasonable" JSON format outputted by the previous script
into a [D2](https://d2lang.com/) graph with LaTeX formatting for the TLA+
states, which might look a bit nicer than the regular ASCII representation in
TLA+'s native state graph.

Most commonly, this will have the output of the previous script piped into it
like this:

```bash
# In your TLA+ Model directory:
dot -Tjson Model_1.json \
| tlaplus-dot-json-to-reasonable-json.py \
| tlaplus-dot-reasonable-json-to-d2.py
```

As before, this writes compact JSON to standard output and you can refer to the
`--help` text for other options.

You can pipe this output into `d2` in turn to render the graph.
I recommend using the Elk layout engine rather than the default (Dagre) for
optimal results:

```bash
# In your TLA+ Model directory:
dot -Tjson Model_1.json \
| tlaplus-dot-json-to-reasonable-json.py \
| tlaplus-dot-reasonable-json-to-d2.py
| D2_LAYOUT=elk d2 - > Model_1.svg
```

This writes the rendered graph into an SVG file named `Model_1.svg`.

Here is an example of what a rendered graph looks like:

![Example TLA+ state graph rendered with D2](https://github.com/user-attachments/assets/21b5406f-408b-4cd5-9370-fbcb66c032be)
