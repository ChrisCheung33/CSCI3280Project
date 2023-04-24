import socket

# Host = '0.0.0.0'
# Port = 8000

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((Host,Port))

# while True:
#     outdata = input('please input message: ')
#     print('send: ' + outdata)
#     s.send(outdata.encode())
    
#     indata = s.recv(1024)
#     if len(indata) == 0:
#         s.close()
#         print('server closed connection.')
#         break
#     print('recv: {}'.format(indata.decode()))

(HOST,PORT)=('localhost',19123)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))

with open('./music/numb.wav', 'rb') as f:
  for l in f: s.sendall(l)
s.close()