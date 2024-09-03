# MSR-necromancer: Using large language models to access old wisdom
Molten salt reactors (MSRs) were built and operated in the 1950s and 60s at the Oak Ridge National Laboratory. During this period, a lot of technical and scientific knowledge was developed and written down. We are using large language models to make this wealth of wisdom available for researchers in the current century.
This code presents an introduction to leveraging openly available foundational large language models (FLLM) into virtual subject-matter experts (ViSMErs), demonstrating locally executed retrieval-augmented text generation using pre-processed dataset of the historical MSR documents. 

# Purpose
Create an offline usable knowledge base distilled from the 1950s and newer MSR work, to make it available for 21st century researchers. 

# How to run the basic RAG on local GPU
- First, clone the repository and navigate to directory *examples/01-RAG*.
- Second, install the Python environment  using a shell *script 01_instal_env.sh*. 
You may need to edit variables in the script depending on your Python and CUDA versions. 
- Third, check that the paths and parameters at the beginning of the Python script 02_run_RAG.py are suitable for your local computer. In particular, the number of model layers to put on GPU may need to be changed depending on your GPU’s memory. The 13B model with the RAG takes about 12 GB of GPU RAM, and fits into a 16 GB GPU, such as NVIDIA A4000, along with the regular desktop loads.
- Lastly, run the script in Python and start asking about MSRs!

First time running the script will download the FLLM  blob, as well as smaller files needed by the tokenizer of the cleaned MSR historical documents used for augmentation.
These are saved in /tmp/llama_index/ and reused on rerun.
