#!/bin/bash

export LD_LIBRARY_PATH=$HOME/PANkreator/lib/lib/
source $HOME/PANkreator/panvenv/bin/activate
cd $HOME/PANkreator/pbc/
python3 pga.py
