from socket import *
from threading import Thread
import time

def getListOfFile(file_name, list):
    f = open(file_name,"rt")
    for line in f:#Doc tung dong trong file
        list.append(line)
    f.close()

def connect():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    msg = client_socket.recv(BUFFSIZE).decode("utf8")
    getServerFiles(msg)
    print("Cac file co the tai: ")
    for i in server_file:
        print(i + "-" + str(server_file[i]) + " bytes")
    
def getServerFiles(msg):
    temp = msg.split("\n")
    temp.remove("")
    for line in temp:
        t = line.split(" ")
        if server_file.get(t[0]) == None:
            server_file[t[0]] = int(t[1])
    

        
    
        


HOST = '127.0.0.1'
PORT = 12345
BUFFSIZE = 1024
file_list = []
server_file = {}
#khoang thoi gian duyet lại file 
interval = 5

if __name__ == "__main__":
    time1 = 0
    a = Thread(target=connect)
    b = Thread(target=connect)
    a.start()
    a.join()
    while True: 
        break
        time2 = time.time()
        #Duyet file input.txt 5s mot lan
        if time2 - time1 >= interval:
            Thread(target=getListOfFile("input.txt"), args =(file_list,) ).start()
            Thread(target=getListOfFile("input.txt"), args =(file_list,) ).join()
            time1 = time2
