from socket import *
udpSocket = socket(AF_INET,SOCK_DGRAM)
binaddr=('192.168.8.107',8778)
udpSocket.bind(binaddr)
while True:
    recvData = udpSocket.recvfrom(1024)
    print(recvData)
udpSocket.close()
