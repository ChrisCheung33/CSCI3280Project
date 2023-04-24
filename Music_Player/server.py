import socket

# Host = '0.0.0.0'
# Port = 8000

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind((Host,Port))
# s.listen(5)

# print('server start at:{}:{}'.format(Host,Port))
# print('wait for connection...')

# while True:
#     conn, addr = s.accept()
#     print('connected by ' + str(addr))
    
#     while True:
#         indata = conn.recv(1024)
#         if len(indata) == 0:
#             conn.close()
#             print('client closed connection.')
#             break
#         print('rev: ' + indata.decode())
        
#         outdata = 'echo ' + indata.decode()
#         conn.send(outdata.encode())
#     s.close()

(HOST,PORT) = ('localhost',19123)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

with open('output.wav','wb') as f:
  while True:
    l = conn.recv(1024)
    if not l: break
    f.write(l)
s.close()