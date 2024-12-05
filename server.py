import socket
import threading
import os
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
LIST_FILE_PATH = "list.txt"
DOWNLOAD_PATH = "Download/"
def send_list_file(client_socket):
    try:
        with open(LIST_FILE_PATH, 'r') as file:
            file_list = file.read()
        client_socket.sendall(file_list.encode())
        print("Send list file successfully")
    except Exception as e:
        print(f"Error: {e}")

