from socket import *
udpSocket = socket(AF_INET,SOCK_DGRAM)
sendAddr=('192.168.8.107',8778)
sendData=input('please input something:').encode('utf-8')
udpSocket.sendto(sendData,sendAddr)
recvData=udpSocket.recvfrom(1024)
print(recvData)
udpSocket.close()
