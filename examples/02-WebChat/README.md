# Client-server examples

The scripts in this directory use the same "llama-index FLLM with RAG" approach as ../01-RAG/, but in a client-server architecture, where the clients communicate with the server using BSD sockets.


* server_RAG.py - server script that opens a socket on localhost:65001 and responds to client queries.
* test_client.py - simple CLI client in Python.
* chatmsr.html - web chatbot using HTML/CSS/Javascript, which uses querymsrn.php for the communication with the server.
* querymsrn.php - PHP script that reads user messages from XMLHttp/POST, passes them via socket to the server, and returns the response.
