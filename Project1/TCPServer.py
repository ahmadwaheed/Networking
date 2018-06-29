# simple (non-concurrent) TCP server example
from socket import *
serverPort = 12000

listeningSocket = socket(AF_INET, SOCK_STREAM)
listeningSocket.bind(('', serverPort))
listeningSocket.listen(1)
print('Server ready, socket', listeningSocket.fileno(), 'listening on localhost :', serverPort)
while 1:
    connectionSocket, addr = listeningSocket.accept()
    firstName = connectionSocket.recv(1024)
    print('Got connection on socket', connectionSocket.fileno(), 'from', addr[0], ':', addr[1])
    connectionSocket.send(str.encode('Hi ' + bytes.decode(firstName) + '!'))
    lastName = connectionSocket.recv(1024)
    connectionSocket.send(str.encode('Hello ' + bytes.decode(firstName) + ' ' + bytes.decode(lastName)+ '!'))
    print('Closing socket', connectionSocket.fileno())
    connectionSocket.close()
