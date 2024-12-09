import socket
import threading
import os
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
FILES_PATH = "Files/"  # Thư mục chứa file trên server
def send_file_chunk_socket(filename, start, end, conn):
    try:
        filepath = os.path.join(FILES_PATH, filename)
        if not os.path.exists(filepath):
            conn.sendall(b"ERROR")
            print(f"File {filename} does not exist.")
            return

        with open(filepath, 'rb') as file:
            file.seek(start)
            remaining_bytes = end - start + 1
            while remaining_bytes > 0:
                chunk_size = min(1024, remaining_bytes)
                data = file.read(chunk_size)
                if not data:
                    break
                conn.sendall(data)
                remaining_bytes -= len(data)
        print(f"Sent chunk {start}-{end} of file {filename}.")
    except Exception as e:
        print(f"Error when sending file chunk: {e}")
    finally:
        conn.close()

def send_file_multi_socket(filename, conn):
    try:
        filepath = os.path.join(FILES_PATH, filename)
        file_size = os.path.getsize(filepath)

        # Chia file thành 4 phần
        chunk_size = file_size // 4
        sockets = []  # Danh sách các socket mới

        # Tạo 4 kết nối socket mới
        for i in range(4):
            # Mỗi socket sử dụng một port tăng dần
            new_port = PORT + i + 1
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.bind((SERVER, new_port))
            new_socket.listen(1)
            sockets.append((new_socket, new_port))

        # Gửi danh sách port cho client
        ports = " ".join([str(port) for _, port in sockets])
        conn.sendall(ports.encode(FORMAT))

        # Chờ client kết nối tới từng socket
        threads = []
        for i, (sock, _) in enumerate(sockets):
            start = i * chunk_size
            end = start + chunk_size - 1 if i < 3 else file_size - 1
            client_conn, client_addr = sock.accept()
            print(f"Client {client_addr} connected to socket {i + 1}.")
            thread = threading.Thread(target=send_file_chunk_socket, args=(filename, start, end, client_conn))
            threads.append(thread)
            thread.start()

        # Đợi tất cả các luồng hoàn thành
        for thread in threads:
            thread.join()

        print(f"File {filename} sent using 4 sockets.")
    except Exception as e:
        print(f"Error when sending file with multiple sockets: {e}")

def handle_client(conn, addr):
    try:
        print(f"Connected by {addr}")

        # Gửi danh sách file tới client
        file_list = os.listdir(FILES_PATH)
        if not file_list:
            conn.sendall("No files available".encode(FORMAT))
            return

        file_list_str = "\n".join(file_list)
        conn.sendall(file_list_str.encode(FORMAT))
        print("Sent list of files to client.")

        while True:
            # Nhận yêu cầu từ client
            request = conn.recv(1024).decode(FORMAT)
            if not request:
                break

            parts = request.split()
            command = parts[0]

            if command == "DOWNLOAD":
                filename = parts[1]
                send_file_multi_socket(filename, conn)
            else:
                conn.sendall(b"INVALID COMMAND")
                print(f"Invalid command received: {request}")
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

def start_server():
    os.makedirs(FILES_PATH, exist_ok=True)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(10)
    print(f"Server started on {SERVER}:{PORT}")

    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"Active connections: {threading.active_count() - 1}")
        except Exception as e:
            print(f"Error accepting connections: {e}")

if __name__ == "__main__":
    start_server()
