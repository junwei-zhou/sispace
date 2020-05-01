from socket import *

tcpClientSocket = socket(AF_INET,SOCK_STREAM)
seraddr=('192.168.8.107',7788)
tcpClientSocket.connect(seraddr)
sendData = input('input :').encode('utf-8')
tcpClientSocket.send(sendData)
recvData = tcpClientSocket.recv(1024)
#print('recv the data :%s'%recvData)
print('recv the data :',recvData)
tcpClientSocket.close()
