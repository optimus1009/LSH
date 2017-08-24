#!/bin/bash
sed 's/[^[:print:]]//g' $1 \
| sed 's/[0-9a-zA-Z+=\./:\"<>|_&#]/ /g' \
| sed 's/  */ /g' > $2
# sed '/^ *$/d' > $2