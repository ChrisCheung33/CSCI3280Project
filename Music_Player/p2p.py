import socket
import threading
import time
import json
import csv
import socket
import threading

# Client: Send Data, Server: Recieve Data

class p2p_obj:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server_tuple = (host,port)
        self.connect_server_tuple_list = []
        
    def server(self,file_name,file_format):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self.server_tuple)
        s.listen(1)
        conn, addr = s.accept()
        
        if file_format == "wav":
            open_mode = 'wb'
        else:
            open_mode = 'w'
        
        with open(file_name+"."+file_format,open_mode) as f:
            while True:
                if(file_format == "csv"):
                    data = conn.recv(1024)
                    f.write(data.decode('utf-8'))
                else:
                    l = conn.recv(1024)
                    if not l: break
                    f.write(l)
            s.close()
    
    def client(self,file_name,file_format):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(self.server_tuple)

        if(file_format == "wav"):
            with open(file_name+file_format, 'rb') as f:
                for l in f: s.sendall(l)
        elif(file_format == "csv"):
            while True:
                # open the .csv file and read its content
                with open('music_database.csv', 'r') as f:
                    data = f.read()

                # send the content of the .csv file to the client
                s.sendall(data.encode('utf-8'))

        # close the connection with the client
        s.close()
    
    def post_database(self):
        self.client("music_database","csv")
            
    def add_connect_server_tuple(self,new_server_host):
        if len(self.connect_server_tuple_list) < 5:
            self.connect_server_tuple_list.append((new_server_host,8000))

    def get_online_csv(self):
        self.server("getdata", "csv")
    
