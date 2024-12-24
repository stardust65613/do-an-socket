from socket import *
from threading import Thread
import threading
import time
import os

def getListOfFile(file_name, list):
    while not close_flag:
    #Duyet file input.txt 5s mot lan
        f = open(file_name,"rt")
        for line in f:#Doc tung dong trong file
            if line.strip('\n') == "" or line.strip("\n") in list:
                continue
            list.append(line.strip('\n'))
        f.close()
        time.sleep(5)
       

def printProgress(file,isFinish):
    global recv_bytes
    global chunk_sizes
    txt = ""
    for i in range(4):
        txt += "Downloading " + file + " part " + str(i+1) + "... " + str(round(recv_bytes[i]/chunk_sizes[i]*100)) + "%\n"
    print(txt,end = "")
    if isFinish == True:
        print("The file "+file+" has been downloaded successfully!")
        return
    print('\033[4A',end="")

def connect(address):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(address)
    msg = client_socket.recv(BUFFSIZE).decode("utf8")
    getServerFiles(msg)
    return client_socket

  
def getServerFiles(msg):
    temp = msg.split("\n")
    if "" in temp:
        temp.remove("")
    for line in temp:
        t = line.split(" ")
        if server_file.get(t[0]) == None:
            server_file[t[0]] = t[1]
    

def printServerFile():
    print("Server files:")
    for s in server_file:
        print(s + " " + server_file[s],end="\n")
    print("\n")
    
def handle_connection(socket,id,PATH):
    global file_list
    global close_flag
    while not close_flag :
        try:
            for file in file_list:
                if file in downloaded_file:
                    continue
                received_bytes = 0
                
                #Gui ten file can tai
                socket.send(str("DOWNLOAD " + file + " " + str(id)).encode("utf8"))
                data = socket.recv(BUFFSIZE)
                if not data:
                    continue
                if data.decode("utf8") == "ERROR":
                    #bo qua file neu server khong co
                    downloaded_file.append(file)
                    continue
                msg = data.decode("utf8").split()
                chunk_size = int(msg[0])
                chunk_sizes[id] = chunk_size
                start = int(msg[1])
                if os.path.isfile(PATH + file) == False:
                    with open(PATH + file,"wb") as f:
                        f.close()
                with open(PATH + file,"r+b") as f:
                    f.seek(start)
                    while True:
                        global recv_bytes
                        data = socket.recv(BUFFSIZE)
                        received_bytes += len(data)
                        recv_bytes[id] = received_bytes
                        f.write(data)
                        #tim socket tai cham nhat
                        mn = min(recv_bytes)
                        min_id = recv_bytes.index(mn)
                        #xuat ra man hinh qua trinh tai
                        if id == min_id:
                            printProgress(file,False)
                        if received_bytes >= chunk_size:
                            f.close()
                            break
                    barrier.wait()
                    #thong bao khi tai hoan tat
                    if id == 0:
                        printProgress(file,True)
                    barrier.wait()
                    downloaded_file.append(file)
                    recv_bytes[id] = 0

        except KeyboardInterrupt:
            break
         


FINISHH = False
BUFFSIZE = 1024
file_list = []
downloaded_file = []
client_sockets = []
server_file = {}
chunk_sizes = [0,0,0,0]
recv_bytes = [0,0,0,0]
barrier = threading.Barrier(4)
#khoang thoi gian duyet lại file 
interval = 5
close_flag = False

if __name__ == "__main__":
    HOST = input("Nhap IP: ")  
    PORT = int(input("Nhap port: "))
    PATH = os.getcwd() + "\\"
    ADDRESS = (HOST,PORT)
    server_file_display = False
    connections = 4  # Number of sockets to open
    threads = []
    num = 0
    for i in range(connections):
        new_soc = connect(ADDRESS)
        client_sockets.append(new_soc)
        
    print("Connection established")    

    if server_file_display == False:
        printServerFile()
        server_file_display = True
        update_files_thread = Thread(target=getListOfFile, args = ("input1.txt",file_list),daemon=True)
        update_files_thread.start()
        for i in range(connections):
            thread = Thread(target=handle_connection,args=(client_sockets[i],i,PATH),daemon=True)
            threads.append(thread)
            thread.start()              
        
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            close_flag = True
            for thread in threads:
                thread.join()
            threads.clear()
            update_files_thread.join()
            for soc in client_sockets:
                soc.close()

