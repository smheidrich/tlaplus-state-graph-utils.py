# TODO

## Next


## Soon

[ ] Make tests pkg structure match src

## Later

[ ] Allow users to define conditional styling based on predicates on the states
    (distinguish "happy path", highlight "errors" etc.)
[ ] Rename `Boxes~` -> `[Nested]Container~` to match CLI opt
[ ] Switch to a reasonable CLI library once one exists. argparse pain points:
    - No way for `choices` to be an enum
    - No way for `choices` to be reasonably formatted in help, or more
      generally to have exceptions from auto-formatting/wrapping
    - No way to specify default subcommand
[ ] Make tests cover 100% of CLI, but with everything behind the CLI mocked
[ ] ... and/or just move more stuff out of CLI into core and add tests for that
[ ] Update README with new commands
[ ] Add examples for every output style to README
[ ] 'rg TODO' and resolve remaining issues

After https://github.com/pypa/packaging.python.org/issues/1605 PR is done
(either in the Packaging Guide or elsewhere) and I know what the actual best
solution for handling missing extras is:

[ ] Replace current "missing d2 extra" handling by this
[ ] Make tree-sitter extra (for state parsing) separate from D2
[ ] Ensure similar human-readable error msg when tree-sitter not installed
