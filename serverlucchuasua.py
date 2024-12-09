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

def send_file(filename, conn):
    filepath = os.path.join(DOWNLOAD_PATH, filename)  # Lấy đường dẫn đầy đủ của file trong thư mục Download
    try:
        if not os.path.isfile(filepath):
            conn.sendall(b"0")
            print(f"File {filename} does not exist")
            return

        total_size = os.path.getsize(filepath)
        conn.sendall(str(total_size).encode())  # Gửi tổng kích thước file

        # Đợi xác nhận từ client
        ack = conn.recv(1024).decode()
        if ack != 'OK':
            print(f"Client cannot receive the size of file {filename}")
            return

        sent_size = 0
        with open(filepath, 'rb') as f:
            while True:
                bytes_read = f.read(1024)
                if not bytes_read:
                    break
                conn.sendall(bytes_read)
                sent_size += len(bytes_read)
                print(f"\rSending progress {filename}: {(sent_size / total_size) * 100:.1f}%", end="")

        print(f" - File {filename} has been successfully sent!")
    except Exception as e:
        print(f"Error when sending file {filename}: {e}")
        conn.sendall(b"ERROR")

def handle_client(client_socket, addr):
    try:
        print(f"Connection from {addr}")

        # Gửi list file
        send_list_file(client_socket)

        while True:
            # Nhận tên file từ client
            filename = client_socket.recv(1024).decode().strip()
            if not filename:
                print(f"Client from {addr} has stopped")
                break

            send_file(filename, client_socket)

    except Exception as e:
        print(f"Error when handling connection from {addr}: {e}")

    finally:
        # Đóng kết nối với client
        client_socket.close()
        print(f"Connection from {addr} has been closed")

def start_server():
    # Thiết lập server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ADDR))
    server_socket.listen(10)

    print("Server IP:", SERVER)
    print("Server Port:", PORT)

    while True:
        try:
            # Chấp nhận kết nối từ client
            client_socket, addr = server_socket.accept()

            # Tạo một thread mới để xử lý client này
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

        except Exception as e:
            print(f"Error when handling connection: {e}")

if __name__ == "__main__":
    start_server()
