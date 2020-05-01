from socket import *

tcpServerSocket = socket(AF_INET,SOCK_STREAM)
address = ('',7788)
tcpServerSocket.bind(address)
tcpServerSocket.listen(5)
newSocket,clientAddr = tcpServerSocket.accept()
recvData = newSocket.recv(1024)
#print('recve the data is %s' %recvData)
print('recve the data is ' ,recvData)
ndata='thank you'.encode('utf-8')
newSocket.send(ndata)
newSocket.close()
tcpServerSocket.close()
