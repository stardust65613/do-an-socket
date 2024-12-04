import socket
import threading
import os
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
LIST_FILE_PATH = "list.txt"
DOWNLOAD_PATH = "Download/"
