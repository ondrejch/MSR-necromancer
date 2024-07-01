#!/bin/bash

# This scripts creates new Python virtual environment and installs all the modules
# needed for MSR Necromancer
#
# Ondrej Chvala <ochvala@utexas.edu>
# MIT licensse

# Set your environemnte heer
PYTHON="python3.11"
VENVDIR="~/.local/necromancer"

# Create virtual environment
$PYTHON -m venv $VENVDIR

# Activate virtual environment
source ~/.local/necromancer/bin/activate

# Install 


