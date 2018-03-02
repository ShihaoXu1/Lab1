import socket,sys
HOST = ''
PORT = 8999
ADDR =(HOST,PORT)
BUFSIZE = 1024

sock = socket.socket()
try:
    sock.connect(ADDR)
    print('have connected with server')

    while True:
      data = raw_input(">")
      if len(data)>0:
        print('send:',data)
        sock.sendall(data.encode('utf-8')) 
        recv_data = sock.recv(BUFSIZE)
        print(recv_data)
      else:
        sock.close()
        break
except Exception:
    print('error')
    sock.close()
    sys.exit()