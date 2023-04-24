import socket
import threading
import time
import json


import csv
import socket
import threading

class Network:
    def __init__(self, tracker_server_ip, tracker_server_port):
        self.tracker_server_ip = tracker_server_ip
        self.tracker_server_port = tracker_server_port
        self.register_with_tracker_server()
        self.start_distributed_sharing()

    def register_with_tracker_server(self):
        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli.connect((self.tracker_server_ip, self.tracker_server_port))
        cli.send('my_identifier'.encode('utf-8'))
        cli.close()

    def get_ip_addresses(self):
        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli.connect((self.tracker_server_ip, self.tracker_server_port))
        data = cli.recv(4096)
        if data:
            ip_addresses = data.decode('utf-8').split(',')
            print(ip_addresses)
            return ip_addresses
        cli.close()
        return []

    def start_distributed_sharing(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind(('0.0.0.0', 44447))
        self.serv.listen(5)
        client_threads = []
        ip_addresses = self.get_ip_addresses()
        for ip in ip_addresses:
            client_threads.append(threading.Thread(target=self.client, args=(ip,)))
        for i in range(0, len(client_threads)):
            client_threads[i].start()
        print("Clients are running")
        while True:
            conn, addr = self.serv.accept()
            server_thread = threading.Thread(target=self.server, args=(conn, addr,))
            server_thread.start()
            print("New connection to server created!")

    def server(self, conn, addr):
        while True:
            data = ''
            try:
                data = conn.recv(4096)
            except Exception:
                print("Server: Lost a connection... Retrying...")
                time.sleep(5)
                break
            if not data: break
            try:
                query = data.decode('utf-8')
                results = self.search_music(query)
                conn.send(','.join(results).encode('utf-8'))
            except Exception:
                print("Server: Could not decode message: ", data)
            conn.close()
            print('Server: client disconnected')

    def search_music(self, query):
        results = []
        with open('music_database.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if query.lower() in row[0].lower():
                    results.append(row[0])
        return results

    def client(self, ip):
        self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            connected = False
            while not connected:
                try:
                    print("Client: Connecting to ", ip)
                    self.cli.connect((ip, 44447))
                    connected = True
                except Exception:
                    print('Client: Could not connect to ', ip, '. Retrying...')
                    time.sleep(5)
            while True:
                time.sleep(2)
                try:
                    query = input("Enter search query: ")
                    print("Client: Sending search query to ", ip)
                    self.cli.send(query.encode('utf-8'))
                    data = self.cli.recv(4096)
                    if data:
                        results = data.decode('utf-8').split(',')
                        print("Results from {}: {}".format(ip, results))
                except Exception:
                    print("Client: Could not send more data to ", ip)
                    break

network = Network('localhost', 12345)
