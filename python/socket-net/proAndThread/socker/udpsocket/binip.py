from socket import *
udpSocket = socket(AF_INET,SOCK_DGRAM)
binaddr=('',8778)
udpSocket.bind(binaddr)
recvData = udpSocket.recvfrom(1024)
print(recvData)
udpSocket.close()
