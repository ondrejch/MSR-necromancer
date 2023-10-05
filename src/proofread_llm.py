#!/usr/bin/env python3
#
# Module that uses Karen-the-Editor LLM for proofreading
#
# Ondrej Chvala, ochvala@utexas.edu
# 2023-10-05
# MIT
import os

from llama_cpp import Llama

llm = Llama(model_path=os.path.expanduser('~//models/Karen-The-Editor.gguf.q5_K_M.bin))




# This executes if someone runs this module directly
if __name__ == '__main__':
    print("This is a MSR cleaning module.")
 #   input("Press Ctrl+C to quit, or enter else to test it. ")
