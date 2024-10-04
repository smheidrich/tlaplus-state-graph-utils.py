# TODO

## Next


## Soon

[ ] Translate unknown file format exceptions into readable CLI errors
[ ] Ensure human-readable error msg when py_d2 (via d2 extra) not installed
[ ] 'rg TODO' and resolve remaining issues
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
