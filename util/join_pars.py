#!/bin/env -S python3 -u

import os

def join_paragraphs(text: str) -> str:
    # Split the text into paragraphs based on double newlines
    paragraphs = text.split('\n\n')
    # Process each paragraph to join lines within it
    for i in range(len(paragraphs)):
        # Split the paragraph into lines
        lines = paragraphs[i].splitlines()
        # Join the lines back together with a space in between
        paragraphs[i] = ' '.join(lines)
    # Join paragraphs with double newline to keep them separate
    result = '\n\n'.join(paragraphs)
    return result


def list_txt_files(mydir) -> list:
    mylist = []
    for root, dirs, files in os.walk(mydir):
        for f in files:
#            print(root, dirs, f)
            if f.endswith('.txt'):
#                mylist.append(root + '/' + f)
                mylist.append(f)
    mylist.sort()
    return mylist


in_dir: str = os.getcwd()
out_dir: str = '../12-ANS-W2024_OKpar/'
out_dir: str = in_dir

for my_file in list_txt_files(in_dir):
    print(my_file)
    with open(in_dir + '/' + my_file, 'r') as fin:
        din = fin.read()
    with open(out_dir + '/' + my_file, 'w') as fout:
        fout.write(join_paragraphs(din))

