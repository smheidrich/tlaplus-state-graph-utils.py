#!/bin/bash
scriptdir="$(dirname "$0")"
dot -Tjson | "$scriptdir"/tladotjson-to-d2.py
