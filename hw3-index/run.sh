#!/bin/sh

SCRIPT=query.py

if [[ "$1" != "VarByte" ]] && [[ "$1" != "Simple9" ]]; then
    echo "Please specify one of encodings: VarByte or Simple9"
    exit
fi

python ${SCRIPT} "$1"
