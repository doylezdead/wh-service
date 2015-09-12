#!/bin/bash

if [[ $1 == "clean"  ]]; then
    rm -r venv wh-service.egg-info
    rm activate
    exit 0
fi

if [[ `which pyvenv-3.4 | wc -l` > 0 ]]; then
    pyvenv-3.4 venv
else
    pvers=`which python3.4`
    virtualenv -p $pvers venv
fi

ln -sf venv/bin/activate .
source activate
pip install bottle PyDictionary pymongo


# python setup.py develop
