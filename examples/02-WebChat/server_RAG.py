#!/usr/bin/env python3

# Make sure you activate the Python environment first!
# $ source $HOME/.local/necromancer/bin/activate
"""
Socket server that accompanies web chat app
Ondrej Chvala <ochvala@utexas.edu>
"""
import socket
from typing import Optional

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import (messages_to_prompt, completion_to_prompt)
from llama_index.core import set_global_tokenizer
from transformers import AutoTokenizer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.core.types import ChatMessage

### Configurable parameters start ###

# Set either the full path to the model blob or the URL. The other shall be set to None.
my_model_url: Optional[str] = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf"
my_model_path: Optional[str] = None

# How many model layers to put on GPU? The full model is 9GB. Reduce this number if you have less GPU memory.
my_n_gpu_layers: int = 64

# Path to the directory with the historical MSR documents.
my_document_dir: str = "../../data/01_ANS_W2024_data"

### Configurable parameters end ###

print("*** Loading FLLM into memory ***")
# Instantiate FLLM
llm = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
    model_url=my_model_url,
    # Optionally, you can set the path to a pre-downloaded model instead of model_url
    model_path=my_model_path,
    temperature=0.1, max_new_tokens=1024,
    # Llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    context_window=3900,
    generate_kwargs={"top_p": 0.95},
    # Set to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": my_n_gpu_layers},
    messages_to_prompt=messages_to_prompt, completion_to_prompt=completion_to_prompt,
    verbose=False,
)

# Instantiate tokenizer for the dataset
print("*** Loading RAG ***")
set_global_tokenizer(AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf").encode)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Load documents for augmentation
documents = SimpleDirectoryReader(my_document_dir, recursive=True).load_data()

# Instantiate vector store index
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

# Set up the query engine with the document store
query_engine = index.as_query_engine(llm=llm)

# System prompt
my_system_prompt: str = """ \
You are an expert with deep knowledge in nuclear, mechanical, and chemical engineering. \
You are also a helpful, respectful and honest assistant. \
Always answer as helpfully as possible and follow all given instructions. \
Do not speculate or make up information. 
"""


def chat_server():
    host = 'localhost'
    port = 65001
    print(f"*** Opening socket on {host} port {port} ***")

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))

    max_conns: int = 1
    socket_server.listen(max_conns)

    while True:
        print(f"*** Listening ***")
        conn, addr = socket_server.accept()
        user_q: str = conn.recv(4096).decode()
        response: str = query_engine.query(my_system_prompt + user_q).__str__()
        conn.sendall(response.encode('utf-8'))
        conn.close()


if __name__ == "__main__":
    chat_server()
