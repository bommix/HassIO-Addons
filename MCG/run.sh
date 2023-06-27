#!/bin/sh
set -e

# Die Variable aus der Konfigurationsdatei lesen
VARIABLE=$(jq --raw-output '.variable' options.json)

# Das MCG.py-Programm mit der Variable starten
python3 -u MCG.py "$VARIABLE"