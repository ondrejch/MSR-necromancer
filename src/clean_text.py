#!/usr/bin/env python3
#
# Module that handles molten salt properties for neutronic simulations
#
# Ondrej Chvala, ochvala@utexas.edu
# 2023-10-05
# MIT

import re
import os

EN_US_WORDS = '/usr/share/dict/american-english'  # Words dictionary


def capital_letters(line) -> bool:
    """Is the line mostly capital letters?"""
    uppercase_count = sum(1 for char in line if char.isupper())
    lowercase_count = sum(1 for char in line if char.islower())

    # Check if the line should be kept
    if float(uppercase_count) > float(lowercase_count):
        return True  # Drop line
    return False  # Keep line


class PreCleanText(object):
    """Takes OCRd text and returns pre-cleaned text using algorithmic rules"""

    def __init__(self, d_in: str = None, d_out: str = None):
        """Constructor, sets input and output directories. Other constants can be set after initialization. """
        if d_in == d_out:
            raise ValueError("Input and output directories must differ")
        if not os.path.isdir(d_in):
            raise ValueError("Input dir does not exist: ", d_in)
        if not os.path.isdir(d_out):
            raise ValueError("OOutput dir does not exist: ", d_out)

        self.dir_in: str = d_in  # Input directory
        self.dir_out: str = d_out  # Output dir
        self.is_remove_special_chars: bool = True  # Remove spacial characters?
        self.is_remove_capitalized_lines: bool = True  # Remove capitalized lines?
        self.is_print_rejects: bool = True  # Print rejects to stdout
        self.max_length_line: int = 5  # Maximum characters per line to keep the line
        self.record_separator: str = '\n#-------------------------------#\n'
        self.remove_strings = ['NUCLEAR APPLICATIONS & TECHNOLOGY', '"', "'", ';', '\\*', '\\?', '”', '’', '‘', '®', '|']

        self.text_in = ""
        self.long_paragraphs = []

    def print_reject(self, line):
        if self.is_print_rejects:
            print("Reject: ", line)

    def clean_file(self, file_name):
        """Runs methods to clean an input file"""
        self.text_in = ""
        self.long_paragraphs = []

        with open(self.dir_in + "/" + file_name) as fin:
            self.text_in = fin.read()
        self.clean()
        self.write_out(file_name)

    def clean(self):
        """Runs all teh algorithmic cleanup"""
        self.text_in = self.text_in.replace('-\n', '')  # Join lines with split words
        self.text_in = re.sub(r'\ +\n', '\n', self.text_in)  # Strip spaces at the end of a line
        self.text_in = re.sub(r'\n\ +', '\n', self.text_in)  # Strip spaces at the beginning of a line

        for rs in self.remove_strings:
            self.text_in = re.sub(rs, '', self.text_in)
        self.text_in = re.sub(r'VOL. \d+', '', self.text_in)  # Remove Fig references
        self.text_in = re.sub(r'Fig\. \d+', '', self.text_in)  # Remove Fig references
        self.text_in = re.sub(r'Tab\. \d+', '', self.text_in)  # Remove Tab references

        # if self.is_remove_special_chars:                 # Remove non-ASCII characters
        #     self.text_in = re.sub(r"[^a-zA-Z0-9 ]", "", self.text_in)

        text_in_lower = self.text_in.lower()  # Lowercase text

        # Remove header and references
        pos_from = max(text_in_lower.find('\nabstract'), text_in_lower.find('\nintroduction'))
        pos_to = min(text_in_lower.find('\nreferences'), text_in_lower.find('\nacknowledgments'), len(text_in_lower))
        self.text_in = self.text_in[pos_from: pos_to]
        text_in_lower = text_in_lower[pos_from: pos_to]

        # Join paragraphs
        paragraphs = []
        current_paragraph = []
        for line in self.text_in.splitlines():
            if len(line) > 1 and not re.search(r'[a-zA-Z]', line):  # Skip lines with no words
                self.print_reject(line)
                continue
            if self.is_remove_capitalized_lines and capital_letters(line):  # Skip capitalized lines
                self.print_reject(line)
                continue
            if line.strip():  # Non-empty line
                current_paragraph.append(line.strip())
            elif current_paragraph:  # Empty line and current_paragraph is not empty
                paragraphs.append('\n'.join(current_paragraph))
                current_paragraph = []
        if current_paragraph:  # Append the last paragraph if there's content
            paragraphs.append('\n'.join(current_paragraph))

        # Find duplicate lines
        repeating_lines = set()
        seen = set()
        for line in paragraphs:
            if line in seen and line not in repeating_lines:
                repeating_lines.add(line)
            else:
                if len(line) > 3:
                    seen.add(line)

        # Remove duplicate lines
        for line in paragraphs:
            if line in repeating_lines:
                paragraphs.remove(line)

        # Remove paragraphs with very short lines
        for i, par in enumerate(paragraphs):
            n_lines = 0
            tot_len = 0
            avg_len = 0.0
            for line in par.splitlines():
                n_lines += 1
                tot_len += len(line)
                avg_len = float(tot_len) / float(n_lines)
            #    if 20 <= float(tot_len) / float(n_lines) <25:
            #        print(f'#-------------\n{par}')
            paragraphs[i] = par + "\n--->" + str(float(tot_len) / n_lines)
            if avg_len > self.max_length_line:
                self.long_paragraphs.append(par)

    def write_out(self, f_out):
        """ Dump output"""
        outfile = self.dir_out + "/" + f_out
        with open(outfile, 'w') as outfile:
            outfile.write(self.record_separator.join(line for line in self.long_paragraphs))


# This executes if someone runs this module directly
if __name__ == '__main__':
    print("This is a MSR cleaning module.")
 #   input("Press Ctrl+C to quit, or enter else to test it. ")

    i_dir = '/home/o/git/msr-archive/ocr/'
    o_dir = os.getcwd()
    my_file = 'NAT_MSRchemistry.txt'

    precl = PreCleanText(i_dir, o_dir)
    precl.is_print_rejects = True
    precl.clean_file(my_file)
