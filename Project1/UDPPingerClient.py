

import time
import select
from socket import *
import sys
from datetime import date, datetime

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(1)
#dateList = []
#todaysDate = datetime.date.today()
#dateList.append(todaysDate)
#UTCtiming = date.utcn
#UTCow()
#clientSocket.sendto(message.encode(),(serverName,serverPort))
#clientSocket.connect((serverName,serverPort))

#ping ten times
for testTime in range(10):

    #sending time
    sendingTime = time.time()

    #creating message
    message = 'PING ' + str(testTime + 1) + " " + str(time.strftime("%D %a %H:%M:%S")+ " UTC")


    #sending data to server
    clientSocket.sendto(message.encode(),(serverName, serverPort))

    try:
        #receiving message from server
        message,address = clientSocket.recvfrom(1024)

        #this is the receiving time
        receivingTime = time.time()

        #getting response time
        RTT = receivingTime - sendingTime

        #modifting the message and printing modified message
        modifiedMessage = message.upper()

        print (bytes.decode(modifiedMessage))
        #print(message)
        print ("RTT:  ", RTT, "\n")
        #print (RTT)

        #printing round trip value
    #print ("Round Trip Time", RTT)

    except timeout:
        print ("REQUEST TIMED OUT")

clientSocket.close()
#return ("I am done")
            # Send a message to server
            # Then try to recieve a message from the server
            # if u recieve a message back; capitalize it and print the uncapitalized statement , capitalized statement , and how much total time it took .
            # if u dont recieve message from server, print the uncapitalized statement and "Timed Out"
            #timed out is a timer ..
