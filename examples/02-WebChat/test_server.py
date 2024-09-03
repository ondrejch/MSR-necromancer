"""
Basic socks server test
Ondrej Chvala <ochvala@utexas.edu>
"""
import socket


def chat_server():
    # Socket server & port
    host = 'localhost'
    port = 65001

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))

    max_conns: int = 1
    socket_server.listen(max_conns)

    while True:
        conn, addr = socket_server.accept()
        user_q:str  = conn.recv(10240).decode()
        response: str = "Hello from the server!"
        conn.sendall(response.encode('utf-8'))
        conn.close()


if __name__ == "__main__":
    chat_server()
