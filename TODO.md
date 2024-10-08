# TODO

## Next


## Soon

[ ] Allow users to define conditional styling based on predicates on the states
    (distinguish "happy path", highlight "errors" etc.)
[ ] ^ Better idea: If the state is completely represented as JSON, users can
    make simple modifications based on predicates themselves using `jq`
    (relevant parts of its syntax: assignment-update operator `|=` and
    conditionals/if-then-else-end); not as powerful and convenient as
    predicates themselves written in TLA+, but oh well.
[ ] ^ Requirement 1: Allow outputting JSON-ified state in reasonable JSON (CLI
    flag)
[ ] ^ Requirement 2: Allow some basic/universal styling options (classes?) in
    reasonable JSON
[ ] Document jq approach in README

## Later

[ ] Make tests cover 100% of CLI, but with everything behind the CLI mocked
[ ] ... and/or just move more stuff out of CLI into core and add tests for that
[ ] Think about how to allow custom D2 global styles (maybe just D2 includes
    or `(cat output.d2 && cat custom.d2)` and no further action needed?)
[ ] Switch to a reasonable CLI library once one exists. argparse pain points:
    - No way for `choices` to be an enum
    - No way for `choices` to be reasonably formatted in help, or more
      generally to have exceptions from auto-formatting/wrapping
    - No way to specify default subcommand
[ ] Clean up container rendering stuff (separate modules, refactor more)
[ ] 'rg TODO' and resolve remaining issues

After https://github.com/pypa/packaging.python.org/issues/1605 PR is done
(either in the Packaging Guide or elsewhere) and I know what the actual best
solution for handling missing extras is:

[ ] Replace current "missing d2 extra" handling by this
[ ] Make tree-sitter extra (for state parsing) separate from D2
[ ] Ensure similar human-readable error msg when tree-sitter not installed
