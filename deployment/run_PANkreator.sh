#!/bin/bash

source $HOME/PANkreator/panvenv/bin/activate
export LD_LIBRARY_PATH=$HOME/PANkreator/lib/lib/
cd $HOME/PANkreator/pbc/
python3 pga.py
