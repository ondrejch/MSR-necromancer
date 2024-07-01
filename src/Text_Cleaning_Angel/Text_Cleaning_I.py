import os
import re

class TextCleaning:
    def __init__(self, d_in: str = None, d_out: str = None):
        if d_in == d_out:
            raise ValueError("Input and output directories must differ")
        if not os.path.isdir(d_in):
            raise ValueError("Input dir does not exist: ", d_in)
        if not os.path.isdir(d_out):
            raise ValueError("Output dir does not exist: ", d_out)

        self.dir_in = d_in
        self.dir_out = d_out
        self.is_remove_special_chars = True
        self.is_remove_capitalized_lines = True
        self.is_print_rejects = True
        self.max_length_line = 5
        self.record_separator = '\n#-------------------------------#\n'
        self.remove_strings = ['NUCLEAR APPLICATIONS & TECHNOLOGY', '"', "'", ';', '\\*', '\\?', '”', '’', '‘', '®', '|']

        self.text_in = ""
        self.long_paragraphs = []

    @staticmethod
    def capital_letters(line):
        return line.isupper()

    def print_reject(self, line):
        if self.is_print_rejects:
            print("Reject: ", line)

    def clean_file(self, file_name):
        self.text_in = ""
        self.long_paragraphs = []

        with open(os.path.join(self.dir_in, file_name), 'r', encoding='utf-8') as fin:
            self.text_in = fin.read()
        self.clean()
        self.write_out(file_name)

    def clean(self):
        self.text_in = self.text_in.replace('-\n', '')
        self.text_in = re.sub(r'\ +\n', '\n', self.text_in)
        self.text_in = re.sub(r'\n\ +', '\n', self.text_in)

        for rs in self.remove_strings:
            self.text_in = re.sub(rs, '', self.text_in)
        self.text_in = re.sub(r'VOL. \d+', '', self.text_in)
        self.text_in = re.sub(r'Fig\. \d+', '', self.text_in)
        self.text_in = re.sub(r'Tab\. \d+', '', self.text_in)

        text_in_lower = self.text_in.lower()

        paragraphs = []
        current_paragraph = []
        for line in self.text_in.splitlines():
            if len(line) > 1 and not re.search(r'[a-zA-Z]', line):
                self.print_reject(line)
                continue
            if self.is_remove_capitalized_lines and TextCleaning.capital_letters(line):
                self.print_reject(line)
                continue
            if line.strip():
                current_paragraph.append(line.strip())
            elif current_paragraph:
                paragraphs.append('\n'.join(current_paragraph))
                current_paragraph = []
        if current_paragraph:
            paragraphs.append('\n'.join(current_paragraph))

        repeating_lines = set()
        seen = set()
        for line in paragraphs:
            if line in seen and line not in repeating_lines:
                repeating_lines.add(line)
            else:
                if len(line) > 3:
                    seen.add(line)

        for line in paragraphs:
            if line in repeating_lines:
                paragraphs.remove(line)

        for i, par in enumerate(paragraphs):
            n_lines = 0
            tot_len = 0
            avg_len = 0.0
            for line in par.splitlines():
                n_lines += 1
                tot_len += len(line)
                avg_len = float(tot_len) / float(n_lines)
            paragraphs[i] = par + "\n--->" + str(float(tot_len) / n_lines)
            if avg_len > self.max_length_line:
                self.long_paragraphs.append(par)



    def write_out(self, file_name):
        """ Dump output to a new file in the output directory with _cleaned appended to the filename"""
        base_name, ext = os.path.splitext(file_name)
        outfile_name = os.path.join(self.dir_out, base_name + "_cleaned" + ext)
        with open(outfile_name, 'w', encoding='utf-8') as outfile:
            outfile.write(self.record_separator.join(line for line in self.long_paragraphs))


# Create an instance of the TextCleaning class with the specified input and output directories
cleaner = TextCleaning(d_in=r"C:\\Users\\angel\\PycharmProjects\\LLM_Project\\Uncleaned_text",
                       d_out=r"C:\\Users\\angel\\PycharmProjects\\LLM_Project\\Chvala_Cleaned")

# Clean a specific file. For this example, let's say you want to clean "FFR_part2.txt"
cleaner.clean_file("FFR_part2.txt")