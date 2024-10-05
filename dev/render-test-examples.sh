#!/bin/bash
for x in tests/data/long-example/*.d2; do
  D2_LAYOUT=elk d2 \
    --elk-padding '[top=10,left=10,bottom=10,right=10]' \
    --elk-edgeNodeBetweenLayers 20 \
    --elk-nodeNodeBetweenLayers 20 \
    "$x"
done
