# TODO

## Next

[ ] Add any kind of test for styleClass parsing (reasonable JSON)

## Soon

[ ] Fix bug re: bools in state not being parsed as such
[ ] Fix bug re: single state doesn't get rendered as D2 (empty string instead)
    & use that to simplify D2 styleClass output test

## Later

[ ] Consider using https://github.com/wenkokke/py-tree-sitter-type-provider
    to simplify TLA+ state parsing
[ ] Allow parsing of various structured state formats in reasonable-json
[ ] ^ Use some kind of library, Pydantic or Marshmallow or whatever...
[ ] ^ Error if mismatch between different reprs (TLA+, own structured, ITF)
[ ] Make tests cover 100% of CLI, but with everything behind the CLI mocked
[ ] ... and/or just move more stuff out of CLI into core and add tests for that
[ ] Clean up container rendering stuff (separate modules, refactor more)
[ ] 'rg TODO' and resolve remaining issues
[ ] Option to include D2 preamable? Not really needed b/c
    `(cat preamble.d2 && ...)` does the trick just fine, but might be
    convenient

## Much later

[ ] Switch to a reasonable CLI library once one exists. argparse pain points:
    - No way for `choices` to be an enum
    - No way for `choices` to be reasonably formatted in help, or more
      generally to have exceptions from auto-formatting/wrapping
    - No way to specify default subcommand
[ ] Add built-in support for styleClass conditional on predicates on the states
    (easier-to-use alternative to cookbook approach via `jq`)
    [ ] Alternative: Write completely separate tool reminiscient of `jq` but
        for TLA+ states; but how to add `styleClass` specifically with that?

## Conditional on other developments

After https://github.com/pypa/packaging.python.org/issues/1605 PR is done
(either in the Packaging Guide or elsewhere) and I know what the actual best
solution for handling missing extras is:

[ ] Replace current "missing d2 extra" handling by this
[ ] Make tree-sitter extra (for state parsing) separate from D2
[ ] Ensure similar human-readable error msg when tree-sitter not installed
