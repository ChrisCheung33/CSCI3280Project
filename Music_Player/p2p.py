import socket
import time
import json
import csv
import socket
import threading
import pandas as pd
from io import StringIO

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
            if(file_format == "csv"):
                buffer = b''
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    buffer += data
                strData=str(buffer,'utf-8')
                f.write(strData)
                data = StringIO(strData) 
                music_df = pd.read_csv(data)
            else:
                while True:
                    l = conn.recv(1024)
                    if not l: break
                    f.write(l)
        s.close()
        return music_df
    
    def client(self,file_name,file_format):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(self.server_tuple)

        with open(file_name+"."+file_format, 'rb') as f:
            for l in f: s.sendall(l)

        # close the connection with the client
        s.close()
    
    def post_database(self):
        self.client("music_database","csv")
            
    def add_connect_server_tuple(self,new_server_host):
        if len(self.connect_server_tuple_list) < 5:
            self.connect_server_tuple_list.append((new_server_host,8000))

    def get_online_df(self):
        return self.server("getdata", "csv")
    
