import socket

class TrackerServer:
    def __init__(self, port):
        self.port = port
        self.ip_addresses = {}

    def start(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind(('0.0.0.0', self.port))
        self.serv.listen(5)
        while True:
            conn, addr = self.serv.accept()
            data = conn.recv(4096)
            if data:
                self.ip_addresses[data.decode('utf-8')] = addr[0]
                print(self.ip_addresses)
            conn.close()

tracker_server = TrackerServer(12345)
tracker_server.start()