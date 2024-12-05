from socket import *
from threading import Thread

# Ham lay kich thuoc file (bytes)
def getNumOfBytes(size):
    res = 0
    i = 0
    while i < len(size):
        if size[i] >= '0' and size[i] <= '9':
            i += 1
        else:
            break
    res = int(size[:i])
    if size[i:] == "KB":
        res = res*1024
    elif size[i:] == "MB":
        res = res*1024*1024
    elif size[i:] == "GB":
        res = res*1024*1024*1024
    return res
            
        

def getListOfFile(file_name):
    list = {}
    f = open(file_name,"rt")
    for line in f:#Doc tung dong trong file
        temp = line.split()
        list[temp[0]] = getNumOfBytes(temp[1])
    f.close()
    return list

def accept_connections():
    client, addr = server.accept()
    Thread(target=handle_client, args=(client,)).start()

def handle_client(client): 
    data = ""
    for file in list_of_file:
        # Gui list file 
        data += file + " " + str(list_of_file[file]) + "\n"
    client.send(bytes(data,"utf8"))
    
        

def handle_downloading(client, file_name, chunk, offset):
    a = 0
    


HOST = '127.0.0.1'
PORT = 12345
BUFFSIZE = 1024

server = socket(AF_INET,SOCK_STREAM)
server.bind((HOST,PORT))
list_of_file = getListOfFile("input.txt")

if __name__ == "__main__":
    server.listen(5)
    ACCEPT_THREAD = Thread(target=accept_connections)
    
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()