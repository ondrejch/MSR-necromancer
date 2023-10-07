#!/usr/bin/env python3
#
# Module that uses Karen-the-Editor LLM for proofreading
#
# Ondrej Chvala, ochvala@utexas.edu
# 2023-10-05
# MIT

import os
from llama_cpp import Llama

DEBUG: int = 3      # How much debugging outputs to print


def preamble() -> str:
    """Preamble for LLM 1st run"""
    return f'Assistant is a meticulous senior editor with a specialization in editing scientific papers. ' \
           f'When given text, Assistant detects and corrects grammatical errors, including subject-verb agreement, ' \
           f'tense consistency, punctuation, capitalization, use of correct articles, ' \
           f'and correct present perfect and past perfect tense.'


def prompt(user_text) -> str:
    """Prompt for LLM"""
    return f'''
USER: Edit the following for spelling and grammar mistakes:

{user_text}

ASSISTANT:'''


class ProofCleanText(object):
    """Polishing text cleanup using Karen-the-Editor LLM"""

    def __init__(self, d_in: str = None, d_out: str = None,
                 model: str = os.path.expanduser('~/models/Karen-The-Editor.Q5_K_M.gguf'),
                 n_gpu_layers: int = 64, n_ctx: int = 2048):
        """Initialize the class and the model
        On machines without a GPU (usha), set n_gpu_layers to 0
        """
        if d_in == d_out:
            raise ValueError("Input and output directories must differ")
        if not os.path.isdir(d_in):
            raise ValueError("Input dir does not exist: ", d_in)
        if not os.path.isdir(d_out):
            raise ValueError("OOutput dir does not exist: ", d_out)
        if not os.path.isfile(model):
            raise ValueError("Model file not found", model)

        self.dir_in: str = d_in  # Input directory
        self.dir_out: str = d_out  # Output dir
        self.llm = Llama(model_path=model, n_gpu_layers=n_gpu_layers, n_ctx=n_ctx)
        self.record_separator: str = '\n#-------------------------------#\n'  # Paragraph separator for input
        self.edited_record_separator: str = '\n#---LLM_EDITED---#\n'  # Paragraph separator for output
        self.records = []  # Internal buffer for input file paragraphs
        self.is_1st_run: bool = True

    def llm_inference(self, text):
        """Return corrected text"""
        my_prompt: str = ''
        if self.is_1st_run:
            my_prompt = preamble() + prompt(text)
            self.is_1st_run = False
        else:
            my_prompt = prompt(text)
        output = self.llm(my_prompt, max_tokens=2048, temperature=0.8, top_p=0.5, echo=False, stop=['#'])
        if DEBUG > 1:
            print(output, flush=True)
        return output["choices"][0]["text"].strip()

    def read_file(self, file_name):
        """Reads a file with separated paragraphs"""
        with open(self.dir_in + "/" + file_name) as fin:
            tmp_records = fin.read().split(self.record_separator)
        self.records = [r.replace("\n", " ").replace("\\s+", " ") for r in tmp_records if len(r) > 0]

    def proces_record(self, idx: int = 0):
        """Process one record though LLM"""
        return self.llm_inference(self.records[idx])

    def process_file(self, file_name):
        """Process all records in the file"""
        self.read_file(file_name)
        outfile_name = self.dir_out + "/" + file_name
        outfile = open(outfile_name, 'w')
        for my_rec in self.records:
            edited_record = self.llm_inference(my_rec)
            outfile.write(edited_record + self.edited_record_separator)
            outfile.flush()
        outfile.close()


# This executes if someone runs this module directly
if __name__ == '__main__':
    print("This is a MSR cleaning module.")
    input("Press Ctrl+C to quit, or enter else to test it. ")

    i_dir = os.getcwd()
    o_dir = os.path.expanduser('~/tmp/')
    my_file = 'MSadventure.txt'

    keditor = ProofCleanText(i_dir, o_dir)
    keditor.process_file(my_file)

""" # ---  PLAYGROUND  --- #

import os
from llama_cpp import Llama
llm = Llama(model_path =os.path.expanduser('~/models/Karen-The-Editor.gguf.q5_K_M.bin'))
user_text = 'Chemical separations, of which reductive extraction appears most attractive, for removing uranium and protactinium from the fuel salt and from each other have been demonstrated in small scale laboratory equipment. Separations of lanthanides from the fuel are markedly more difficult, but reductive extraction of these elements into molten bismuth appears possible.'

prompt = f'''Assistant is a meticulous senior editor with a specialization in editing fictional stories. When given text, Assistant detects and corrects grammatical errors, including subject-verb agreement, tense consistency, punctuation, capitalization, use of correct articles and correct present perfect and past perfect tense.

USER: Edit the following for spelling and grammar mistakes:

{user_text}

ASSISTANT:'''

output = llm(
    prompt,
    max_tokens=512,
#    temperature=0.1,
#    top_p=0.8,
    echo=False,
    stop=["#"],
)
output_text = output["choices"][0]["text"].strip()

"""
