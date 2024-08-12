#!/bin/bash
#
# This scripts creates new Python virtual environment and installs all the modules
# needed for MSR Necromancer.
#
# By default it uses Python v. 3.11. To install this in Ubuntu 22.04, use
# $ sudo apt install python3.11-full
#
# To install CUDA 12.5 in Ubuntu 22.04, use
# $ sudo apt install cuda-12-5
#
# Ondrej Chvala <ochvala@utexas.edu>
# MIT license

# Set your environment here
NVCC=/usr/local/cuda/bin/nvcc
PYTHON=python3.12
VENV_DIR=$HOME/.local/necromancer

# Create virtual environment
$PYTHON -m venv $VENV_DIR

# Activate virtual environment
source $VENV_DIR/bin/activate

# Update pip in the virtual environment
python -m pip install --upgrade pip

# Install CUDA-enabled llama-cpp-python
CUDACXX=$NVCC CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir

# Install llama-index modules
pip install llama-index
pip install llama-index-llms-llama-cpp
pip install llama-index-embeddings-huggingface

# I like ipython, but this is optional
pip install IPython
