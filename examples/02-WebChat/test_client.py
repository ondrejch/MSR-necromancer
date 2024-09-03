#!/usr/bin/env python3
"""
Test client for the WebChat socks server
Ondrej Chvala <ochvala@utexas.edu>
"""
import socket


def run_client():
    host = 'localhost'
    port = 65001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    user_input: str = input("You: ")
    client_socket.send(user_input.encode('utf-8'))

    data = client_socket.recv(16384)
    print(f"Received message: {data.decode('utf-8')}")


if __name__ == "__main__":
    run_client()
