#!/bin/bash

if [[ $1 == "clean"  ]]; then
    rm -r venv wh-service.egg-info
    rm activate
    exit 0
fi

virtualenv venv

ln -sf venv/bin/activate .
source activate
pip install bottle PyDictionary pymongo newspaper


# python setup.py develop
