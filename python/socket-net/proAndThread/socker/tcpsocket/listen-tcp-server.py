from socket import *
from time import sleep
tcpSerSocket = socket(AF_INET, SOCK_STREAM)
address = ('', 9788)
tcpSerSocket.bind(address)
connNum = int(input("the max links:"))
tcpSerSocket.listen(connNum)
while True:
    newSocket, clientAddr = tcpSerSocket.accept()
    print (clientAddr)
    sleep(1)
