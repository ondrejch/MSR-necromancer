#!/usr/bin/env python3
#
# Module that handles runs pre-cleaning of OCR'd texts
#
# Ondrej Chvala, ochvala@utexas.edu
# 2023-10-06
# MIT

from clean_text import PreCleanText
import os


i_dir = '/home/MSR-LLM/msr-archive/ocr/'
o_dir = '/home/MSR-LLM/pre-cleaned/'
precl = PreCleanText(i_dir, o_dir)
precl.is_print_rejects = False

file_list = [f for f in os.listdir(i_dir) if f.endswith('.txt')]

for my_file in file_list:
	print("Processing ", my_file)
	precl.clean_file(my_file)

print("All done!")
