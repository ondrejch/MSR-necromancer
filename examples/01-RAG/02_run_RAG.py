

# Make sure you activate the Python environment first!
# $ source $HOME/.local/necromancer/bin/activate
"""
Script to run the MSR Necromancer RAG session. Pulled together from and inspired by llamaindex example:
https://docs.llamaindex.ai/en/stable/examples/llm/llama_2_llama_cpp/

The purpose hof this script, much like with the example above, is to be illustrative and easy to use.
You are welcome to add pre-prompts, load it in the python shell (e.g., ipython) or Jupyter Notebook
to interact with the augmented model, turn it into a web service, etc.
Note that modifications here include changes in paths etc. as the API has evolved since the publication
of the above howto.

Ondrej Chvala <ochvala@utexas.edu>
"""
from typing import Optional

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import (messages_to_prompt, completion_to_prompt)
from llama_index.core import set_global_tokenizer
from transformers import AutoTokenizer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.types import ChatMessage

### Configurable parameters start ###

# Set either the full path to the model blob or the URL. The other shall be set to None.
my_model_url: Optional[str] = \
    "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf"
my_model_path: Optional[str] = None

# How many model layers to put on GPU? The full model is 9GB. Reduce this number if you have less GPU memory.
# 1 layer is approximately 400 MB of GPU RAM. Setting 64 layers reliably loads the whole model in GPU RAM.
# An Ubuntu 24.04 laptop with 4 GB GPU RAM (TU117GLM) can only load 4 layers, since about 2 GBs are used by regular desktop loads.
my_n_gpu_layers: int = 64

# Path to the directory with the historical MSR documents.
my_document_dir: str = "../../data/01_ANS_W2024_data"

# System prompt
my_system_prompt: str = """ \
You are a professional scientists with deep knowledge in nuclear, mechanical, and chemical engineering. \
You are also a helpful, respectful and honest assistant. \
Always answer as helpfully as possible and follow all given instructions. \
Do not speculate or make up information. \
"""

# What questions would you like to ask
my_queries: list = [
    "Explain in detail what is a molten salt reactor",
    "Explain in detail what type and form of fuel is used in molten salt reactors",
    "Explain in detail what are advantages and disadvantages of molten salt reactors",
]

### Configurable parameters end ###

print("*** Loading FLLM into memory ***")
# Instantiate FLLM
llm = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
    model_url=my_model_url,
    # Optionally, you can set the path to a pre-downloaded model instead of model_url
    model_path=my_model_path,
    temperature=0.1, max_new_tokens=512,
    # Llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    context_window=3900,
    generate_kwargs={"top_p": 0.05},
    # Set to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": my_n_gpu_layers},
    messages_to_prompt=messages_to_prompt, completion_to_prompt=completion_to_prompt,
    verbose=False,
)

#  Query the base model
print("*** Querying the base model ***")
for my_llm_request in my_queries:
    print("*-- Question: " + my_llm_request)
    response_iter = llm.stream_complete(my_llm_request)
    for response in response_iter:
        print(response.delta, end="", flush=True)
    print("\n---")

# Instantiate tokenizer for the dataset
print("\n\n*** Loading RAG ***")
set_global_tokenizer(AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf").encode)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Load documents for augmentation
documents = SimpleDirectoryReader(my_document_dir, recursive=True).load_data()

# Instantiate vector store index
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
# Set up the query engine with the document store
query_engine = index.as_query_engine(llm=llm)

# Run text queries to the augmented model
print("*** Querying the augmented model ***")
for my_llm_request in my_queries:
    print("*-- Question: " + my_llm_request)
    response = query_engine.query(my_llm_request)
    print(response)
    print("\n---")
