# concurrent TCP server example
from socket import *
from multiprocessing import Process

serverPort = 12000
listeningSocket = socket(AF_INET, SOCK_STREAM)
listeningSocket.bind(('', serverPort))
listeningSocket.listen(1)
print('Server ready, listening on localhost :', serverPort)
while 1:
    connectionSocket, addr = listeningSocket.accept()
    pid = os.fork()
    if pid != 0: # parent
        connectionSocket.close()
        continue # skips back to accept() to listen for new connections
    
    # child - services the connected client
    listeningSocket.close();
    print('Got connection on socket', connectionSocket.fileno(), 'from', addr[0], ':', addr[1])
    firstName = connectionSocket.recv(1024)
    
    connectionSocket.send(str.encode('Hi ' + bytes.decode(firstName) + '!'))
    lastName = connectionSocket.recv(1024)
    
    connectionSocket.send(str.encode('Hello ' + bytes.decode(firstName) + ' ' + bytes.decode(lastName) + '!'))
    print('Closing socket', connectionSocket.fileno())
    connectionSocket.close()
    os._exit(0)
